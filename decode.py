from math import ceil, floor
from time import localtime

from threp.utils import unsigned_int, unsigned_char, float
from threp.common import decode, decompress, entry
from threp.static import work_attr, skeys, kkeys, oldwork_magicnumber_flc
from threp.type import *

def threp_decodedata(buffer):
    work_magicnumber = unsigned_int(buffer, 0)
    if work_magicnumber in oldwork_magicnumber_flc:
        return oldworkrep_cut(oldwork_magicnumber_flc[work_magicnumber], buffer)
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
            raise Exception("Bad file magic number")

def threp_cut(decodedata, work, frameignore = False):
    info = {'stages': {}, 'stage': None,
            'character': None, 'ctype': None, 'rank': None, 'clear': None, 'player': '', 'slowrate': None, 'date': None, 'error':[]}

    # f=open('rep161.txt', 'wb')
    # f.write(decodedata)
    # f.close()

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

    if work=='95':
        for i in range(7, 15):
            info['player'] += chr(unsigned_char(decodedata, i))
        info['player'] = info['player'].strip()
        info['character'] = 0
    else:
        for i in range(8):
            info['player'] += chr(unsigned_char(decodedata, i))
        info['player'] = info['player'].strip()

    info['slowrate']=round(float(decodedata, work_attr[work]['slowrate']), 2)

    info['date']=str(date[0])+"/"+str(date[1]).zfill(2)+"/"+str(date[2]).zfill(2)+" "+str(date[3]).zfill(2)+":"+str(date[4]).zfill(2)

    stagedata = work_attr[work]['stagedata']

    stagedata_t = work_attr[work]['stagedata'] + work_attr[work]['stagedata_offset']

    score = list(range(6))

    if work=='125' or work=='143' or work=='95' or work=='165':
        score[0] = unsigned_int(decodedata, work_attr[work]['totalscoredata'])
        info['stage']=1
        stage=1
    else:
        for i in range(1, stage):
            frame = unsigned_int(decodedata, stagedata_t + 0x4)
            llength = unsigned_int(decodedata, stagedata_t + 0x8)
            if frame * 6 + ceil(frame / 30) == llength:
                pass
            elif frame * 3 + ceil(frame / 30) == llength:
                pass
            else:
                if frameignore:
                    tmp_frame = frame
                    try:
                        frame = true_frame(llength)
                    except:
                        # 长度再次出错
                        frame = correct_true_frame(llength)
                        # 忽略帧数，强制保留单面长度
                        info['error'].append({'type': "length so short error",
                                              'message': str(i) + "面，读取到的单面长度：" + str(
                                                  llength) + "，判断为长度出错，尝试自动补正"})
                    # 忽略帧数，强制保留单面长度
                    info['error'].append({'type': "frame read error",
                                          'message': str(i) + "面，读取到的单面帧数：" + str(tmp_frame) + "，读取到的单面长度：" + str(
                                              llength) + "，帧数计算出的单面长度：" + str(tmp_frame * 6 + ceil(tmp_frame / 30)) + "，判断为单面帧数出错"})
                else:
                    # rep单面长度出错
                    info['error'].append({'type': "length read error",
                                          'message': str(i) + "面，读取到的单面帧数：" + str(frame) + "，读取到的单面长度：" + str(
                                              llength) + "，帧数计算出的单面长度：" + str(frame * 6 + ceil(frame / 30)) + "，判断为单面长度出错"})
                    llength = frame * 6 + ceil(frame / 30)
            stagedata_t += llength + work_attr[work]['replaydata_offset']
            stagedata += work_attr[work]['replaydata_offset'] + llength
            score[i - 1] = unsigned_int(decodedata, stagedata + 0xc)
        score[stage - 1] = unsigned_int(decodedata, work_attr[work]['totalscoredata'])

    stagedata = work_attr[work]['stagedata'] + work_attr[work]['stagedata_offset']

    for l in range(stage):
        stage_info = {'score': None, 'frame': None, 'llength': None, 'faith': None,
                      'bin': {'header': None, 'replay': None, 'tail': None},
                      'index': {'header': None, 'replay': None, 'tail': None}}

        replaydata = stagedata + work_attr[work]['replaydata_offset']
        frame = unsigned_int(decodedata, stagedata + 0x4)
        llength = unsigned_int(decodedata, stagedata + 0x8)

        if work=='95' or work=='165':
            perframe=6
            frame=int(llength/6)-2
        else:
            if frame * 6 + ceil(frame / 30) == llength:
                perframe = 6
            elif frame * 3 + ceil(frame / 30) == llength:
                perframe = 3
            else:
                if frameignore:
                    # 忽略帧数，强制保留单面长度
                    try:
                        frame = true_frame(llength)
                    except:
                        # 长度再次出错
                        frame = correct_true_frame(llength)
                    perframe = 6
                else:
                    # rep单面长度出错
                    llength = frame * 6 + ceil(frame / 30)
                    perframe = 6

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

