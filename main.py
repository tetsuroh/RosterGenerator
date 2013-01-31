from rg.util import csv
from rg.app import RGApp

from time import time
import os
import re


def main():
    """
    Generate roster using Genetic Algorithm.
    """
    start = time()
    setting_files = list(filter(lambda x: x.endswith('.json'),
                                os.listdir('settings')))
    while True:
        for i, f in enumerate(setting_files):
            print("%d, %s" % (i + 1, f))
        num = input("Please input selected file number >> ")
        if re.match('^\d+$', num):
                break
    rgapp = RGApp("./settings/%s" %
                  setting_files[int(num) - 1])
    drop = len(rgapp.settings['last_month_data'])
    try:
        rgapp.evolve_verbose()
    except KeyboardInterrupt:
        pass
    finally:
        roster = rgapp.best_entity.gene
        print("Shift length is %d" % len(roster[0]))
        with open("out.csv", mode="w", encoding="utf-8") as filep:
            filep.write(csv.from_roster(roster,
                                        drop=drop))
    end = time()
    print("complete in %d seconds." % (end - start))

if __name__ == '__main__':
    main()
