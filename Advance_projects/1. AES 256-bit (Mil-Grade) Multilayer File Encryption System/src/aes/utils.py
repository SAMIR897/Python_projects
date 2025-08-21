def gf_multiply(a, b):
    """Multiply two numbers in GF(2^8) with polynomial reduction."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= 0x1B  # Polynomial x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return p & 0xFF

def pad(data):
    """PKCS7 padding for 16-byte blocks."""
    pad_len = 16 - (len(data) % 16)
    return data + bytes([pad_len] * pad_len)