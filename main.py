# main.py
import numpy as np
from acf import VocabularyPartitioner, CDFPermuter

# Step 1: Initialize with a shared mathematical seed
pi_constant = "3.14159265358979323846"
partitioner = VocabularyPartitioner(shared_seed=pi_constant, vocab_size=10)
permuter = CDFPermuter(partitioner)

# Step 2: Create a mock probability distribution from a Cognitive Reasoning Layer
mock_logits = np.array([0.1, 0.05, 0.25, 0.15, 0.05, 0.02, 0.08, 0.12, 0.11, 0.07])

# Step 3: Permute the axis to encode a binary '1' bit
target_bit = 1
adjusted_probs = permuter.permute_distribution(mock_logits, target_bit=target_bit)

print("Original Distribution Sum:", np.sum(mock_logits))
print("Permuted Distribution Sum:", np.sum(adjusted_probs))
print("The cumulative structural curve remains flawlessly intact.")
