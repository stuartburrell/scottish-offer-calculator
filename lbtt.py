import numpy as np


def generate_cached_tax_array(ftb: bool, upper_tax_threshold: int) -> np.array:
    if ftb:
        first_threshold = 175_000
    else:
        first_threshold = 145_000

    second_threshold = 250_000
    third_threshold = 325_000
    tax_array = np.zeros(upper_tax_threshold)
    tax_array[:first_threshold] = 0.0
    tax_array[first_threshold:second_threshold] = 0.02
    tax_array[second_threshold:third_threshold] = 0.05
    tax_array[third_threshold:] = 0.10
    return np.cumsum(tax_array)


UPPER_TAX_THRESHOLD = 750_000
FTB_LBTT_CACHE = generate_cached_tax_array(
    ftb=True, upper_tax_threshold=UPPER_TAX_THRESHOLD
)
STANDARD_LBTT_CACHE = generate_cached_tax_array(
    ftb=False, upper_tax_threshold=UPPER_TAX_THRESHOLD
)


def compute_lbtt(offer: float, ftb: bool = False):
    if ftb:
        return round(
            FTB_LBTT_CACHE[min(offer - 1, 749_999)] + max(offer - 750_000, 0) * 0.12
        )
    else:
        return round(
            STANDARD_LBTT_CACHE[min(offer - 1, 749_999)]
            + max(offer - 750_000, 0) * 0.12
        )