#region 红妖永花

def oldworkrep_cut(work, data):
    funcdic = {
        '06': hmxrep_cut,
        '07': yymrep_cut,
        '08': yycrep_cut,
        '09': hyzrep_cut
    }
    return funcdic[work](data), work

# 红魔乡
def hmxrep_cut(dat):
    rep_info = {}

    rep_info["buffer"] = dat

    decodedata = bytearray(len(dat))
    mask = dat[0x0e]
    for i in range(0x0f):
        decodedata[i] = dat[i]
    for i in range(0x0f, len(dat)):
        decodedata[i] = (dat[i] + 0x100 - mask) & 0xff
        mask = (mask + 0x07) & 0xff

    # f=open('rep6rrrr.txt', 'wb')
    # f.write(decodedata)
    # f.close()

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
    rep_info['base_info'] = f"{chars[char]} {levels[rank]}"
    rep_info['base_infos'] = {
        "character": chars[char].split(" ")[0],
        "shottype": chars[char].split(" ")[1],
        "rank": levels[rank],
        "stage": ""
    }
    rep_info['slowrate'] = round(drop, 3)

    rep_info['stage_score'] = []
    rep_info['screen_action'] = []
    rep_info['keyboard_action'] = []

    rep_info['z_frame'] = []
    rep_info['x_frame'] = []
    rep_info['c_frame'] = []
    rep_info['shift_frame'] = []

    total_frame_count=0

    for i in range(7):
        stage_offset=unsigned_int(decodedata, 0x34 + i * 0x4)
        if stage_offset!=0:
            rep_info['stage_score'].append(unsigned_int(decodedata, stage_offset))
            replay_offset=stage_offset + 0x10
            stage_replaydata=[]
            i=0x0
            frame=unsigned_int(decodedata, replay_offset + i)
            while frame!=9999999:
                # 检测 z x c shift
                left_hand_flag = unsigned_int(decodedata, replay_offset + i + 0x4) & 0xf
                frame_dic = {
                    1: 'z_frame',
                    2: 'x_frame',
                    4: 'shift_frame'
                }
                if left_hand_flag in frame_dic:
                    rep_info[frame_dic[left_hand_flag]].append(frame)
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
                        skey.append(f'[{(frame_count // 60):<6}]')
                    skey.append(skeys[stage_replaydata[i][1]])
                    kkey.append(kkeys[stage_replaydata[i][1]])
                    if (frame_count + 1) % 60 == 0:
                        rep_info['screen_action'].append(''.join(skey))
                        rep_info['keyboard_action'].append(kkey)
                        skey = []
                        kkey = []
                    frame_count+=1
                    total_frame_count += 1
            rep_info['screen_action'].append(''.join(skey))
            rep_info['keyboard_action'].append(kkey)

    rep_info['error']=[]

    rep_info['frame_count']=total_frame_count

    return rep_info

