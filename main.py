from time import time
import os
import re
from optparse import OptionParser
from datetime import datetime, timedelta
from calendar import monthrange

from rg.util import tsv
from rg.util.settings import load, save
from rg.app import RGApp


def main(date, out, extension, setting_filename):
    """
    Generate roster using Genetic Algorithm.
    """
    if not setting_filename:
        setting_files = list(filter(lambda x: x.endswith('.json'),
                                    os.listdir('settings')))
        while True:
            for i, f in enumerate(setting_files):
                print("%d, %s" % (i + 1, f.split('.')[0]))
            num = input("Please input selected file number >> ")
            if re.match('^\d+$', num) and \
                    0 < int(num) <= len(setting_files):
                setting_filename = setting_files[num-1]
                break
    settings = get_settings("./settings/"+setting_filename, date)
    start = time()
    rgapp = RGApp("./settings/%s" %
                  setting_filename)
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

        with open("%s.%s" % (out, extension),
                  mode="w", encoding="utf-8") as filep:
            filep.write(tsv_string)
    end = time()
    print("complete in %d seconds." % (end - start))


def get_settings(file_name, date):
    """
    change settings by command line options.
    Arguments:
    - `file_name`: file name of settings.
    - `options`: options.
    """
    settings = load(file_name)
    (settings['date']['year'],
     settings['date']['month'],
     settings['date']['day']) = (date[0],
                                 date[1],
                                 date[2])
    save(settings, file_name)
    return settings


def get_options():
    """
    """
    now = datetime.now()
    (_, lastday) = monthrange(now.year, now.month)
    next_month = now + timedelta(days=lastday - now.day + 1)
    parser = OptionParser()
    parser.add_option("-s", "--setting", dest="setting_filename",
                      help="read settings from FILE")

    parser.add_option("-o", "--out", dest="out",
                      help="write result to FILE",
                      default="out/out")

    parser.add_option("-e", "--extension", dest="extension",
                      help="file extension. tsv or xlsx",
                      default="tsv")

    parser.add_option("-t", "--template", dest="template")

    parser.add_option("--start-position", nargs=2, dest="start_position",
                      action="store", type="int", default=(0, 0))

    parser.add_option("--date", nargs=3, dest="date",
                      action="store", type="int",
                      help="--date year month day | Default value"
                      "is the 1st of next month.",
                      default=(next_month.year,
                               next_month.month,
                               1))

    parser.add_option("-l", "--length", dest="length",
                      action="store", type="int",
                      help="Length of roster.")

    return parser.parse_args()

if __name__ == '__main__':
    (options, args) = get_options()
    main(date=options.date,
         out=options.out,
         extension=options.extension,
         setting_filename=options.setting_filename)
