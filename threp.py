from utils import unsigned_int, unsigned_char
from struct import pack
from common import decode, decompress
from math import ceil, floor

_keys = [0xf0a1, 0xfca1, 0xfda1, 0xfda1, 0xfba1, 0x49a8, 0x4ca8, 0x49a8, 0xfaa1, 0x4aa8, 0x4ba8, 0x4aa8, 0xfba1, 0x49a8,
         0x4ca8, 0x49a8]
keys = [pack('I', key).decode('gbk')[0] for key in _keys]

work_attr={'10':[0x72303174, 0x4c, 0x50, 0x54, 0x58, 0x5c, 0x64, 0x1c4, 0x10, 0x400, 0xaa, 0xe1, 0x80, 0x3d, 0x7a, 0x8, 0x0],
           '11':[0x72313174, 0x58, 0x5c, 0x60, 0x64, 0x68, 0x70, 0x90, 0x14, 0x800, 0xaa, 0xe1, 0x40, 0x3d, 0x7a, 0x8, 0x0],
           '12':[0x72323174, 0x58, 0x5c, 0x60, 0x64, 0x68, 0x70, 0xa0, 0x14, 0x800, 0x5e, 0xe1, 0x40, 0x7d, 0x3a, 0x8, 0x0],
           '13':[0x72333174, 0x58, 0x5c, 0x60, 0x64, 0x68, 0x84, 0xc4, 0x14, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x8, -0x10],
           '14':[0x72333174, 0x78, 0x7c, 0x80, 0x84, 0x88, 0xa4, 0xdc, 0x14, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x8, -0x10],
           '15':[0x72353174, 0x88, 0x8c, 0x90, 0x94, 0x98, 0xc8, 0x238, 0x14, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x1c, -0x24],
           '16':[0x72363174, 0x80, 0x84, 0x9c, 0x8c, 0x90, 0xc8, 0x294, 0x14, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x20, -0x28],
           '128': [0x72383231, 0x58, 0x5c, 0x60, 0x64, 0x68, 0x70, 0x90, 0x14, 0x800, 0x5e, 0xe7, 0x80, 0x7d, 0x36, 0x8, 0x0]}

dzz_attr=['A1-1','A1-2','A1-3','A2-2','A2-3','B1-1','B1-2','B1-3','B2-2','B2-3','C1-1','C1-2','C1-3','C2-2','C2-3','Extra','All','All','All','All','All','All','All']

def threp_decodedata(buffer, work):
    length = unsigned_int(buffer, 0x1c)
    dlength = unsigned_int(buffer, 0x20)
    decodedata = bytearray(dlength)
    rawdata = bytearray(buffer[0x24:])
    decode(rawdata, length, work_attr[work][9], work_attr[work][10], work_attr[work][11])
    decode(rawdata, length, work_attr[work][12], work_attr[work][13], work_attr[work][14])
    decompress(rawdata, decodedata, length)

    return decodedata


def threp_cut(decodedata, work):
    info = {'meta': decodedata[:work_attr[work][6]], 'stages': {}, 'stage': None,
            'character': None, 'ctype': None, 'rank': None, 'clear': None,
            'code': work_attr[work][0]}

    #f=open('rep1284.txt', 'wb')
    #f.write(decodedata)
    #f.close()

    stage = decodedata[work_attr[work][1]]
    character = unsigned_char(decodedata, work_attr[work][2])
    ctype = unsigned_char(decodedata, work_attr[work][3])
    rank = unsigned_char(decodedata, work_attr[work][4])
    clear = unsigned_char(decodedata, work_attr[work][5])

    info['stage'] = stage
    info['character'] = character
    info['ctype'] = ctype
    info['rank'] = rank
    info['clear'] = clear

    stagedata = work_attr[work][6]

    score = list(range(6))

    for i in range(1, stage):
        stagedata += work_attr[work][7] + unsigned_int(decodedata, stagedata + work_attr[work][15])
        score[i - 1] = unsigned_int(decodedata, stagedata + 0xc)
    score[stage - 1] = unsigned_int(decodedata, work_attr[work][8])

    stagedata = work_attr[work][6] + work_attr[work][16]
    for l in range(stage):
        stage_info = {'score': None, 'frame': None, 'llength': None, 'faith': None,
                      'bin': {'header': None, 'replay': None, 'tail': None},
                      'index': {'header': None, 'replay': None, 'tail': None}}
        stage_info['score'] = score[l]
        info['stages'][l] = stage_info

        replaydata = stagedata + work_attr[work][7]
        frame = unsigned_int(decodedata, stagedata + 0x4)
        llength = unsigned_int(decodedata, stagedata + 0x8)
        if frame * 6 + ceil(frame / 30) == llength:
            pass
        elif frame * 3 + ceil(frame / 60) == llength:
            frame //= 2
        else:
            print('!Unknow frame pattern, try to detect true frame size througn stage length')
            frame = floor(llength / (6 + 1 / 30))

        stage_info['score'] = score[l]
        stage_info['frame'] = frame
        stage_info['llength'] = llength
        stage_info['bin']['header'] = decodedata[stagedata: replaydata]
        stage_info['bin']['replay'] = decodedata[replaydata: (replaydata + (frame * 6))]
        stage_info['bin']['tail'] = decodedata[(replaydata + (frame * 6)): (replaydata + llength)]
        stage_info['index']['header'] = (stagedata, replaydata)
        stage_info['index']['replay'] = (replaydata, (replaydata + (frame * 6)))
        stage_info['index']['tail'] = ((replaydata + (frame * 6)), (replaydata + llength))

        info['stages'][l] = stage_info

        stagedata += llength + work_attr[work][7]

    return info


