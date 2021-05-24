from threp.utils import Ref

def get_bit(buffer, ref_pointer, ref_filter, length):
    result = 0
    current = buffer[ref_pointer.value]
    for i in range(length):
        result <<= 1
        if current & ref_filter.value:
            result |= 0x1
        ref_filter.value >>= 1
        if ref_filter.value == 0:
            ref_pointer.value += 1
            current = buffer[ref_pointer.value]
            ref_filter.value = 0x80
    return result

def decompress(buffer, decode, length):
    ref_pointer = Ref()
    ref_pointer.value = 0
    ref_filter = Ref()
    ref_filter.value = 0x80
    dest = 0
    dict = [0 for i in range(0x2010)]
    while ref_pointer.value < length:
        bits = get_bit(buffer, ref_pointer, ref_filter, 1)
        if ref_pointer.value >= length:
            return dest
        if bits:
            bits = get_bit(buffer, ref_pointer, ref_filter, 8)
            if ref_pointer.value >= length:
                return dest
            decode[dest] = bits
            dict[dest & 0x1fff] = bits
            dest += 1
        else:
            bits = get_bit(buffer, ref_pointer, ref_filter, 13)
            if ref_pointer.value >= length:
                return dest
            index = bits - 1
            bits = get_bit(buffer, ref_pointer, ref_filter, 4)
            if ref_pointer.value >= length:
                return dest
            bits += 3
            for i in range(bits):
                dict[dest & 0x1fff] = dict[index + i]
                decode[dest] = dict[index + i]
                dest += 1
    return dest

def decode(buffer, length, block_size, base, add):
    assert isinstance(buffer, bytearray)
    tbuf = buffer.copy()
    p = 0
    left = length
    if left % block_size < block_size // 4:
        left -= left % block_size
    left -= length & 1
    while left:
        if left < block_size:
            block_size = left
        tp1 = p + block_size - 1
        tp2 = p + block_size - 2
        hf = (block_size + (block_size & 0x1)) // 2
        for i in range(hf):
            buffer[tp1] = tbuf[p] ^ base
            base = (base + add) % 0x100
            tp1 -= 2
            p += 1
        hf = block_size // 2
        for i in range(hf):
            buffer[tp2] = tbuf[p] ^ base
            base = (base + add) % 0x100
            tp2 -= 2
            p += 1
        left -= block_size

def entry(file):
    buffer = bytearray(0x100000)
    with open(file, 'rb') as f:
        _buffer = f.read()
    flength = len(_buffer)
    buffer[:flength] = _buffer
    return file, buffer, flength