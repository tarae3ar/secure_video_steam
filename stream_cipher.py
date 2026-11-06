"""Small, deliberately insecure LFSR stream cipher for teaching."""

MAX_SEED = 0xFFFF
LFSR_PERIOD_BITS = 0xFFFF


def _validate_seed(seed: int) -> None:
    if not isinstance(seed, int) or not 1 <= seed <= MAX_SEED:
        raise ValueError("seed must be an integer from 1 to 65535")


def _next_bit(state: int) -> tuple[int, int]:
    """Return output bit and next state for x^16 + x^14 + x^13 + x^11 + 1."""
    # TODO(student 1): replace this reference state transition in the handout.

    output = state & 1
   # extract feedback bits
    bit0 = (state >> 0) & 1
    bit2 = (state >> 2) & 1
    bit3 = (state >> 3) & 1
    bit5 = (state >> 5) & 1

    feedback = bit0 ^ bit2 ^ bit3 ^ bit5
    # Shift register right
    shifted_state = state >> 1
    # Insert feedback at bit 15
    next_state = shifted_state | (feedback << 15)
    return output, next_state


def keystream(length: int, seed: int, offset: int = 0) -> bytes:
    """Return length keystream bytes, starting at an absolute byte offset."""
    _validate_seed(seed)
    if not isinstance(length, int) or length < 0:
        raise ValueError("length must be a non-negative integer")
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("offset must be a non-negative integer")

    # TODO(student 2): replace this reference generator in the handout.
    # initial state
    state = seed

    # Skip bytes before the requested offset
    skip_bits = (offset * 8) % LFSR_PERIOD_BITS

    for _ in range(skip_bits):
        _, state = _next_bit(state)

    #create the output
    result = bytearray()

    for _ in range(length):
        value = 0

        for _ in range(8):
            bit, state = _next_bit(state)
            value = (value << 1) | bit

        result.append(value)

    return bytes(result)



def xor_bytes(data: bytes, seed: int, offset: int = 0) -> bytes:
    """Encrypt or decrypt data with the keystream at absolute byte offset."""
    # TODO(student 3): replace this reference XOR operation in the handout.
    key = keystream(len(data), seed, offset)

    result = bytearray()

    for i in range(len(data)):
        encrypted_byte = data[i] ^ key[i]
        result.append(encrypted_byte)

    return bytes(result)
