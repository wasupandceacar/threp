from threp.static import types_dic

def raise_unrecog(type_, name):
    raise Exception(f"Unrecognized {type_} {name}")

def get_alltypes(work, character, ctype, rank, clear):
    if work not in types_dic:
        raise Exception(f"Unrecognized work {work}")
    dic = types_dic[work]
    res = []
    for attr_str, attr in dict(character=character, ctype=ctype, rank=rank, clear=clear).items():
        if not dic[attr_str]:
            res.append("")
            continue
        if attr > len(dic[attr_str]) - 1:
            raise_unrecog(attr_str, attr)
        res.append(dic[attr_str][attr])
    return res

def format_types(work, character, ctype, rank, clear):
    if work in ["95", "125", "143"]:
        return ' '.join([character, f"{ctype}-{rank}", clear]).strip().replace("  ", " ")
    if work in ["165"]:
        return ' '.join([character, f"{rank}-{ctype}", clear]).strip().replace("  ", " ")
    return ' '.join([character, ctype, rank, clear]).strip().replace("  ", " ")
