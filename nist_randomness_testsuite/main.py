import random
import pandas as pd
from Crypto.Cipher import DES, Blowfish, ARC4
from Crypto.Random import get_random_bytes

# Import your NIST feature modules
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

TARGET_LEN = 512  # Must be multiple of 8 for DES/Blowfish

def pad_or_truncate(data, length=TARGET_LEN):
    if len(data) >= length:
        return data[:length]
    return data + b'\x00'*(length - len(data))

def generate_sample(algorithm="DES"):
    pt = get_random_bytes(TARGET_LEN)

    if algorithm == "DES":
        key = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_ECB)
        ct = cipher.encrypt(pt)
        label = "DES"

    elif algorithm == "Blowfish":
        key = get_random_bytes(16)
        cipher = Blowfish.new(key, Blowfish.MODE_ECB)
        ct = cipher.encrypt(pt)
        label = "Blowfish"

    elif algorithm == "RC4":
        key = get_random_bytes(16)
        cipher = ARC4.new(key)
        ct = cipher.encrypt(pt)
        label = "RC4"

    else:
        raise ValueError(f"Unsupported algorithm: {algorithm}")

    ct_fixed = pad_or_truncate(ct)
    return pt, ct_fixed, label

def bytes_to_bin(data_bytes):
    return ''.join(format(b, '08b') for b in data_bytes)

# Prepare dataset
samples_per_algo = 5
algorithms = ["DES", "Blowfish", "RC4"]
dataset = []

for algo in algorithms:
    for _ in range(samples_per_algo):
        pt, ct, label = generate_sample(algo)
        ct_bin = bytes_to_bin(ct)[:1000000]  # limit to 1 million bits

        # Compute NIST features (take only p-values)
        features = {}
        features['freq'] = float(FrequencyTest.monobit_test(ct_bin)[0])
        features['block_freq'] = float(FrequencyTest.block_frequency(ct_bin)[0])
        features['runs'] = float(RunTest.run_test(ct_bin)[0])
        features['longest_one'] = float(RunTest.longest_one_block_test(ct_bin)[0])
        features['matrix_rank'] = float(Matrix.binary_matrix_rank_text(ct_bin)[0])
        features['spectral'] = float(SpectralTest.spectral_test(ct_bin)[0])
        features['template_non_overlap'] = float(TemplateMatching.non_overlapping_test(ct_bin, '000000001')[0])
        features['template_overlap'] = float(TemplateMatching.overlapping_patterns(ct_bin)[0])
        features['universal'] = float(Universal.statistical_test(ct_bin)[0])
        features['linear_complexity'] = float(ComplexityTest.linear_complexity_test(ct_bin)[0])
        features['serial'] = float(Serial.serial_test(ct_bin)[0][0])
        features['approx_entropy'] = float(ApproximateEntropy.approximate_entropy_test(ct_bin)[0])
        features['cumsum_forward'] = float(CumulativeSums.cumulative_sums_test(ct_bin, 0)[0])
        features['cumsum_backward'] = float(CumulativeSums.cumulative_sums_test(ct_bin, 1)[0])

        # Random Excursions features
        re_vals = RandomExcursions.random_excursions_test(ct_bin)
        features['random_excursions'] = sum([float(v[0]) for v in re_vals if isinstance(v, (tuple, list)) and v[0] not in (None, '')])

        rv_vals = RandomExcursions.variant_test(ct_bin)
        features['random_excursion_variant'] = sum([float(v[0]) for v in rv_vals if isinstance(v, (tuple, list)) and v[0] not in (None, '')])



        # Add row
        dataset.append({
            'plain_text': pt.hex(),
            'cipher_text': ct.hex(),
            'algo': label,
            **features
        })

# Create DataFrame and save CSV
df = pd.DataFrame(dataset)
df.to_csv("nist_dataset.csv", index=False)
print("CSV saved as nist_dataset.csv")
