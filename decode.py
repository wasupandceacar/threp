from math import ceil
from time import localtime

from .utils import unsigned_int, unsigned_char, float
from .common import decode, decompress, entry
from .static import work_attr, skeys, kkeys, hmx_magicnumber, yym_magicnumber
from .type import *

def threp_decodedata(buffer):
    work_magicnumber = unsigned_int(buffer, 0)
    if work_magicnumber==hmx_magicnumber:
        return hmxrep_cut(buffer), '06'
    elif work_magicnumber==yym_magicnumber:
        return yymrep_cut(buffer), '07'
    else:
        is_2hu_replay = False
        for key, value in work_attr.items():
            if work_magicnumber == value['magic_number']:
                is_2hu_replay = True
                work = key
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

def hmxrep_cut(dat):
    rep_info = {}

    decodedata = bytearray(len(dat))
    mask = dat[0x0e]
    for i in range(0x0f):
        decodedata[i] = dat[i]
    for i in range(0x0f, len(dat)):
        decodedata[i] = (dat[i] + 0x100 - mask) & 0xff
        mask = (mask + 0x07) & 0xff

    #f=open('rep66.txt', 'wb')
    #f.write(decodedata)
    #f.close()

    date = decodedata[0x10:0x10 + 8]
    name = decodedata[0x19:0x19 + 8]
    char = decodedata[0x06]
    rank = decodedata[0x07]
    drop = float(decodedata, 0x2c)

    date = date.strip()
    date = "20" + date[6:8].decode('utf-8') + "/" + date[0:2].decode('utf-8') + "/" + date[3:5].decode('utf-8')
    rep_info['date'] = date.strip()
    rep_info['player'] = name.strip().decode('utf-8')
    chars = ("Reimu A", "Reimu B", "Marisa A", "Marisa B")
    levels = ("Easy", "Normal", "Hard", "Lunatic", "Extra")
    rep_info['base_info'] = chars[char]+" "+levels[rank]
    rep_info['slowrate'] = round(drop, 3)

    rep_info['stage_score'] = []
    rep_info['screen_action'] = []
    rep_info['keyboard_action'] = []

    for i in range(7):
        stage_offset=unsigned_int(decodedata, 0x34 + i * 0x4)
        if stage_offset!=0:
            rep_info['stage_score'].append(unsigned_int(decodedata, stage_offset))
            replay_offset=stage_offset + 0x10
            stage_replaydata=[]
            i=0x0
            frame=unsigned_int(decodedata, replay_offset + i)
            while frame!=9999999:
                press=(unsigned_int(decodedata, replay_offset + i + 0x4) >> 4) & 0xf
                i+=0x8
                stage_replaydata.append([frame, press])
                frame = unsigned_int(decodedata, replay_offset + i)
            kkey=[]
            skey=[]
            frame_count = 0
            for i in range(len(stage_replaydata)-1):
                for index in range(stage_replaydata[i][0], stage_replaydata[i+1][0]):
                    if (frame_count % 60 == 0):
                        skey.append('[{0:<6}]'.format(frame_count // 60))
                    skey.append(skeys[stage_replaydata[i][1]])
                    kkey.append(kkeys[stage_replaydata[i][1]])
                    if (frame_count + 1) % 60 == 0:
                        rep_info['screen_action'].append(''.join(skey))
                        rep_info['keyboard_action'].append(kkey)
                        skey = []
                        kkey = []
                    frame_count+=1
            rep_info['screen_action'].append(''.join(skey))
            rep_info['keyboard_action'].append(kkey)

    return rep_info

def yymrep_cut(dat):
    rep_info = {}

    decodedata = bytearray(len(dat))
    mask = dat[0x0d]
    for i in range(0x10):
        decodedata[i] = dat[i]
    for i in range(0x10, len(dat)):
        decodedata[i] = (dat[i] - mask) & 0xff
        mask = (mask + 0x07) & 0xff

    #f = open('rep711.txt', 'wb')
    #f.write(decodedata)
    #f.close()

    dat = decodedata
    # decompress
    v04 = 0
    v1c = 0
    v30 = 0
    v28 = 0
    v34 = 1
    v11 = 0x80
    v20 = 0
    # reinit v20
    for i in range(0,4):
        v20 = v20 * 0x100 + dat[0x17-i]
    v4b = []
    for i in range(0,0x16c80):
        v4b.append(0)

    rep_length=unsigned_int(dat, 0x4c)
    decodedata=bytearray(rep_length)
    for i in range(0x54):
        decodedata[i] = dat[i]

    index=0x54
    i=0x54
    while index < rep_length:
        flStopDoLoop = 0
        while index < rep_length:
            flFirstRun = 1
            tmpFirst = True
            while v30!=0 or tmpFirst:
                tmpFirst = False
                if v11==0x80:
                    v04=dat[i]
                    if(i-0x54 < v20):
                        i += 1
                    else:
                        v04 = 0
                    v28 += v04
                if flFirstRun == 1:
                    v1c = v04 & v11
                    v11 = v11 >> 1
                    if (v11 == 0):
                        v11=0x80
                    if (v1c == 0):
                        flStopDoLoop = 1
                        break
                    v30 = 0x80
                    v1c = 0
                    flFirstRun = 0
                else:
                    if (v11 & v04)!=0:
                        v1c=v1c | v30
                    v30=v30 >> 1
                    v11=v11 >> 1
                    if(v11==0):
                        v11=0x80
            if flStopDoLoop == 1:
                break
            decodedata[index] = v1c
            index+=1
            v4b[v34] = v1c & 0xff
            v34 = (v34+1) & 0x1fff
        if index > rep_length:
            break
        v30 = 0x1000
        v1c = 0
        while(v30!=0):
            if(v11==0x80):
                v04=dat[i]
                if i-0x54 < v20:
                    i += 1
                else:
                    v04 = 0
                v28 += v04
            if((v11 & v04)!=0):
                v1c = v1c | v30
            v30 = v30>>1
            v11 = v11>>1
            if(v11==0):
                v11 = 0x80
        v0c = v1c
        if v0c==0:
            break
        v30=8
        v1c=0
        while v30 != 0:
            if v11 == 0x80:
                v04=dat[i]
                if(i-0x54 < v20):
                    i += 1
                else:
                    v04 = 0
                v28 += v04
            if (v11 & v04)!=0:
                v1c=v1c|v30
            v30=v30>>1
            v11=v11>>1
            if(v11==0):
                v11=0x80
        v24 = v1c+2
        v10=0
        while v10<=v24 and index < rep_length:
            v2c=v4b[(v0c+v10)&0x1fff]
            decodedata[index] = v2c
            index+=1
            v4b[v34]=v2c & 0xff
            v34=(v34+1) & 0x1fff
            v10 += 1

    #f = open('rep7.txt', 'wb')
    #f.write(decodedata)
    #f.close()

    # raplay info
    date = decodedata[0x58:0x58+5]
    name = decodedata[0x5e:0x5e+8]
    char = decodedata[0x56]
    rank = decodedata[0x57]
    drop = float(decodedata, 0xcc)

    # [date, player, char, score, rank, version, drop]
    rep_info['date'] = date.strip().decode()
    rep_info['player'] = name.strip().decode()
    chars = ("Reimu A", "Reimu B", "Marisa A", "Marisa B", "Sakuya A", "Sakuya B")
    levels = ("Easy","Normal","Hard","Lunatic","Extra","Phantasm")
    rep_info['base_info'] = chars[char] + " " + levels[rank]
    rep_info['slowrate'] = round(drop, 3)

    rep_info['stage_score'] = []
    rep_info['screen_action'] = []
    rep_info['keyboard_action'] = []

    stage_end=unsigned_int(decodedata, 0x38)
    stage_offsets=[]

    for i in range(7):
        stage_offset = unsigned_int(decodedata, 0x1c + i * 0x4)
        if stage_offset != 0:
            rep_info['stage_score'].append(unsigned_int(decodedata, stage_offset) * 10)
            stage_offsets.append(stage_offset)

    stage_offsets.append(stage_end)

    for i in range(len(stage_offsets)-1):
        start = stage_offsets[i] + 0x28
        frame = int((stage_offsets[i+1]-stage_offsets[i]-0x28)/4)
        skey = []
        kkey = []
        for j in range(frame):
            if (j % 60 == 0):
                skey.append('[{0:<6}]'.format(j // 60))
            framekey = unsigned_int(decodedata, start + j * 4) >> 4 & 0xf
            skey.append(skeys[framekey])
            kkey.append(kkeys[framekey])
            if ((j + 1) % 60 == 0):
                rep_info['screen_action'].append(''.join(skey))
                rep_info['keyboard_action'].append(kkey)
                skey = []
                kkey = []
        rep_info['screen_action'].append(''.join(skey))
        rep_info['keyboard_action'].append(kkey)

    return rep_info

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
        # 红魔乡
        if work=='06' or work=='07':
            return decodedata
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
