from __future__ import division
# command line prompt
# python data_profile.py -[mh][source folder of data] [target folder for profiles] 
# -m make markdown
# -h make html




import os
from os.path import isfile, join
import csv
import datetime
import pandas as pd
import glob
import markdown
import sys



def getFiles(path):
    """Function to return a list of all files within a folder"""
    files = [ f for f in os.listdir(path) if isfile(join(path,f)) and f[0] != '.' ]
    return files

def basic_stats(file):
    stats = os.stat(file)
    size = stats.st_size
    last_modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    last_access = datetime.datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
    return {'filename': file, 'size': size, 'last_access': last_access, 'last_modified': last_modified}

def review_csv(file, mode = 'rt', headers = True, index_row = True, missing = ''):
    with open(file, mode) as fin:
        fin = csv.reader(fin)
        if headers:
            col_names = next(fin)
            data = [r for r in fin]
        else:
            data = [r for r in fin]

    if index_row:
        ids = [r[0] for r in data]
    else:
        ids = "None declared"

    num_rows = len(data)
    data = map(list, zip(*data))
        

    num_columns = len(col_names)
    col_info = {'csv_basic': {'num_rows': num_rows, 'num_columns': num_columns}, 'cols': {}}
    for i, col in enumerate(col_names):
        info = {}
        info['unique_values'] = len(set(data[i]))
        info['missing'] = data[i].count(missing)
        info['percent_missing'] = "{:.0%}".format(info['missing'] / len(data[i]))
        info['percent_digit'] = "{:.0%}".format(len([d for d in data[i] if d.isdigit()]) /                                 len([d for d in data[i] if len(d) > 0]))
        digits = [d for d in data[i] if d.isdigit()]
        if len(digits) > 0:
            info['min_digit'] = min(digits)
            info['max_digit'] = max(digits)
        else:
            info['min_digit'] = "no digits"
            info['max_digit'] = "no digits"
        if headers:
            col_info['cols'][col] = info
        else:
            col_info['cols']['col_' + str(i)] = info
    return col_info
            
def make_md(file_data, target, print_me = True, make_md = True, make_html = False):
    dt = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
    for f, f_data in file_data.iteritems():
        md = ""
        md += "Data Profile for " + f + "\n\n"
        md += "Generated on: " + dt + "\n"
        md += "\n\n"
        basic = f_data['csv_basic']
        md += "Number of columns: " + str(basic['num_columns']) + "\n"
        md += "Number of rows: " + str(basic['num_rows']) + "\n"
        md += "\n"
        info = [f_data['columns'] for f in file_data.keys()][0]
        for key, data in info.iteritems():
            md += "**" + key + "**" + "\n"
            md += "-" * (len(key) + 2) + "\n"
            md += "* Description of column: \n"
            md += "* Collection methods: \n"
            md += "* Description of data values and units: \n"
            md += "* Reason for missing values: \n"
            md += "\n"
            for column, val in data.iteritems():
                md += "* " + column + ": " + str(val) + "\n"
            md += "\n"
        if print_me:
            print md#return md
        if make_md:
            write_name = f.split('/')[-1].split('.')[0] + '_DataProfile.md'
            with open(target + write_name, 'wt') as fout:
                fout.write(md)
        if make_html:
            write_name = f.split('/')[-1].split('.')[0] + '_DataProfile.html'
            with open(target + write_name, 'wt') as fout:
                fout.write(markdown.markdown(md))
        print "Profiles written into " + target
        

def main(source, target, kind):

    #files = [source + f for f in getFiles(source)]
    files = glob.glob(source + "*")
    print "Generating profile for: " + ", ".join(files)

    file_data = {}

    for f in files:
        if f.endswith('.csv'):
            finfo = basic_stats(f)
            csvinfo = review_csv(f, mode = 'rU', missing = '[unknown]')
            file_data[f] = ({'file_metadata': finfo, \
                             'csv_basic': csvinfo['csv_basic'], \
                             'columns': csvinfo['cols']})

    make_md(file_data, target, print_me = False, make_md = True, make_html = True)



if __name__ == "__main__":
    args = sys.argv
    #print args
    # ['data_profile.py', '-m', 'vagrants/', 'vagrant-profiles/']
    main(args[2], args[3], args[1])
    # not dealing with the the mode right now, just letting it make both


