import random
from sympy import isprime
from typing import NamedTuple

def find_large_prime(start, end):
    for num in range(start, end, 1):
        if isprime(num):
            return num

class Pair(NamedTuple):
    x: int
    y: int

def search_pairs(n: int, num: int, p: int, q: int, depth: int) -> list[Pair]:
    # init pairs list
    pairs = []

    # loop over 0 to 9 to prepend a digit to p
    for x in range(0, 10):
        new_p = (x * 10**depth + p)     # compute new p value
        if new_p * 10 > n:              # if new_p it's already higher than n, no need to keep computing
            break

        # loop over 0 to 9 to prepend a digit to q
        for y in range(0, 10):
            new_y = (y * 10**depth + q)     # compute new q value
            product = new_p * new_y         # compute the new product
            if product > n:                 # if too big early quit the loop
                break;
            # add to pairs only if the product ends with the digits of num
            if product == num or product % (10 ** len(str(num))) == num:
                pairs.append(Pair(new_p, new_y))
    return pairs


def find_prime_factors(n: int) -> tuple[int, int] | None:
    """
    Attempts to decompose `n` into two prime factors `p` and `q` such that n = p * q.

    Parameters:
    - n: The integer to be decomposed.

    Returns:
    - A tuple (p, q) where both `p` and `q` are prime and `n = p * q`, or None if no such factors are found.
    """

    def _recursive_search(n: int, factor_q: int = 0, factor_p: int = 0, depth: int = 0) -> tuple[int, int] | None:
        """
        Recursively attempts to find prime factors of `n` by constructing potential values for `p` and `q`.

        Parameters:
        - n: The integer to be decomposed.
        - factor_q: The current value being constructed for factor `q`.
        - factor_p: The current value being constructed for factor `p`.
        - depth: The current depth of recursion, representing the number of digits added to `p` and `q`.

        Returns:
        - A tuple (factor_p, factor_q) if prime factors are found, otherwise None.
        """
        # Get the last `depth + 1` digits of `n`
        partial_n = int(str(n)[-(depth + 1):])

        # If `partial_n` is non-zero, attempt to find a pair of factors
        if partial_n != 0:

            # Find candidate pairs (potential_p, potential_q) such that their product ends with `partial_n`
            for potential_p, potential_q in search_pairs(n, partial_n, factor_p, factor_q, depth):

                # Check if `potential_p * potential_q` equals `n` and both are prime and non-trivial
                if (potential_p * potential_q == n and potential_p != 1 and potential_q != 1 and
                    isprime(potential_p) and isprime(potential_q)):
                    return potential_p, potential_q

                # If the product is smaller than `n`, attempt deeper recursion to expand `p` and `q`
                elif potential_p * potential_q < n:
                    result = _recursive_search(n, potential_q, potential_p, depth + 1)
                    if result is not None:
                        return result  # Return result up the call stack if found
        return None

    # Start the recursive search with initial values for p, q, and depth
    return _recursive_search(n)


if __name__ == "__main__":
    low = 10 ** 5
    high = 10 * low
    p_base = random.randint(low, high) # search a prime from this point
    q_base = random.randint(low, high) # search a prime from this point
    p = find_large_prime(p_base, 2*p_base)
    q = find_large_prime(q_base, 2*q_base)
    print(f"{p = }, {q = }, {p * q = }")
    print(f"{find_prime_factors(p * q)=}")