def th10type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'Reimu'
    elif character == 1:
        character_s = 'Marisa'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if ctype == 0:
        ctype_s = 'A'
    elif ctype == 1:
        ctype_s = 'B'
    elif ctype == 2:
        ctype_s = 'C'
    else:
        raise Exception("Unrecognized ctype {}".format(ctype))
    if rank == 0:
        rank_s = 'easy'
    elif rank == 1:
        rank_s = 'normal'
    elif rank == 2:
        rank_s = 'hard'
    elif rank == 3:
        rank_s = 'lunatic'
    elif rank == 4:
        rank_s = 'extra'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear == 8:
        clear_s = 'all'
    elif clear == 7:
        clear_s = 'extra'
    else:
        clear_s = str(clear)
    return character_s, ctype_s, rank_s, clear_s

def th11type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'Reimu'
    elif character == 1:
        character_s = 'Marisa'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if ctype == 0:
        ctype_s = 'A'
    elif ctype == 1:
        ctype_s = 'B'
    elif ctype == 2:
        ctype_s = 'C'
    else:
        raise Exception("Unrecognized ctype {}".format(ctype))
    if rank == 0:
        rank_s = 'easy'
    elif rank == 1:
        rank_s = 'normal'
    elif rank == 2:
        rank_s = 'hard'
    elif rank == 3:
        rank_s = 'lunatic'
    elif rank == 4:
        rank_s = 'extra'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear == 8:
        clear_s = 'all'
    elif clear == 7:
        clear_s = 'extra'
    else:
        clear_s = str(clear)
    return character_s, ctype_s, rank_s, clear_s

def th12type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'Reimu'
    elif character == 1:
        character_s = 'Marisa'
    elif character == 2:
        character_s = 'Sanae'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if ctype == 0:
        ctype_s = 'A'
    elif ctype == 1:
        ctype_s = 'B'
    else:
        raise Exception("Unrecognized ctype {}".format(ctype))
    if rank == 0:
        rank_s = 'easy'
    elif rank == 1:
        rank_s = 'normal'
    elif rank == 2:
        rank_s = 'hard'
    elif rank == 3:
        rank_s = 'lunatic'
    elif rank == 4:
        rank_s = 'extra'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear == 8:
        clear_s = 'all'
    elif clear == 7:
        clear_s = 'extra'
    else:
        clear_s = str(clear)
    return character_s, ctype_s, rank_s, clear_s

def th13type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'Reimu'
    elif character == 1:
        character_s = 'Marisa'
    elif character == 2:
        character_s = 'Sanae'
    elif character == 3:
        character_s = 'Youmu'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if rank == 0:
        rank_s = 'easy'
    elif rank == 1:
        rank_s = 'normal'
    elif rank == 2:
        rank_s = 'hard'
    elif rank == 3:
        rank_s = 'lunatic'
    elif rank == 4:
        rank_s = 'extra'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear == 8:
        clear_s = 'all'
    elif clear == 7:
        clear_s = 'extra'
    else:
        clear_s = str(clear)
    return character_s, "", rank_s, clear_s

