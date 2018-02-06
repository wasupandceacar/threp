from struct import unpack

def unsigned_int(_bytes, pointer):
    return unpack('I', _bytes[pointer:pointer + 4])[0]


def unsigned_char(_bytes, pointer):
    return unpack('B', _bytes[pointer:pointer + 1])[0]


def signed_int(_bytes, pointer):
    return unpack('i', _bytes[pointer:pointer + 4])[0]


def bin32(num):
    return '{0:>32}'.format(bin(num)[2:]).replace(' ', '0')


def bin8(num):
    return '{0:>8}'.format(bin(num)[2:]).replace(' ', '0')


def bin16(num):
    return '{0:>16}'.format(bin(num)[2:]).replace(' ', '0')


class Ref(object):
    pass

def diff2(s1, s2):
    import difflib
    matcher = difflib.SequenceMatcher(None, s1, s2)
    rl = []
    for tag, i1, i2, j1, j2 in reversed(matcher.get_opcodes()):
        if tag == 'delete':
            rl = ['[-'] + s1[i1:i2] + ['-]'] + rl
            del s1[i1:i2]
        elif tag == 'equal':
            rl = s1[i1:i2] + rl
        elif tag == 'insert':
            rl = ['[+'] + s2[j1:j2] + ['+]'] + rl
            s1[i1:i2] = s2[j1:j2]
        elif tag == 'replace':
            rl = ['['] + s1[i1:i2] + ['->'] + s2[j1:j2] + [']'] + rl
            s1[i1:i2] = s2[j1:j2]
    return rl

def find_last_true(l, pred):
    assert pred(l[0])
    left = 0
    right = len(l)
    while right - left >= 2:
        check = left + (right - left) // 2
        if pred(l[check]):
            left = check
        else:
            right = check
    return right if pred(right) else left

def find_last_match(seq1, seq2):
    pred = lambda cut: seq1[:cut] == seq2[:cut]
    length = min(len(seq1), len(seq2))
    return find_last_true(list(range(length)), pred)

def replay_to_binary_seq(replay):
    assert len(replay) % 6 == 0
    frame = len(replay) // 6
    l = []
    for i in range(frame):
        n1, n2 = unpack('IH', replay[i * 6:(i + 1) * 6])
        l.append(bin32(n1) + bin16(n2))
    return l