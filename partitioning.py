# src/acf/partitioning.py
import random
import hashlib

class VocabularyPartitioner:
    def __init__(self, shared_seed: str, vocab_size: int = 32000):
        """
        Initializes the partitioner using a shared mathematical constant.
        Bypasses cognitive asymmetry by keeping the partition entirely 
        independent of dynamic context windows.
        """
        self.vocab_size = vocab_size
        self.vocab = list(range(vocab_size))
        
        # Derive a deterministic integer seed from the text constant
        hashed = hashlib.sha256(shared_seed.encode('utf-8')).digest()
        self.seed_int = int.from_bytes(hashed, byteorder='big') % (2**32)
        
        self.v_0, self.v_1 = self._generate_static_partitions()

    def _generate_static_partitions(self):
        """Slices the vocabulary into two disjoint, pseudo-random sets."""
        rng = random.Random(self.seed_int)
        shuffled_vocab = list(self.vocab)
        rng.shuffle(shuffled_vocab)
        
        midpoint = self.vocab_size // 2
        v_0 = set(shuffled_vocab[:midpoint])
        v_1 = set(shuffled_vocab[midpoint:])
        return v_0, v_1

    def get_bit_assignment(self, token_id: int) -> int:
        """Determines if a given token belongs to the 0 or 1 bucket."""
        if token_id in self.v_1:
            return 1
        return 0
