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
        num_uniques = len(set(data[i]))
        info['unique_values'] = str(num_uniques) + " (this includes missing values)"
        if num_uniques <= 10:
            uvals = set(data[i])
            uval_print = []
            for x in uvals:
                if x == missing:
                    uval_print.append("[missing code]")
                else:
                    uval_print.append(x)
            info['unique_value_content'] = "The values are:\n\t* " + "\n\t* ".join(uval_print) + "\n"
        else:
            info['unique_value_content'] = "Not reported: More than 10 unique values"
        info['missing'] = data[i].count(missing)
        info['percent_missing'] = "{:.0%}".format(info['missing'] / len(data[i]))
        digits = len([d for d in data[i] if d.isdigit()])
        totalvalues = len([d for d in data[i] if len(d) > 0])
        if totalvalues == 0:
            info['percent_digit'] = "no digits"
        else:
            info['percent_digit'] = "{:.0%}".format(digits / totalvalues)

        if digits > 0:
            digit_values = [d for d in data[i] if d.isdigit()]
            info['min_digit'] = min(digit_values)
            info['max_digit'] = max(digit_values)
        else:
            info['min_digit'] = "no digits"
            info['max_digit'] = "no digits"
        if headers:
            col_info['cols'][col] = info
        else:
            col_info['cols']['col_' + str(i)] = info
    return col_info
            
def make_md(file_data, headers, target, print_me = True, make_md = True, make_html = False):
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
        for key in headers:#key, data in info.iteritems():
            data = info[key]
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

def get_headers(file):
    with open(file, 'rU') as fin:
        fin = csv.reader(fin)
        headers = next(fin)
    return headers
        

def main(source, target, kind, missingcode):

    #files = [source + f for f in getFiles(source)]
    files = glob.glob(source + "*")
    print "Generating profile for: " + ", ".join(files)

    file_data = {}

    for f in files:
        if f.endswith('.csv'):
            finfo = basic_stats(f)
            headers = get_headers(f)
            csvinfo = review_csv(f, mode = 'rU', missing = missingcode)
            file_data[f] = ({'file_metadata': finfo, \
                             'csv_basic': csvinfo['csv_basic'], \
                             'columns': csvinfo['cols']})

    make_md(file_data, headers, target, print_me = False, make_md = True, make_html = True)



if __name__ == "__main__":
    args = sys.argv
    #print args
    # ['data_profile.py', '-m', 'vagrants/', 'vagrant-profiles/', '']
    main(args[2], args[3], args[1], args[4])
    # not dealing with the the mode right now, just letting it make both


