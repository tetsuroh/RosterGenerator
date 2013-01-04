from rg import convert
from rg_app import RGApp

from time import time


def main():
    """
    Generate roster using Genetic Algorithm.
    """
    start = time()
    rgapp = RGApp("./settings/sunhome_kitchen.json")
    roster = rgapp.evolve_verbose().gene
    with open("out.csv", mode="w", encoding="utf-8") as filep:
        filep.write(convert(roster))
    end = time()
    print("complete in %d seconds." % (end - start))

if __name__ == '__main__':
    main()
