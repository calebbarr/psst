def tail(_list):
    return _list if len(_list) == 0 else _list[1:]

def head(_list):
    return _list[0] if len(_list) > 0 else None

def drop(_list,n):
    return [] if n > len(_list) else _list[n:]

def dropright(_list,n):
    return [] if n > len(_list) else _list[:-n]