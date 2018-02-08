from math import ceil
from time import localtime

from .utils import unsigned_int, unsigned_char, float
from .common import decode, decompress, entry
from .static import work_attr, skeys, kkeys
from .type import *

def threp_decodedata(buffer):
    work_magicnumber = unsigned_int(buffer, 0)
    is_2hu_replay=False
    for key, value in work_attr.items():
        if work_magicnumber==value['magic_number']:
            is_2hu_replay=True
            work=key
    if is_2hu_replay:
        length = unsigned_int(buffer, 0x1c)
        dlength = unsigned_int(buffer, 0x20)
        decodedata = bytearray(dlength)
        rawdata = bytearray(buffer[0x24:])
        decode(rawdata, length, work_attr[work]['decode_var1'], work_attr[work]['decode_var2'],
               work_attr[work]['decode_var3'])
        decode(rawdata, length, work_attr[work]['decode_var4'], work_attr[work]['decode_var5'],
               work_attr[work]['decode_var6'])
        decompress(rawdata, decodedata, length)
        return decodedata, work
    else:
        raise Exception("Unrecognized replay file")

def threp_cut(decodedata, work):
    info = {'stages': {}, 'stage': None,
            'character': None, 'ctype': None, 'rank': None, 'clear': None, 'player': '', 'slowrate': None, 'date': None}

    #f=open('rep143.txt', 'wb')
    #f.write(decodedata)
    #f.close()

    stage = decodedata[work_attr[work]['stage']]
    character = unsigned_char(decodedata, work_attr[work]['character'])
    ctype = unsigned_char(decodedata, work_attr[work]['ctype'])
    rank = unsigned_char(decodedata, work_attr[work]['rank'])
    clear = unsigned_char(decodedata, work_attr[work]['clear'])
    date = localtime(unsigned_int(decodedata, work_attr[work]['date']))

    info['stage'] = stage
    info['character'] = character
    info['ctype'] = ctype
    info['rank'] = rank
    info['clear'] = clear

    for i in range(8):
        info['player']+=chr(unsigned_char(decodedata, i))
    info['player']=info['player'].replace(" ", "")

    info['slowrate']=round(float(decodedata, work_attr[work]['slowrate']), 2)

    info['date']=str(date[0])+"/"+str(date[1]).zfill(2)+"/"+str(date[2]).zfill(2)+" "+str(date[3]).zfill(2)+":"+str(date[4]).zfill(2)

    stagedata = work_attr[work]['stagedata']

    score = list(range(6))

    if work=='125' or work=='143':
        score[0] = unsigned_int(decodedata, work_attr[work]['totalscoredata'])
        info['stage']=1
        stage=1
    else:
        for i in range(1, stage):
            stagedata += work_attr[work]['replaydata_offset'] + unsigned_int(decodedata, stagedata + work_attr[work]['scoredata_offset'])
            score[i - 1] = unsigned_int(decodedata, stagedata + 0xc)
        score[stage - 1] = unsigned_int(decodedata, work_attr[work]['totalscoredata'])

    stagedata = work_attr[work]['stagedata'] + work_attr[work]['stagedata_offset']
    for l in range(stage):
        stage_info = {'score': None, 'frame': None, 'llength': None, 'faith': None,
                      'bin': {'header': None, 'replay': None, 'tail': None},
                      'index': {'header': None, 'replay': None, 'tail': None}}
        stage_info['score'] = score[l]
        info['stages'][l] = stage_info

        replaydata = stagedata + work_attr[work]['replaydata_offset']
        frame = unsigned_int(decodedata, stagedata + 0x4)
        llength = unsigned_int(decodedata, stagedata + 0x8)
        if frame * 6 + ceil(frame / 30) == llength:
            perframe=6
        elif frame * 3 + ceil(frame / 30) == llength:
            perframe=3
        else:
            raise Exception("Replay file Frame decode error")

        stage_info['score'] = score[l]
        stage_info['frame'] = frame
        stage_info['llength'] = llength
        stage_info['bin']['header'] = decodedata[stagedata: replaydata]
        stage_info['bin']['replay'] = decodedata[replaydata: (replaydata + (frame * perframe))]
        stage_info['bin']['tail'] = decodedata[(replaydata + (frame * perframe)): (replaydata + llength)]
        stage_info['index']['header'] = (stagedata, replaydata)
        stage_info['index']['replay'] = (replaydata, (replaydata + (frame * perframe)))
        stage_info['index']['tail'] = ((replaydata + (frame * perframe)), (replaydata + llength))

        info['stages'][l] = stage_info

        stagedata += llength + work_attr[work]['replaydata_offset']

    return info

