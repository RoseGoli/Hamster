def align(args:dict, prefix:str='<code>', suffix:str='</code>', sep:str=' : ') -> str:
    [result, maxLength] = ['', 0]

    for key, value in args.items():
        if (len(key) > maxLength):
            maxLength = len(key)

    for key, value in args.items():
        result += prefix + str(key).ljust(maxLength) + sep + suffix + str(value) + "\n"

    return rtl(result)

def rtl(string):
    return f"{string}\u200f"