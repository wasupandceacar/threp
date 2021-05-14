from struct import unpack

def unsigned_int(_bytes, pointer):
    return unpack('I', _bytes[pointer:pointer + 4])[0]

def unsigned_char(_bytes, pointer):
    return unpack('B', _bytes[pointer:pointer + 1])[0]

def float(_bytes, pointer):
    return unpack('f', _bytes[pointer:pointer + 4])[0]

def bin32(num):
    return f'{bin(num)[2:]:>32}'.replace(' ', '0')

def bin16(num):
    return f'{bin(num)[2:]:>16}'.replace(' ', '0')

class Ref(object):
    pass