def threp_output(info, work):
    stage = info['stage']

    output = {}

    if work=='10':
        character, ctype, rank, clear = th10type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='11':
        character, ctype, rank, clear = th11type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='12':
        character, ctype, rank, clear = th12type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='13':
        character, ctype, rank, clear = th13type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='14':
        character, ctype, rank, clear = th14type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='15':
        character, ctype, rank, clear = th15type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='16':
        character, ctype, rank, clear = th16type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='128':
        character, ctype, rank, clear = th128type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='125':
        character, ctype, rank, clear = th125type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='143':
        character, ctype, rank, clear = th143type(info['character'], info['ctype'], info['rank'], info['clear'])
    else:
        raise Exception("Unrecognized work {}".format(work))

    output['base_info']=' '.join([character, ctype, rank, clear]).strip().replace("  ", " ")
    output['stage_score']=[]
    output['player']=info['player']
    output['slowrate'] = info['slowrate']
    output['date'] = info['date']

    for l in range(stage):
        output['stage_score'].append(info['stages'][l]['score']*work_attr[work]['score_rate'])

    output['screen_action']=[]
    output['keyboard_action']=[]

    # 文花帖DS的rep
    if work=='125':
        for l in range(stage):
            stage_info = info['stages'][l]
            replaydata = stage_info['bin']['replay']
            replaydata.append(0x00)
            frame = stage_info['frame']
            skey = []
            kkey = []
            for i in range(frame):
                if (i % 60 == 0):
                    skey.append('[{0:<6}]'.format(i // 60))
                framekey = unsigned_int(replaydata, i * 3) >> 3 & 0xf
                skey.append(skeys[framekey])
                kkey.append(kkeys[framekey])
                if ((i + 1) % 60 == 0):
                    output['screen_action'].append(''.join(skey))
                    output['keyboard_action'].append(kkey)
                    skey = []
                    kkey = []
            output['screen_action'].append(''.join(skey))
            output['keyboard_action'].append(kkey)
    else:
        for l in range(stage):
            stage_info = info['stages'][l]
            replaydata = stage_info['bin']['replay']
            frame = stage_info['frame']
            skey = []
            kkey = []
            for i in range(frame):
                if (i % 60 == 0):
                    skey.append('[{0:<6}]'.format(i // 60))
                framekey = unsigned_int(replaydata, i * 6) >> 4 & 0xf
                skey.append(skeys[framekey])
                kkey.append(kkeys[framekey])
                if ((i + 1) % 60 == 0):
                    output['screen_action'].append(''.join(skey))
                    output['keyboard_action'].append(kkey)
                    skey = []
                    kkey = []
            output['screen_action'].append(''.join(skey))
            output['keyboard_action'].append(kkey)

    return output

def load(file):
    try:
        work = 'noob'
        file, buffer, flength = entry(file)
        decodedata, work = threp_decodedata(buffer)
        replay_info = threp_output(threp_cut(decodedata, work), work)
        if len(replay_info['screen_action'])==0:
            # 解决th13和14文件头一样问题
            if work=='13':
                work='14'
                return threp_output(threp_cut(decodedata, work), work)
            elif work=='14':
                work='13'
                return threp_output(threp_cut(decodedata, work), work)
            else:
                raise Exception("Failed when decode replay file")
        else:
            return replay_info
    except:
        # 解决th13和14文件头一样问题
        if work == '13':
            work = '14'
            return threp_output(threp_cut(decodedata, work), work)
        elif work == '14':
            work = '13'
            return threp_output(threp_cut(decodedata, work), work)
        else:
            raise Exception("Failed to open replay file")
