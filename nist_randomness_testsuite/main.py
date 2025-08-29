import os
from FrequencyTest import FrequencyTest
from RunTest import RunTest
from Matrix import Matrix
from Spectral import SpectralTest
from TemplateMatching import TemplateMatching
from Universal import Universal
from Complexity import ComplexityTest
from Serial import Serial
from ApproximateEntropy import ApproximateEntropy
from CumulativeSum import CumulativeSums
from RandomExcursions import RandomExcursions

# Example: your ciphertext as a binary string
ciphertext_binary = '110010101011001010'  # replace with your ciphertext

# Limit to first 1 million bits if very long
data = ciphertext_binary[:1000000]

# Run tests
print('Frequency Test:', FrequencyTest.monobit_test(data))
print('Block Frequency Test:', FrequencyTest.block_frequency(data))
print('Runs Test:', RunTest.run_test(data))
print('Longest Run of Ones Test:', RunTest.longest_one_block_test(data))
print('Binary Matrix Rank Test:', Matrix.binary_matrix_rank_text(data))
print('Spectral (DFT) Test:', SpectralTest.spectral_test(data))
print('Non-overlapping Template Matching Test:', TemplateMatching.non_overlapping_test(data, '000000001'))
print('Overlapping Template Matching Test:', TemplateMatching.overlapping_patterns(data))
print('Universal Statistical Test:', Universal.statistical_test(data))
print('Linear Complexity Test:', ComplexityTest.linear_complexity_test(data))
print('Serial Test:', Serial.serial_test(data))
print('Approximate Entropy Test:', ApproximateEntropy.approximate_entropy_test(data))
print('Cumulative Sums Test (Forward):', CumulativeSums.cumulative_sums_test(data, 0))
print('Cumulative Sums Test (Backward):', CumulativeSums.cumulative_sums_test(data, 1))

# Random Excursions Tests
result_excursions = RandomExcursions.random_excursions_test(data)
print('Random Excursions Test:')
for item in result_excursions:
    print(item)

result_variant = RandomExcursions.variant_test(data)
print('Random Excursion Variant Test:')
for item in result_variant:
    print(item)
