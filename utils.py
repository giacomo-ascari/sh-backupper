def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[39m".format(r, g, b, text)

def heighten(a, b, c):
    if a > max(b, c):
        a = 255
    elif b > max(a, c):
        b = 255
    else:
        c = 255
    return a, b, c

def log(head, body, obj=None):
    h = hash(head)
    r, g, b = int(h%256), int(h/10**3%256), int(h/10**6%256)
    r, g, b = heighten(r, g, b)
    head_len = len(head)+2
    print(colored(r, g, b, "[" + head.upper() + "]"), body)
    if obj:
        print(" "*(head_len), obj)