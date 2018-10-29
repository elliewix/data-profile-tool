from __future__ import division
# command line prompt
# python data_profile.py -[mh][source folder of data] [target folder for profiles]
# -m make markdown
# -h make html

import os
from os.path import isfile, join
import csv
import datetime
import glob
# import markdown # removed html output for now
import sys
import json
from pathlib import Path

# this wasn't being used!!!!!!
# def getFiles(path):
#     """Function to return a list of all files within a folder"""
#     files = [f for f in os.listdir(path) if isfile(join(path, f)) and f[0] != '.']
#     p = Path(path)
#     print(glob.glob(p.read_text() / "*"))
#     print('hello')
#     return files


def basic_stats(file):
    stats = os.stat(file)
    size = stats.st_size
    last_modified = datetime.datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    last_access = datetime.datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S')
    return {'filename': str(file.absolute()), 'size': size, 'last_access': last_access, 'last_modified': last_modified}


def review_csv(file, mode='rt', headers=True, index_row=True, missing=''):
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
    data = list(map(list, zip(*data)))

    num_columns = len(col_names)
    col_info = {'csv_basic': {'num_rows': num_rows, 'num_columns': num_columns, 'missing': missing}, 'cols': {}}
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
            uval_print.sort() # sorting unique values for pretty printing
            info['unique_value_content'] = "The values are:\n\t* " + "\n\t* ".join(uval_print) + "\n"
        else:
            info['unique_value_content'] = "Not reported (More than 10 unique values)"
        info['missing'] = data[i].count(missing)
        info['percent_missing'] = "{:.0%}".format(info['missing'] / len(data[i]))
        # digits = len([d for d in data[i] if d.isdigit()])
        # dcount = 0
        passed_digits = []
        for d in data[i]:
            try:
                float(d)
                # dcount += 1
                passed_digits.append(d)
            except:
                passed_digits.append('failed to convert to float')
        digits = len(passed_digits)
        totalvalues = len([d for d in data[i] if len(d) > 0])

        if totalvalues == 0:
            info['percent_digit'] = "no digits"
        else:
            info['percent_digit'] = "{:.0%}".format(digits / totalvalues)

        if digits > 0:
            # digit_values = [float(d) for d in data[i] if d.isdigit()]
            info['min_digit'] = min(passed_digits)
            info['max_digit'] = max(passed_digits)
        else:
            info['min_digit'] = "no digits"
            info['max_digit'] = "no digits"
        if headers:
            col_info['cols'][col] = info
        else:
            col_info['cols']['col_' + str(i)] = info
    return col_info


def make_md(file_name, file_data, headers, target):
    # print(file_name, headers, target)
    dt = '{:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now())
    md = ""
    md += "Data Profile for " + file_name.name + "\n\n"
    md += "Generated on: " + dt + "\n"
    md += "\n\n"
    basic = file_data['csv_basic']
    md += "* Number of columns: " + str(basic['num_columns']) + "\n"
    md += "* Number of rows: " + str(basic['num_rows']) + "\n"
    if basic['missing'] == '':
        missing_print = "(empty string)"
    else:
        missing_print = basic['missing']
    md += "* Using missing value of: " + missing_print + "\n"
    md += "\n"
    info = [file_data['columns'] for f in file_data.keys()][0]
    for key in headers:
        data = info[key]
        md += "**" + key + "**" + "\n"
        md += "-" * (len(key) + 2) + "\n"
        md += "* Description of column: \n"
        md += "* Collection methods: \n"
        md += "* Description of data values and units: \n"
        md += "* Reason for missing values: \n"
        md += "\n"
        for column, val in data.items():  # go through all the data info
            md += "* " + column.replace('_', ' ') + ": " + str(val) + "\n"
        md += "\n"
    # print file_name
    write_name = file_name.stem + '_DataProfile.md'
    # write_name = file_name.split('/')[-1].split('.')[0] + '_DataProfile'
    # print write_name
    with open(target.absolute() / write_name, 'wt') as fout:
        fout.write(md)

    # the html looks like crap
    # with open(target + write_name + '.html', 'wt') as fout:
    #     fout.write(markdown.markdown(md))


def get_headers(file):
    with open(file, 'rU') as fin:
        fin = csv.reader(fin)
        headers = next(fin)
    return headers


def main(source, target, missingcode):
    do_not_write = False
    target = Path(target)
    source = Path(source)
    # if not target.is_dir():
    #     target += "/"  # sorry windows
    # files = [source + f for f in getFiles(source)]
    if source.is_dir():
        # if not source.endswith('/'):
        #     source += "/"
        files = [p.absolute() for p in source.glob('*')]
        num_files = len(files)
    elif source.is_file():
        files = [source.absolute()]  # forcing this into a list of 1 so for loop works
        num_files = 1

    # only report out file names if there are <10 to do
    if num_files < 10:  # change this number if you care
        print("Generating profile for: " + ", ".join([str(p) for p in files]))
    else:
        print("Generating profiles for " + str(num_files) + " files")

    if os.path.isdir(target):  # this will not play nicely with windows...
        confirm_needed = True
        tstr = str(target.absolute())
        while confirm_needed:
            confirm_overwrite = input("\n" + tstr + " already exists. Do you want to overwrite? (Y/N)\n").upper()
            print(confirm_overwrite)
            if confirm_overwrite == "Y":
                confirm_needed = False
                print("Profiles written into " + tstr + "\n")
            elif confirm_overwrite == "N":
                do_not_write = True
                print("Profiles not written.\n")
                break
            else:
                print("Input not understood. Please try again.")
    else:
        target.mkdir()  # but I can't test windows right now...
        print("\n" + str(target.absolute()) + " created")
        print("\nProfiles written into " + str(target.absolute()) + "\n")
    all_file_data = {}

    if not do_not_write:
        for f in files:
            f = Path(f)
            if f.suffix == '.csv':
                finfo = basic_stats(f)
                headers = get_headers(f)
                csvinfo = review_csv(f, mode='rU', missing=missingcode)
                all_file_data[str(f.name)] = ({'file_metadata': finfo,
                                     'csv_basic': csvinfo['csv_basic'],
                                     'columns': csvinfo['cols']})
                make_md(f, all_file_data[str(f.name)], headers, target)
        write_name = str(target.stem + '_DataProfiles.json')
        # write_name = target.split('/')[-2].split('.')[0] + '_DataProfiles.json'
        with open(target.absolute() / write_name, 'wt') as jsonout:
            json.dump(all_file_data, jsonout, indent=4)


if __name__ == "__main__":
    args = sys.argv
    # print args
    # ['data_profile.py', 'vagrants/', 'vagrant-profiles/', '']
    # usage
    # python data_profile.py source output_folder (missing_code)
    # source may be file or folder
    # output must be a folder
    # missing code optional, will presume empty string if not provided
    source_folder = args[1]
    target_folder = args[2]
    if len(args) < 4:
        missing_code = ''  # presuming '' if not provided
    else:
        missing_code = args[3]

    # main(source, target, kind, missingcode)
    main(source_folder, target_folder, missing_code)
    # not dealing with the the mode right now, just letting it make both


