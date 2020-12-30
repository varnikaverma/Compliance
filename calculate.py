from fuzzywuzzy import fuzz

def get_ratio(n, m):
    r = fuzz.token_set_ratio(n, m)
    if r == 100:
        return 1
    else:
        return 0

def count(nn, mm):
    c = len(nn.split())
    c1 = len(mm.split())
    return c, c1