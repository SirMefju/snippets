from bs4 import BeautifulSoup
import csv
from datetime import datetime
import numpy as np
import pathlib
from requests import get
import subprocess


def run_cmd(args_list):
    # print system command
    print('Running system command: {0}'.format(' '.join(args_list)))
    # read data from stdout and stderr, until end-of-file is reached
    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return =  proc.returncode
    return s_return, s_output, s_err 


def html_scraping(URL, file_path, destination):
    # current time
    today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # data source
    page = get(URL)
    # parse html with beautifulsoup
    bs = BeautifulSoup(page.content, 'html.parser')
    # save to csv file
    # 'a' - if file does not exist, it creates a new file for bwriting
    with open(('hbase-'+today+'.csv'), 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['date', 'table name', 'region name', 'region size(GB)', 'number of story files'])
        # search for 'div' with id 'tab_userTables'
        div = bs.find('div', id = 'tab_userTables')
        # search every 'a' in div
        for data in div.find_all('a')[:-1]:
            # replacement for the next link
            x = URL.replace('master-status', '')
            # href is a atribute with 'a'
            url2 = x + data['href']
            page = get(url2)
            # parse new html with beautifulsoup
            soup = BeautifulSoup(page.content, 'html.parser')
            # search for 'table' with id 'regionServerDetailsTable'
            second_page = soup.find('table', id = 'regionServerDetailsTable')
            # search for 'tbody' in 'table' with id 'regionServerDetailsTable'
            tbody = second_page.find('tbody')
            # search every 'tr' in 'tbody' for region name
            for tr in tbody.find_all('tr'):
                # make an array with table names
                table_name = np.array(data.getText())
                # make an array with region names
                region_name = np.array(str(tr.getText().split('\n')[1]))
                # show every [7] 'tr' and separate every space with " " for region size
                td = (tr.getText().split('\n')[7]).split(sep=" ")
                # change size to GB: size, unit
                convert(td[0],td[-1])
                # make an array with region size
                region_size = np.array(result)
                # show every [8] 'tr' for number of story files and change value to intiger
                num_story_files = np.array(int(tr.getText().split('\n')[8]))
                # save to csv file
                csvwriter.writerow([today, table_name, region_name, region_size, num_story_files])
    # move csv file to the selected location
    (ret, out, err)=run_cmd(['hdfs', 'dfs', '-moveFromLocal', file_path+'/hbase-'+today+'.csv',destination])


def convert(size, unit):
    # make global value
    global result
    # change size to GB
    if unit == 'B':
        result = (float(size)/1048576)
    if unit == 'KB':
        result = (float(size)/1048576)
    if unit == 'MB':
        result = (float(size)/1024)
    if unit == 'GB':
        result = (float(size))
    if unit == 'TB':
        result = (float(size)*1024)


def main():
    # URL, file_path, destination
    html_scraping('http://dev-datalake-master01.hestia.polska:16010/master-status', str(pathlib.Path().resolve()), '/tmp/sizing/hbase/mm=202111')

if __name__ == '__main__':
    main()