def th14type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'Reimu'
    elif character == 1:
        character_s = 'Marisa'
    elif character == 2:
        character_s = 'Sakuya'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if ctype == 0:
        ctype_s = 'A'
    elif ctype == 1:
        ctype_s = 'B'
    else:
        raise Exception("Unrecognized ctype {}".format(ctype))
    if rank == 0:
        rank_s = 'easy'
    elif rank == 1:
        rank_s = 'normal'
    elif rank == 2:
        rank_s = 'hard'
    elif rank == 3:
        rank_s = 'lunatic'
    elif rank == 4:
        rank_s = 'extra'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear == 8:
        clear_s = 'all'
    elif clear == 7:
        clear_s = 'extra'
    else:
        clear_s = str(clear)
    return character_s, ctype_s, rank_s, clear_s

def th15type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'Reimu'
    elif character == 1:
        character_s = 'Marisa'
    elif character == 2:
        character_s = 'Sanae'
    elif character == 3:
        character_s = 'Reisen'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if rank == 0:
        rank_s = 'easy'
    elif rank == 1:
        rank_s = 'normal'
    elif rank == 2:
        rank_s = 'hard'
    elif rank == 3:
        rank_s = 'lunatic'
    elif rank == 4:
        rank_s = 'extra'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear == 8:
        clear_s = 'all'
    elif clear == 7:
        clear_s = 'extra'
    else:
        clear_s = str(clear)
    return character_s, "", rank_s, clear_s

def th16type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'Reimu'
    elif character == 1:
        character_s = 'Cirno'
    elif character == 2:
        character_s = 'Aya'
    elif character == 3:
        character_s = 'Marisa'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if ctype == 0:
        ctype_s = 'Spring'
    elif ctype == 1:
        ctype_s = 'Summer'
    elif ctype == 2:
        ctype_s = 'Autumn'
    elif ctype == 3:
        ctype_s = 'Winter'
    elif ctype == 4:
        ctype_s = 'Full'
    else:
        raise Exception("Unrecognized ctype {}".format(ctype))
    if rank == 0:
        rank_s = 'easy'
    elif rank == 1:
        rank_s = 'normal'
    elif rank == 2:
        rank_s = 'hard'
    elif rank == 3:
        rank_s = 'lunatic'
    elif rank == 4:
        rank_s = 'extra'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear == 8:
        clear_s = 'all'
    elif clear == 7:
        clear_s = 'extra'
    else:
        clear_s = str(clear)
    return character_s, ctype_s, rank_s, clear_s

def th128type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'A1'
    elif character == 1:
        character_s = 'A2'
    elif character == 2:
        character_s = 'B1'
    elif character == 3:
        character_s = 'B2'
    elif character == 4:
        character_s = 'C1'
    elif character == 5:
        character_s = 'C2'
    elif character == 6:
        character_s = 'Extra'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if rank == 0:
        rank_s = 'Easy'
    elif rank == 1:
        rank_s = 'Normal'
    elif rank == 2:
        rank_s = 'Hard'
    elif rank == 3:
        rank_s = 'Lunatic'
    elif rank == 4:
        rank_s = 'Extra'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear>=1 and clear<=23:
        clear_s = dzz_attr[clear-1]
    return character_s, "", rank_s, clear_s

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
    else:
        raise Exception("Unrecognized work {}".format(work))

    output['base_info']=' '.join([character, ctype, rank, clear])
    output['stage_score']=[]

    for l in range(stage):
        output['stage_score'].append(info['stages'][l]['score']*10)

    output['kb_action']=[]

    for l in range(stage):
        stage_info = info['stages'][l]
        replaydata = stage_info['bin']['replay']
        frame = stage_info['frame']
        skey = []
        for i in range(frame):
            if (i % 60 == 0):
                skey.append('[{0:<6}]'.format(i // 60))
            framekey = unsigned_int(replaydata, i * 6) >> 4 & 0xf
            skey.append(keys[framekey])
            if ((i + 1) % 60 == 0):
                output['kb_action'].append(''.join(skey))
                skey = []
        output['kb_action'].append(''.join(skey))

    return output

def load(file, work):
    from common import entry
    file, buffer, flength = entry(file)
    decodedata = threp_decodedata(buffer, work)
    return threp_cut(decodedata, work)

if __name__ == '__main__':
    #th = threp_output(load('th10_02.rpy', '10'), '10')
    #th = threp_output(load('th11_08.rpy', '11'), '11')
    #th = threp_output(load('th12_13.rpy', '12'), '12')
    #th = threp_output(load('th13_01.rpy', '13'), '13')
    #th = threp_output(load('th14_01.rpy', '14'), '14')
    #th = threp_output(load('th15_02.rpy', '15'), '15')
    #th = threp_output(load('th16_04.rpy', '16'), '16')
    th = threp_output(load('th128_03.rpy', '128'), '128')
    print(th['base_info'])