# 妖妖梦
def yymrep_cut(dat):
    rep_info = {}

    decodedata = bytearray(len(dat))
    mask = dat[0x0d]
    for i in range(0x10):
        decodedata[i] = dat[i]
    for i in range(0x10, len(dat)):
        decodedata[i] = (dat[i] - mask) & 0xff
        mask = (mask + 0x07) & 0xff

    #f = open('rep715.txt', 'wb')
    #f.write(decodedata)
    #f.close()

    dat = decodedata
    # 解压
    v04 = 0
    v1c = 0
    v30 = 0
    v28 = 0
    v34 = 1
    v11 = 0x80
    v20 = 0

    for i in range(0,4):
        v20 = v20 * 0x100 + dat[0x17-i]
    v4b = []
    for i in range(0,0x16c80):
        v4b.append(0)

    rep_length=unsigned_int(dat, 0x18)

    # rep长度增长，处理某些短rep长度不够的bug
    decodedata=bytearray(rep_length+0x54)
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

    # f = open('rep73.txt', 'wb')
    # f.write(decodedata)
    # f.close()

    date = decodedata[0x58:0x58+5]
    name = decodedata[0x5e:0x5e+8]
    char = decodedata[0x56]
    rank = decodedata[0x57]
    drop = float(decodedata, 0xcc)

    rep_info['date'] = date.strip().decode()
    rep_info['player'] = name.strip().decode()
    chars = ("Reimu A", "Reimu B", "Marisa A", "Marisa B", "Sakuya A", "Sakuya B")
    levels = ("Easy","Normal","Hard","Lunatic","Extra","Phantasm")
    rep_info['base_info'] = f"{chars[char]} {levels[rank]}"
    rep_info['base_infos'] = {
        "character": chars[char].split(" ")[0],
        "shottype": chars[char].split(" ")[1],
        "rank": levels[rank],
        "stage": ""
    }
    rep_info['slowrate'] = round(drop, 3)
    rep_info['stage_score'] = []
    rep_info['screen_action'] = []
    rep_info['keyboard_action'] = []

    is_extra_or_phantasm=(unsigned_int(decodedata, 0x34)!=0)

    is_onestage=(unsigned_int(decodedata, 0x1c) == 0)

    stage_offsets = []

    if is_extra_or_phantasm:
        stage_start = unsigned_int(decodedata, 0x34)
        stage_end = unsigned_int(decodedata, 0x50)
        stage_offsets.append(stage_start)
        stage_offsets.append(stage_end)
        rep_info['stage_score'].append(unsigned_int(decodedata, stage_start) * 10)
    elif is_onestage:
        for i in range(6):
            stage_offset = unsigned_int(decodedata, 0x1c + i * 0x4)
            if stage_offset != 0:
                rep_info['stage_score'].append(unsigned_int(decodedata, stage_offset) * 10)
                stage_offsets.append(stage_offset)
                stage_end = unsigned_int(decodedata, 0x38 + i * 0x4)
                stage_offsets.append(stage_end)
                break
    else:
        stage_end = unsigned_int(decodedata, 0x38)

        for i in range(7):
            stage_offset = unsigned_int(decodedata, 0x1c + i * 0x4)
            if stage_offset != 0:
                rep_info['stage_score'].append(unsigned_int(decodedata, stage_offset) * 10)
                stage_offsets.append(stage_offset)

        stage_offsets.append(stage_end)

    rep_info['z_frame'] = []
    rep_info['x_frame'] = []
    rep_info['c_frame'] = []
    rep_info['shift_frame'] = []

    total_frame_count=0

    for i in range(len(stage_offsets)-1):
        start = stage_offsets[i] + 0x28
        frame = int((stage_offsets[i+1]-stage_offsets[i]-0x28)/4)
        skey = []
        kkey = []
        for j in range(frame):
            if (j % 60 == 0):
                skey.append(f'[{(j // 60):<6}]')
            framekey = unsigned_int(decodedata, start + j * 4) >> 4 & 0xf
            skey.append(skeys[framekey])
            kkey.append(kkeys[framekey])
            if ((j + 1) % 60 == 0):
                rep_info['screen_action'].append(''.join(skey))
                rep_info['keyboard_action'].append(kkey)
                skey = []
                kkey = []
            total_frame_count+=1
            # 检测 z x c shift
            left_hand_flag = unsigned_int(decodedata, start + j * 4) & 0xf
            frame_dic = {
                1: 'z_frame',
                2: 'x_frame',
                4: 'shift_frame'
            }
            if left_hand_flag in frame_dic:
                rep_info[frame_dic[left_hand_flag]].append(total_frame_count)
        rep_info['screen_action'].append(''.join(skey))
        rep_info['keyboard_action'].append(kkey)

    rep_info['error'] = []

    rep_info['frame_count'] = total_frame_count

    rep_info['z_frame'] = filter_constant_frame(rep_info['z_frame'])
    rep_info['x_frame'] = filter_constant_frame(rep_info['x_frame'])
    rep_info['shift_frame'] = filter_constant_frame(rep_info['shift_frame'])

    return rep_info

