from rg.util import tsv
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
        tsv_string = tsv.from_roster(roster)
        tsv_string += "\n\n\t\t休\tA\tB\t2\tC\n"
        tsv_string += "\n".join(["\t=A{0}\t=COUNTIF(C{0}:AG{0}, \"休\")"
                                 "\t=COUNTIF(C{0}:AG{0}, \"A\")"
                                 "\t=COUNTIF(C{0}:AG{0}, \"B\")"
                                 "\t=COUNTIF(C{0}:AG{0}, \"2\")"
                                 "\t=COUNTIF(C{0}:AG{0}, \"C\")"
                                 .format(i)
                                 for i in range(1, 5)])

        with open("out/out.tsv", mode="w", encoding="utf-8") as filep:
            filep.write(tsv_string)
    end = time()
    print("complete in %d seconds." % (end - start))

if __name__ == '__main__':
    main()
