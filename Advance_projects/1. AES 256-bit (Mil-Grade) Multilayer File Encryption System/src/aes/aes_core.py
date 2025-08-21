from .constants import SBOX, MIX_COLUMNS_MATRIX
from .utils import gf_multiply, pad
from .key_expansion import key_expansion

def sub_bytes(state):
    return [[SBOX[state[i][j]] for j in range(4)] for i in range(4)]

def shift_rows(state):
    return [state[0], [state[1][1], state[1][2], state[1][3], state[1][0]],
            [state[2][2], state[2][3], state[2][0], state[2][1]],
            [state[3][3], state[3][0], state[3][1], state[3][2]]]

def mix_columns(state):
    result = [[0 for _ in range(4)] for _ in range(4)]
    for c in range(4):
        for r in range(4):
            for k in range(4):
                result[r][c] ^= gf_multiply(MIX_COLUMNS_MATRIX[r][k], state[k][c])
    return result

def add_round_key(state, round_key):
    return [[state[i][j] ^ round_key[i][j] for j in range(4)] for i in range(4)]

def aes_encrypt(plaintext, key):
    state = [list(plaintext[i:i+4]) for i in range(0, 16, 4)]
    round_keys = key_expansion(key)
    state = add_round_key(state, [round_keys[i:i+4] for i in range(0, 16, 4)])
    for round_num in range(1, 14):
        state = sub_bytes(state)
        state = shift_rows(state)
        if round_num < 13:
            state = mix_columns(state)
        state = add_round_key(state, [round_keys[16 + round_num*4 : 16 + (round_num+1)*4]])
    return b''.join(bytes(s) for s in state)