# 永夜抄
def yycrep_cut(dat):
    rep_info = {}

    decodedata = bytearray(len(dat))
    mask = dat[0x15]
    for i in range(0x18):
        decodedata[i] = dat[i]
    length = unsigned_int(dat, 0x0c)
    for i in range(0x18, length):
        decodedata[i] = (dat[i] + 0x100 - mask) & 0xff
        mask = (mask + 0x07) & 0xff

    rawdata = bytearray(decodedata[0x68:])

    dlength = unsigned_int(decodedata, 0x1c)
    newdecodedata = bytearray(dlength)
    decompress(rawdata, newdecodedata, length - 0x68)

    mergedecodedata=bytearray(dlength+0x68)
    for i in range(0x68):
        mergedecodedata[i]=decodedata[i]
    for i in range(0x68, dlength+0x68):
        mergedecodedata[i]=newdecodedata[i-0x68]

    # f = open('rep8rrr.txt', 'wb')
    # f.write(mergedecodedata)
    # f.close()

    decodedata=mergedecodedata

    date = decodedata[0x6c:0x6c + 5]
    name = decodedata[0x72:0x72 + 8]
    char = decodedata[0x6a]
    rank = decodedata[0x6b]
    drop = float(decodedata, 0x118)

    rep_info['date'] = date.strip().decode()
    rep_info['player'] = name.strip().decode()
    chars = ("Rm & Yk", "Ms & Al", "Sk & Rr", "Ym & Yy", "Reimu", "Yukari", "Marisa", "Alice", "Sakuya", "Remilia", "Youmu", "Yuyuko")
    levels = ("Easy", "Normal", "Hard", "Lunatic", "Extra")
    spellid=decodedata[0x7c]+256*decodedata[0x7d]
    rep_info['base_infos'] = {
        "character": chars[char],
        "shottype": "",
        "stage": ""
    }
    if spellid!=65535:
        rep_info['base_info'] = f"{chars[char]} Spell No.{spellid+1}"
        rep_info['base_infos']['rank'] = f"Spell No.{spellid+1}"
    else:
        rep_info['base_info'] = f"{chars[char]} {levels[rank]}"
        rep_info['base_infos']['rank'] = levels[rank]
    rep_info['slowrate'] = round(drop, 3)
    rep_info['stage_score'] = []
    rep_info['screen_action'] = []
    rep_info['keyboard_action'] = []

    is_extra = (unsigned_int(decodedata, 0x40) != 0)

    is_onestage = (unsigned_int(decodedata, 0x20) == 0)

    stage_offsets = []

    stage_dic = {
        3: "4A",
        4: "4B",
        6: "6A",
        7: "6B"
    }

    if is_extra:
        stage_start = unsigned_int(decodedata, 0x40)
        stage_end = unsigned_int(decodedata, 0x64)
        stage_offsets.append(stage_start)
        stage_offsets.append(stage_end)
        rep_info['stage_score'].append(unsigned_int(decodedata, stage_start) * 10)
    elif is_onestage:
        for i in range(8):
            stage_offset = unsigned_int(decodedata, 0x20 + i * 0x4)
            if stage_offset != 0:
                if i in stage_dic:
                    stage = stage_dic[i]
                    rep_info['base_info'] += f" {stage}"
                    rep_info['base_infos']['stage'] += stage
                rep_info['stage_score'].append(unsigned_int(decodedata, stage_offset) * 10)
                stage_offsets.append(stage_offset)
                stage_end = unsigned_int(decodedata, 0x44 + i * 0x4)
                stage_offsets.append(stage_end)
                break
    else:
        stage_end = unsigned_int(decodedata, 0x44)

        for i in range(9):
            stage_offset = unsigned_int(decodedata, 0x20 + i * 0x4)
            if stage_offset != 0:
                if i in stage_dic:
                    stage = stage_dic[i]
                    rep_info['base_info'] += f" {stage}"
                    rep_info['base_infos']['stage'] += stage
                rep_info['stage_score'].append(unsigned_int(decodedata, stage_offset) * 10)
                stage_offsets.append(stage_offset)

        stage_offsets.append(stage_end)

    rep_info['z_frame'] = []
    rep_info['x_frame'] = []
    rep_info['c_frame'] = []
    rep_info['shift_frame'] = []

    total_frame_count=0

    for i in range(len(stage_offsets) - 1):
        start = stage_offsets[i] + 0x20
        frame = int((stage_offsets[i + 1] - stage_offsets[i] - 0x20) / 2)
        skey = []
        kkey = []
        for j in range(frame):
            if (j % 60 == 0):
                skey.append(f'[{(j // 60):<6}]')
            framekey = unsigned_int(decodedata, start + j * 2) >> 4 & 0xf
            skey.append(skeys[framekey])
            kkey.append(kkeys[framekey])
            if ((j + 1) % 60 == 0):
                rep_info['screen_action'].append(''.join(skey))
                rep_info['keyboard_action'].append(kkey)
                skey = []
                kkey = []
            total_frame_count+=1
            # 检测 z x c shift
            left_hand_flag = unsigned_int(decodedata, start + j * 2) & 0xf
            frame_dic = {
                1: 'z_frame',
                2: 'x_frame',
                4: 'shift_frame'
            }
            if left_hand_flag in frame_dic:
                rep_info[frame_dic[left_hand_flag]].append(total_frame_count)
        rep_info['screen_action'].append(''.join(skey))
        rep_info['keyboard_action'].append(kkey)

    rep_info['error'] = []

    rep_info['frame_count'] = total_frame_count

    rep_info['z_frame'] = filter_constant_frame(rep_info['z_frame'])
    rep_info['x_frame'] = filter_constant_frame(rep_info['x_frame'])
    rep_info['shift_frame'] = filter_constant_frame(rep_info['shift_frame'])

    return rep_info

