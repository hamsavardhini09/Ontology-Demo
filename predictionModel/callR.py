__author__ = 'Karuna'

import os
import subprocess
from subprocess import Popen, PIPE, STDOUT

def func():
    file = open('predictionModel/Rinput.txt', 'r')

    path = "/usr/lib/R/bin/Rscript"
    script = "predictionModel/load_and_run.R"

    p = Popen([path, script, file.read()], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    output = p.stdout.read()
    p.stdout.close()
    return output

'''if __name__ == '__main__':
    value = func()
    print value'''



