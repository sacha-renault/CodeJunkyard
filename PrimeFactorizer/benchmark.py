import time
import random
from math import floor, log10
from collections import defaultdict
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from scipy.stats import linregress

TEST_NUMBA = True

if TEST_NUMBA:
    from prime_factorizer_numba import find_prime_factors
else:
    from prime_factorizer import find_prime_factors

def sieve_of_eratosthenes(limit: int):
    """Create an array of prime numbers in [2, limit]"""
    is_prime = [True] * (limit + 1)
    p = 2
    while (p * p <= limit):
        # If is_prime[p] is not changed, then it is a prime
        if is_prime[p]:
            # Update all multiples of p to false
            for i in range(p * p, limit + 1, p):
                is_prime[i] = False
        p += 1

    # Collecting all prime numbers
    primes = [p for p in range(2, limit + 1) if is_prime[p] if p != 2]
    return primes

def benchmark(p: int, q: int, n_test: int = 100) -> float:
    total_time = 0.0
    for _ in range(n_test):
        # mesure the time of a single function call
        start = time.perf_counter()
        result = find_prime_factors(p * q)
        end = time.perf_counter()

        # ensure result is correct
        if result is None or result not in [(p, q), (q, p)]:
            raise Exception(f"No result or wrong result, {p=}, {q=}, {result=}")

        # increment the time
        total_time += end - start
    return total_time / n_test # avg time to compute

if __name__ == "__main__":
    # max exponenet
    MAX_EXP = 6

    # get prime numbers
    prime_numbers = sieve_of_eratosthenes(10**MAX_EXP)

    # save them in a dictionnary with floor(log10) as key
    prime_dict = defaultdict(list)
    for number in prime_numbers:
        prime_dict[floor(log10(number))].append(number)

    # create a dictionnary key = log10(n) and result avg result time
    results = []

    # iterate until max_exp
    try:
        progress_bar = tqdm(total=10 * (MAX_EXP - 1) ** 2)
        for i in range(1, MAX_EXP):
            for j in range(1, MAX_EXP):
                for _ in range(10): # make 10 test per exp
                    p = random.choice(prime_dict[i])
                    q = random.choice(prime_dict[j])
                    results.append((p * q, benchmark(p, q, 1)))
                    progress_bar.update(1)
        progress_bar.close()
    except KeyboardInterrupt:
        print("Early stopping")

    # plotting
    results.sort(key=lambda x: x[1])
    x_vals = [v[0] for v in results]
    y_vals = [v[1] for v in results]

    # Take log10 of x values (already done in your initial setup)
    x_log_vals = np.log10(x_vals)
    y_log_vals = np.log10(y_vals)

    # Perform quadratic regression on the log-transformed data
    slope, intercept, _, _, _ = linregress(x_log_vals, y_log_vals)

    # Generate values for the linear regression line
    x_fit_log = np.linspace(min(x_log_vals), max(x_log_vals), 500)
    y_fit_log = slope * x_fit_log + intercept

    plt.scatter(x_vals, y_vals, label="Data Points")
    plt.plot(10 ** x_fit_log, 10 ** y_fit_log, color="red", label=f"Linear Regression (log-log), y={slope:.4f}*x + {intercept:.4f}")
    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("p * q")
    plt.ylabel("Average compute time")
    plt.title("Benchmark Result")
    plt.legend()

    print(f"NUMBA: {TEST_NUMBA}, done, saving figure.")
    if TEST_NUMBA:
        plt.savefig("PrimeFactorizer/assets/fig_numba.png")
    else:
        plt.savefig("PrimeFactorizer/assets/fig.png")