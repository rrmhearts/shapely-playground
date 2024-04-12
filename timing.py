
import timeit
import numpy as np

def while_loop(n=100_000_000):
    i = 0
    s = 0
    while i < n:
        s+=1
        i+=1
    return s

def for_loop(n=100_000_000):
    s = 0
    for i in range(n):
        s+= 1
    return s

if __name__ == "__main__":
    print(f'while loop: {timeit.timeit(while_loop, number=1)}')
    print(f'for loop: {timeit.timeit(for_loop, number=1)}')
    print(f'numpy: {timeit.timeit(lambda : np.sum(np.arange(100_000_000)), number=1 )}')