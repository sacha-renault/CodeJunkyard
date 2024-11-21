import random
import numpy as np
from numba import njit

# Define the Numba-compatible structured type for Pair
pair_type = np.dtype([('x', np.int32), ('y', np.int32)])

@njit
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

@njit
def search_pairs(n: int, num: int, p: int, q: int, depth: int):
    max_pairs = 1000  # Adjust based on expected data
    pairs = np.zeros(max_pairs, dtype=pair_type)
    pair_count = 0

    for x in range(0, 10):
        new_p = (x * 10**depth + p)
        if new_p * 10 > n:
            break

        for y in range(0, 10):
            new_q = (y * 10**depth + q)
            product = new_p * new_q
            if product > n:
                break
            if product == num or product % (10 ** len(str(num))) == num:
                if pair_count < max_pairs:
                    pairs[pair_count]['x'] = new_p
                    pairs[pair_count]['y'] = new_q
                    pair_count += 1

    return pairs[:pair_count]

@njit
def extract_last_digits(n: int, digits: int) -> int:
    """
    Extract the last `digits` number of digits from the integer `n`.

    Parameters:
    - n: The integer to extract digits from.
    - digits: Number of digits to extract.

    Returns:
    - The last `digits` digits of `n`.
    """
    return n % (10 ** digits)

@njit
def recursive_search(n: int, factor_q: int, factor_p: int, depth: int) -> tuple[int, int] | None:
    partial_n = extract_last_digits(n, depth + 1)

    if partial_n != 0:
        pairs = search_pairs(n, partial_n, factor_p, factor_q, depth)
        for i in range(len(pairs)):
            potential_p = pairs[i]['x']
            potential_q = pairs[i]['y']

            if (potential_p * potential_q == n and
                potential_p != 1 and potential_q != 1 and
                is_prime(potential_p) and is_prime(potential_q)):
                return potential_p, potential_q
            elif potential_p * potential_q < n:
                result = recursive_search(n, potential_q, potential_p, depth + 1)
                if result is not None:
                    return result
    return None

@njit
def find_prime_factors(n: int) -> tuple[int, int] | None:
    return recursive_search(n, 0, 0, 0)

def find_large_prime(start, end):
    for num in range(start, end):
        if is_prime(num):
            return num

if __name__ == "__main__":
    low = 10**5
    high = 10 * low
    p_base = random.randint(low, high)
    q_base = random.randint(low, high)
    p = find_large_prime(p_base, 2 * p_base)
    q = find_large_prime(q_base, 2 * q_base)
    print(f"{p = }, {q = }, {p * q = }")
    print(f"{find_prime_factors(p * q)=}")
