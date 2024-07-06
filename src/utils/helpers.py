import psutil

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

def format_large_num(num):
    suffixes = ['', 'K', 'M', 'B', 'T', 'Q', 'QQ']

    if num == 0:
        return '0'

    abs_num = abs(num)
    magnitude = 0

    while abs_num >= 1000 and magnitude < len(suffixes) - 1:
        abs_num /= 1000
        magnitude += 1

    formatted_num = '{:.2f}'.format(abs_num).rstrip('0').rstrip('.')

    return '{} {}'.format(formatted_num, suffixes[magnitude])

def get_server_usage():
    memory      = psutil.virtual_memory()
    mem_usage   = memory.used / 1e6
    mem_total   = memory.total / 1e6
    mem_percent = memory.percent
    cpu_percent = psutil.cpu_percent()
    
    return {
        'memory_usage_MB': mem_usage,
        'memory_total_MB': mem_total,
        'memory_percent' : mem_percent,
        'cpu_percent'    : cpu_percent
    }

def camel2space(string):
    return ''.join(map(lambda x: x if x.islower() else " " + x, string))