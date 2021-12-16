from struct import unpack
from math import ceil, floor
from threp.static import frame_search_range, frame_correct_retry

def unsigned_int(_bytes, pointer):
    return unpack('I', _bytes[pointer:pointer + 4])[0]

def unsigned_char(_bytes, pointer):
    return unpack('B', _bytes[pointer:pointer + 1])[0]

def float_(_bytes, pointer):
    return unpack('f', _bytes[pointer:pointer + 4])[0]

def bin32(num):
    return f'{bin(num)[2:]:>32}'.replace(' ', '0')

def bin16(num):
    return f'{bin(num)[2:]:>16}'.replace(' ', '0')

class Ref(object):
    pass

def entry(file):
    buffer = bytearray(0x100000)
    with open(file, 'rb') as f:
        _buffer = f.read()
    flength = len(_buffer)
    buffer[:flength] = _buffer
    return buffer

# 过滤按住的连续帧为按下帧
# 只用于shift z x
# 妖妖梦 永夜抄 花映冢
def filter_constant_frame(frame_list):
    result_frame_list = []
    for i, frame in enumerate(frame_list):
        if i == 0 or (frame != frame_list[i-1]+1):
            result_frame_list.append(frame)
    return result_frame_list

# 根据长度获取正确的帧数
def true_frame(llength):
    frame = floor(llength / (6 + 1/30))
    if frame * 6 + ceil(frame / 30) == llength:
        return frame
    # 暴搜，，，
    for i in range(frame - frame_search_range, frame + frame_search_range):
        if i * 6 + ceil(i / 30) == llength:
            return i
    raise Exception("Can't correct the frame length")

def correct_true_frame(llength):
    for _ in range(frame_correct_retry):
        try:
            return true_frame(llength)
        except Exception:
            # 一直加65536，直到能够获取正确的帧数
            llength += 65536