# 花映冢
def hyzrep_cut(dat):
    rep_info = {}

    decodedata = bytearray(len(dat))
    mask = dat[0x15]
    for i in range(0x18):
        decodedata[i] = dat[i]
    length = unsigned_int(dat, 0x0c)
    for i in range(0x18, length):
        decodedata[i] = (dat[i] + 0x100 - mask) & 0xff
        mask = (mask + 0x07) & 0xff

    rawdata = bytearray(decodedata[0xc0:])

    dlength = unsigned_int(decodedata, 0x1c)
    newdecodedata = bytearray(dlength)
    decompress(rawdata, newdecodedata, length - 0xc0)

    mergedecodedata = bytearray(dlength + 0xc0)
    for i in range(0xc0):
        mergedecodedata[i] = decodedata[i]
    for i in range(0xc0, dlength + 0xc0):
        mergedecodedata[i] = newdecodedata[i - 0xc0]

    # f = open('rep9rrr.txt', 'wb')
    # f.write(mergedecodedata)
    # f.close()

    decodedata = mergedecodedata

    date = decodedata[0xc4:0xc4 + 8]
    name = decodedata[0xcd:0xcd + 8]
    rank = decodedata[0xd7]
    mode = decodedata[0x1e4]+decodedata[0x1e5]

    rep_info['date'] = date.strip().decode()
    rep_info['player'] = name.strip().decode()
    chars = ("Reimu", "Marisa", "Sakuya", "Youmu", "Reisen", "Cirno", "Lyrica", "Mystia", "Tewi", "Yuka", "Aya", "Medicine", "Komachi", "Sikieiki", "Marlin", "Lunasa")
    levels = ("Easy", "Normal", "Hard", "Lunatic", "Extra")
    modes = ('Story Mode', 'Extra Mode', 'Human vs Human', 'Human vs Com', 'Com vs Human', 'Com vs Com')
    rep_info['base_info'] = f"{levels[rank]} {modes[mode]}"
    rep_info['base_infos'] = {
        "character": [],
        "shottype": "",
        "rank": levels[rank],
        "stage": modes[mode]
    }
    rep_info['slowrate'] = 0.000
    rep_info['stage_score'] = []
    rep_info['screen_action'] = []
    rep_info['keyboard_action'] = []

    is_match = (unsigned_int(decodedata, 0x44) != 0)

    stage_offsets = []

    if is_match:
        stage_start = unsigned_int(decodedata, 0x44)
        stage_end = unsigned_int(decodedata, 0x6c)
        stage_offsets.append(stage_start)
        stage_offsets.append(stage_end)
        rep_info['stage_score'].append(unsigned_int(decodedata, stage_start) * 10)
        character = f"{chars[decodedata[stage_start + 6]]} vs {chars[decodedata[stage_end + 6]]}"
        rep_info['base_info'] = "\n".join([rep_info['base_info'], character])
        rep_info['base_infos']['character'].append(character)
    else:
        stage_end = unsigned_int(decodedata, 0x48)

        for i in range(9):
            stage_offset = unsigned_int(decodedata, 0x20 + i * 0x4)
            if stage_offset != 0:
                rep_info['stage_score'].append(unsigned_int(decodedata, stage_offset) * 10)
                ai_stage_offset = unsigned_int(decodedata, 0x48 + i * 0x4)
                character = f"{chars[decodedata[stage_offset + 6]]} vs {chars[decodedata[ai_stage_offset + 6]]}"
                rep_info['base_info'] = "\n".join([rep_info['base_info'], character])
                rep_info['base_infos']['character'].append(character)
                stage_offsets.append(stage_offset)

        stage_offsets.append(stage_end)

    rep_info['z_frame'] = []
    rep_info['x_frame'] = []
    rep_info['c_frame'] = []
    rep_info['shift_frame'] = []

    total_frame_count=0

    for i in range(len(stage_offsets) - 1):
        start = stage_offsets[i] + 0x20
        frame = int((stage_offsets[i + 1] - stage_offsets[i] - 0x20) / 2)
        skey = []
        kkey = []
        for j in range(frame):
            if (j % 60 == 0):
                skey.append(f'[{(j // 60):<6}]')
            framekey = unsigned_int(decodedata, start + j * 2) >> 4 & 0xf
            skey.append(skeys[framekey])
            kkey.append(kkeys[framekey])
            if ((j + 1) % 60 == 0):
                rep_info['screen_action'].append(''.join(skey))
                rep_info['keyboard_action'].append(kkey)
                skey = []
                kkey = []
            total_frame_count += 1
            # 检测 z x c shift
            left_hand_flag = unsigned_int(decodedata, start + j * 2) & 0xf
            frame_dic = {
                1: 'z_frame',
                2: 'x_frame',
                4: 'shift_frame'
            }
            if left_hand_flag in frame_dic:
                rep_info[frame_dic[left_hand_flag]].append(total_frame_count)
        rep_info['screen_action'].append(''.join(skey))
        rep_info['keyboard_action'].append(kkey)

    rep_info['error'] = []

    rep_info['frame_count'] = total_frame_count

    rep_info['z_frame'] = filter_constant_frame(rep_info['z_frame'])
    rep_info['x_frame'] = filter_constant_frame(rep_info['x_frame'])
    rep_info['shift_frame'] = filter_constant_frame(rep_info['shift_frame'])

    return rep_info

