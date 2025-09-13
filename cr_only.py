import numpy as np
from time import sleep

@profile
def random_number_average(seconds: float):
    size = round(seconds * 10_000_000)
    arr1 = np.random.randint(low=0, high=100, size=size)
    eternal_list = []
    eternal_list.append(arr1)
    eternal_list.append(eternal_list)
    sleep(seconds)
    return arr1.mean()

def main():
    res1 = random_number_average(0.3)
    res2 = random_number_average(0.5)
    res3 = random_number_average(0.4)
    print(f"Averages: {res1}, {res2}, {res3}")

if __name__ == "__main__":
    main()
