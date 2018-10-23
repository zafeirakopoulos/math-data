import datetime
import random
import argparse
import sys

if "__main__" == __name__:
    parser = argparse.ArgumentParser()

    parser.add_argument("-N", type=int, dest="n")
    parser.add_argument("-M", type=int, dest="m")
    parser.add_argument("-S", type=int, dest="seed")

    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
    else:
        random.seed(datetime.datetime.now())

    #print("[", end="")
    for i in range(args.m):
        print("{\"numbers\":[", end="")
        for j in range(args.n):
            print(random.uniform(0, 100), end="")
            if j is not args.n - 1:
                print(",", end="")
        print("]}")
        pass
    #print("]", end="")
    sys.stdout.close()
