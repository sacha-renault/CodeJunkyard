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

def find_div_pair(n: int, num: int, p: int, q: int, depth: int) -> list[Pair]:
    pairs = []
    for x in range(0, 10):
        fx = (x * 10**depth + p)
        if fx * 10 > n:
            break
        for y in range(0, 10):
            fy = (y * 10**depth + q)
            product = fx * fy
            if product > n:
                break;
            if product == num or product % (10 ** len(str(num))) == num:
                pairs.append(Pair(fx, fy))
    return pairs


def find_pq(n: int) -> tuple[int, int] | None:
    def _inner_find_pq(n: int, q: int = 0, p: int = 0, depth: int = 0) -> tuple[int, int] | None:
        dn = int(str(n)[-(depth + 1):])
        if dn != 0:
            for pp, pq in find_div_pair(n, dn, p, q, depth):
                if pp * pq == n and pp != 1 and pq != 1:
                    return pp, pq
                elif pp * pq < n:
                    result = _inner_find_pq(n, pq, pp, depth + 1)
                    if result is not None:
                        return result  # Return result up the call stack if found
        return None
    return _inner_find_pq(n)



if __name__ == "__main__":
    low = 10 ** 5
    high = 10 * low
    p_base = random.randint(low, high) # search a prime from this point
    q_base = random.randint(low, high) # search a prime from this point
    p = find_large_prime(p_base, 2*p_base)
    q = find_large_prime(q_base, 2*q_base)
    print(f"{p = }, {q = }, {p * q = }")
    print(f"{find_pq(p * q)=}")
