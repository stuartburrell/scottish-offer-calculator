import numpy as np


def generate_cached_tax_array(ftb: bool, cache_size: int) -> np.array:
    if ftb:
        first_threshold = 175_000
    else:
        first_threshold = 145_000

    second_threshold = 250_000
    third_threshold = 325_000
    fourth_threshold = 750_000

    tax_array = np.zeros(cache_size)
    tax_array[:first_threshold] = 0.0
    tax_array[first_threshold:second_threshold] = 0.02
    tax_array[second_threshold:third_threshold] = 0.05
    tax_array[third_threshold:fourth_threshold] = 0.10
    tax_array[fourth_threshold:] = 0.12
    return tax_array


CACHE_SIZE = 5_000_000
STANDARD_TAX_ARRAY = generate_cached_tax_array(ftb=False, cache_size=CACHE_SIZE)
FTB_TAX_ARRAY = generate_cached_tax_array(ftb=True, cache_size=CACHE_SIZE)


def compute_lbtt_slow(offer: float, ftb: bool = False):
    total_tax = 0.0
    if ftb:
        first_threshold = 175_000
    else:
        first_threshold = 145_000
    for pound in range(1, offer + 1):
        if pound <= first_threshold:
            total_tax += 0
        elif pound <= 250_000:
            total_tax += 0.02
        elif pound <= 325_000:
            total_tax += 0.05
        elif pound <= 750_000:
            total_tax += 0.10
        else:
            total_tax += 0.12
    return round(total_tax)


def compute_lbtt(offer: float, ftb: bool = False):
    if offer > CACHE_SIZE:
        return compute_lbtt_slow(offer, ftb=ftb)
    if ftb:
        return round(np.sum(FTB_TAX_ARRAY[:offer]))
    else:
        return round(np.sum(STANDARD_TAX_ARRAY[:offer]))
