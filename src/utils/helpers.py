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

def emoticate(value: str, is_number: bool = False) -> str:
    if is_number and value.isdigit():
        emoji_digits = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
        return ''.join(emoji_digits[int(digit)] for digit in value)
    
    if isinstance(value, bool):
        return '✅' if value else '❌'
    
    return '❌'