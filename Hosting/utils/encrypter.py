line = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
num_chars = len(line)

def get_number(ch: str) -> int:
    if len(ch) != 1:
        raise ValueError("Character length must be 1!")
    if type(ch) != str:
        raise ValueError("Character must be string!")
    return line.index(ch)

def get_char(num: int):
    if 0 <= num <= num_chars:
        return line[num]
    raise ValueError(f"Number must be between 0 and {num_chars}")