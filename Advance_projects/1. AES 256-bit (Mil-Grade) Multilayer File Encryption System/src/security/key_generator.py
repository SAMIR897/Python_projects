import hashlib

def generate_key(passwords, dialpad_counts):
    """Generate encryption key from 2-layer passwords."""
    pwd_str = "".join(passwords) + "".join(str(c) for c in dialpad_counts)
    return hashlib.sha256(pwd_str.encode()).digest()[:32]  # 256-bit key