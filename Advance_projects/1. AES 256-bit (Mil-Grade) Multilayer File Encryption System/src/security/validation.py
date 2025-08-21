def validate_passwords(passwords):
    return len(passwords) == 4 and all(p for p in passwords)

def validate_dialpad(counts):
    return len(counts) == 3 and all(c > 0 for c in counts) and bin(sum(counts) & 0xFF) != "0b0"