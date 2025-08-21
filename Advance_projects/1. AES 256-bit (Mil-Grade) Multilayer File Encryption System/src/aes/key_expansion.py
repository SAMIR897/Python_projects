from .constants import RCON

def key_expansion(key):
    """Expand a 256-bit key into 60 32-bit words for 14 rounds."""
    key_words = [int.from_bytes(key[i:i+4], 'big') for i in range(0, 32, 4)]
    expanded = key_words.copy()
    for i in range(8, 60):
        temp = expanded[i-1]
        if i % 8 == 0:
            temp = (temp << 8) ^ (temp >> 24) ^ RCON[i//8 - 1] ^ expanded[i-8]
        expanded.append(expanded[i-8] ^ temp)
    return expanded