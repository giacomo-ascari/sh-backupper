def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[39m".format(r, g, b, text)

def log(head, body, obj=None):
    h = hash(head)
    r, g, b = int(h%256), int(h/10**3%256), int(h/10**6%256)
    head_len = len(head)+2
    print(colored(r, g, b, "[" + head.upper() + "]"), body)
    if obj:
        print(" "*(head_len), obj)