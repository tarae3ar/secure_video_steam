(function exposeCipher(root) {
  "use strict";
  const LFSR_PERIOD_BITS = 0xffff;

  function nextBit(state) {
    // TODO(student 4): replace this reference state transition in the handout.
    
    const output = state & 1;

   const bit0 = (state >> 0) & 1;
   const bit2 = (state >> 2) & 1;
   const bit3 = (state >> 3) & 1;
   const bit5 = (state >> 5) & 1;

   const feedback = bit0 ^ bit2 ^ bit3 ^ bit5;

   const shiftedState = state >> 1;

   const nextState = shiftedState | (feedback << 15);

   return [output, nextState];
    
  }

  function keystream(length, seed, offset = 0) {
    if (!Number.isInteger(seed) || seed < 1 || seed > 0xffff) throw new RangeError("invalid seed");
    if (!Number.isInteger(length) || length < 0 || !Number.isInteger(offset) || offset < 0) {
      throw new RangeError("invalid length or offset");
    }
    // TODO(student 5): replace this reference generator in the handout.
    
   let state = seed;

   // Skip bits based on offset
   const skipBits = (offset * 8) % LFSR_PERIOD_BITS;

   for (let i = 0; i < skipBits; i++) {
     const [bit, nextState] = nextBit(state);
     state = nextState;
   }

   // Create output bytes
   const result = new Uint8Array(length);

    for (let i = 0; i < length; i++) {
     let value = 0;

     for (let j = 0; j < 8; j++) {
        const [bit, nextState] = nextBit(state);
        state = nextState;
        value = (value << 1) | bit;
      }

     result[i] = value;
   }

   return result;

  }

  function xorBytes(data, seed, offset = 0) {
    
    // TODO(student 6): replace this reference XOR operation in the handout.
    const key = keystream(data.length, seed, offset);

   const result = new Uint8Array(data.length);

   for (let i = 0; i < data.length; i++) {
      result[i] = data[i] ^ key[i];
   }

   return result;
   }

  const cipher = { keystream, xorBytes };
  root.LfsrCipher = cipher;
  if (typeof module !== "undefined") module.exports = cipher;
}(typeof self !== "undefined" ? self : globalThis));
