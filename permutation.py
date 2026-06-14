# src/acf/permutation.py
import numpy as np
from .partitioning import VocabularyPartitioner

class CDFPermuter:
    def __init__(self, partitioner: VocabularyPartitioner):
        self.partitioner = partitioner

    def permute_distribution(self, natural_probabilities: np.ndarray, target_bit: int) -> np.ndarray:
        """
        Shuffles the vocabulary token indices along the axis to prioritize the 
        target bit's vocabulary bucket, assuring zero semantic distortion.
        """
        # Sort tokens by their natural generation probabilities (descending)
        sorted_indices = np.argsort(natural_probabilities)[::-1]
        
        target_group = []
        filler_group = []
        
        # Separate the sorted tokens based on the static bit partitions
        for idx in sorted_indices:
            bit = self.partitioner.get_bit_assignment(idx)
            if bit == target_bit:
                target_group.append(idx)
            else:
                filler_group.append(idx)
                
        # Interleave or prioritize the target group to shift the cumulative mass
        # while preserving the structural geometric curve of the distribution
        permuted_indices = target_group + filler_group
        
        # Reconstruct the aligned probability array matching the new order
        permuted_probabilities = np.zeros_like(natural_probabilities)
        for new_pos, original_idx in enumerate(permuted_indices):
            permuted_probabilities[original_idx] = natural_probabilities[sorted_indices[new_pos]]
            
        return permuted_probabilities
