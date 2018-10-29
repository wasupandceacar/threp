from .static import dzz_attr
from .static import week_array

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
        clear_s = "stage "+str(clear)
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
        clear_s = "stage "+str(clear)
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
        clear_s = "stage "+str(clear)
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
    elif rank == 5:
        rank_s = 'overdrive'
    else:
        raise Exception("Unrecognized rank {}".format(rank))
    if clear == 8:
        clear_s = 'all'
    elif clear == 7:
        clear_s = 'extra'
    else:
        clear_s = "stage "+str(clear)
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
        clear_s = "stage "+str(clear)
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
        clear_s = "stage "+str(clear)
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
        clear_s = "stage "+str(clear)
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

def th125type(character, ctype, rank, clear):
    if character == 0:
        character_s = 'Aya'
    elif character == 1:
        character_s = 'Hatate'
    else:
        raise Exception("Unrecognized character {}".format(character))
    if ctype == 12:
        rank_s = 'EX-'
    elif ctype == 13:
        rank_s = 'SP-'
    elif ctype >= 0 and ctype <= 11:
        rank_s = str(ctype+1) + "-"
    else:
        raise Exception("Unrecognized ctype {}".format(ctype))
    rank_s+=str(rank+1)
    return character_s, "", rank_s, ""

def th143type(character, ctype, rank, clear):
    if ctype >= 0 and ctype <= 10:
        rank_s = str(ctype+1) + "-"
    else:
        raise Exception("Unrecognized ctype {}".format(ctype))
    rank_s+=str(rank+1)
    return "", "", rank_s, ""

def th95type(character, ctype, rank, clear):
    if ctype == 10:
        rank_s = 'EX-'
    elif ctype >= 0 and ctype <= 9:
        rank_s = str(ctype+1) + "-"
    else:
        raise Exception("Unrecognized ctype {}".format(ctype))
    rank_s+=str(rank+1)
    return "", "", rank_s, ""

def th165type(character, ctype, rank, clear):
    if 0 <= rank and rank <= 6:
        rank_s = ""
    elif 7 <= rank and rank <= 13:
        rank_s = 'Inner-'
    elif 14 <= rank and rank <= 20:
        rank_s = 'Nightmare-'
    else:
        raise Exception("Unrecognize ctype {}".format(ctype))
    return "Usami", "", rank_s + week_array[rank % 7] + "-" + str(ctype+1), ""