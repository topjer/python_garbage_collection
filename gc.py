import numpy as np
from time import sleep
import gc

@profile
def random_number_average(seconds: float):
    size = round(seconds * 10_000_000)
    arr1 = np.random.randint(low=0, high=100, size=size)
    sleep(seconds)
    return arr1.mean()

def main():
    gc.disable()
    res1 = random_number_average(0.3)
    res2 = random_number_average(0.5)
    res3 = random_number_average(0.4)
    print(f"Averages: {res1}, {res2}, {res3}")

if __name__ == "__main__":
    main()