#endregion

# 过滤按住的连续帧为按下帧
# 只用于shift z x
# 妖妖梦 永夜抄 花映冢
def filter_constant_frame(frame_list):
    result_frame_list=[]
    for i, frame in enumerate(frame_list):
        if i==0 or (frame!=frame_list[i-1]+1):
            result_frame_list.append(frame)
    return result_frame_list

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
    elif work=='95':
        character, ctype, rank, clear = th95type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='165':
        character, ctype, rank, clear = th165type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='17':
        character, ctype, rank, clear = th17type(info['character'], info['ctype'], info['rank'], info['clear'])
    elif work=='18':
        character, ctype, rank, clear = th18type(info['character'], info['ctype'], info['rank'], info['clear'])
    else:
        raise Exception(f"Unrecognized work {work}")

    output['base_info']=' '.join([character, ctype, rank, clear]).strip().replace("  ", " ")
    output['base_infos']={
        "character": character,
        "shottype": ctype,
        "rank": rank,
        "stage": clear
    }
    output['stage_score']=[]
    output['player']=info['player']
    output['slowrate'] = info['slowrate']
    output['date'] = info['date']
    output['error'] = info['error']

    # 辉针城单面帧数出错，然后因文件头转到神灵庙的bug
    # 由于转到神灵庙，clear情况会读取为0
    if info['clear'] == 0:
        # 加入新的error
        output['error'].append({'type': "DDC frame error"})

    for l in range(stage):
        output['stage_score'].append(info['stages'][l]['score']*work_attr[work]['score_rate'])

    output['screen_action']=[]
    output['keyboard_action']=[]

    output['z_frame'] = []
    output['x_frame'] = []
    output['c_frame'] = []
    output['shift_frame'] = []

    total_frame_count=0

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
                    skey.append(f'[{(i // 60):<6}]')
                framekey = unsigned_int(replaydata, i * 3) >> 3 & 0xf
                skey.append(skeys[framekey])
                kkey.append(kkeys[framekey])
                if ((i + 1) % 60 == 0):
                    output['screen_action'].append(''.join(skey))
                    output['keyboard_action'].append(kkey)
                    skey = []
                    kkey = []
                total_frame_count+=1
                # 检测 z x c shift
                left_hand_flag = unsigned_int(replaydata, i * 3) >> 8 & 0xf
                if left_hand_flag == 1:
                    output['z_frame'].append(total_frame_count)
                if left_hand_flag == 2:
                    output['x_frame'].append(total_frame_count)
                if left_hand_flag == 4:
                    output['shift_frame'].append(total_frame_count)
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
                    skey.append(f'[{(i // 60):<6}]')
                #print("stage", l, hex(i * 6))
                framekey = unsigned_int(replaydata, i * 6) >> 4 & 0xf
                skey.append(skeys[framekey])
                kkey.append(kkeys[framekey])
                if ((i + 1) % 60 == 0):
                    output['screen_action'].append(''.join(skey))
                    output['keyboard_action'].append(kkey)
                    skey = []
                    kkey = []
                total_frame_count+=1
                # 检测 z x c shift
                left_hand_flag = unsigned_int(replaydata, i * 6) >> 16 & 0xf
                c_flag = unsigned_int(replaydata, i * 6) >> 24 & 0xf
                # 文花帖
                if work == '95':
                    if left_hand_flag == 2:
                        output['z_frame'].append(total_frame_count)
                    if left_hand_flag == 1:
                        output['x_frame'].append(total_frame_count)
                    if left_hand_flag == 5:
                        output['shift_frame'].append(total_frame_count)
                else:
                    if left_hand_flag == 1:
                        output['z_frame'].append(total_frame_count)
                    if left_hand_flag == 2:
                        output['x_frame'].append(total_frame_count)
                    # 大战争
                    if work == '128':
                        if c_flag == 2:
                            output['c_frame'].append(total_frame_count)
                    # 神灵庙 辉针城 天邪鬼 绀珠传 天空璋
                    elif work == '13' or work == '14' or work == '143' or work == '15' or work == '16':
                        if c_flag == 10:
                            output['c_frame'].append(total_frame_count)
                    # 风神录
                    if work == '10':
                        if left_hand_flag == 4:
                            output['shift_frame'].append(total_frame_count)
                    else:
                        if left_hand_flag == 8:
                            output['shift_frame'].append(total_frame_count)
            output['screen_action'].append(''.join(skey))
            output['keyboard_action'].append(kkey)

    output['frame_count']=total_frame_count

    return output

