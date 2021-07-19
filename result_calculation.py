from os import listdir
from os.path import isfile, join

dir_path = 'results_length'
folders = [f for f in listdir(dir_path)]
for folder in folders:
    out_run = open(dir_path + "/" + folder + "/outrun29.dat")
    run_results = 0
    line_count = 0
    for l in out_run.readlines():
        line_count += 1
        run_results += float(l.split()[0])
    print(f'mean value: {run_results / line_count} for {folder}')
