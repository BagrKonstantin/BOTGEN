line = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ".lower()
num_chars = len(line)

def get_number(ch: str) -> int:
    if len(ch) != 1:
        raise ValueError("Character length must be 1!")
    if '0' <= ch <= '9':
        return ord(ch) - ord('0')
    elif 'a' <= ch <= 'z':
        return ord(ch) - ord('a') + 10
    else:
        raise ValueError(f"Character must be ASCII 0-9, a-z, got '{ch}'")

def get_char(num: int):
    if 0 <= num <= num_chars:
        return line[num]
    raise ValueError(f"Number must be between 0 and {num_chars}")