def check_error(replay_info, error_str):
    return error_str in [error["type"] for error in replay_info["error"]]

# 根据长度获取正确的帧数
def true_frame(llength):
    frame = floor(llength / (6 + 1/30))
    if frame * 6 + ceil(frame / 30) == llength:
        return frame
    else:
        # 暴搜，，，
        for i in range(frame-10, frame+10):
            if i * 6 + ceil(i / 30) == llength:
                return i
        raise Exception("Cant correct the frame length")

def correct_true_frame(llength):
    try:
        return true_frame(llength)
    except:
        # 一直加65536，直到能够获取正确的帧数
        return correct_true_frame(llength + 65536)

def process_read_error(work, decodedata):
    # 解决th13和14文件头一样问题
    if work == '13':
        work = '14'
        try:
            return threp_output(threp_cut(decodedata, work), work)
        except:
            # 庙rep因长度错误被误转换到城
            work = '13'
            return threp_output(threp_cut(decodedata, work, True), work)
    elif work == '14':
        work = '13'
        # 解决辉针城单面长度出错再跳转问题
        try:
            replay_info2 = threp_output(threp_cut(decodedata, work), work)
            if check_error(replay_info2, "DDC frame error"):
                # 再次跳转，并强制保留单面frame长度
                work = '14'
                return threp_output(threp_cut(decodedata, work, True), work)
            # 出现单面长度错误且帧数过短，判断为矫正错误
            if check_error(replay_info2, "length read error") and replay_info2['frame_count'] < 54000:
                return threp_output(threp_cut(decodedata, work, True), work)
            return replay_info2
        except:
            # 庙rep因长度错误被误转换到城
            return threp_output(threp_cut(decodedata, work, True), work)
    else:
        try:
            # 尝试矫正frame长度重试
            return threp_output(threp_cut(decodedata, work, True), work)
        except:
            # 没救了，等死吧
            raise Exception("Failed to open replay file")

def load(file):
    try:
        file, buffer, flength = entry(file)
        decodedata, work = threp_decodedata(buffer)
        # 红魔乡/妖妖梦/永夜抄/花映冢
        if work in ['06', '07', '08', '09']:
            return decodedata
        replay_info = threp_output(threp_cut(decodedata, work), work)
        return replay_info if not replay_info['screen_action'] else process_read_error(work, decodedata)
    except:
        return process_read_error(work, decodedata)

