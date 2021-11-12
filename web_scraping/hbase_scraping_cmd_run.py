from bs4 import BeautifulSoup
import csv
from datetime import datetime
from requests import get
import numpy as np
import subprocess


def run_cmd(args_list):
    # printing system command
    print('Running system command: {0}'.format(' '.join(args_list)))

    proc = subprocess.Popen(args_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    s_output, s_err = proc.communicate()
    s_return =  proc.returncode
    return s_return, s_output, s_err 


def html_scraping():
    # current time
    today = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    # data source
    URL = 'http://dev-datalake-master01.hestia.polska:16010/master-status'
    page = get(URL)
    # parsing html with beautifulsoup
    bs = BeautifulSoup(page.content, 'html.parser')
    # saving to csv file
    # 'a' - if file does not exist, it creates a new file for writing
    with open(('hbase-'+today+'.csv'), 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['date', 'table name', 'region name', 'region size(GB)', 'number of story files'])
        # searching for 'div' with id 'tab_userTables'
        div = bs.find('div', id = 'tab_userTables')
        # searching every 'a' in div
        for data in div.find_all('a')[:-1]:
            # replacement for the next link
            x = URL.replace('master-status', '')
            # href is a atribute with 'a'
            url2 = x + data['href']
            page = get(url2)
            # parsing new html with beautifulsoup
            soup = BeautifulSoup(page.content, 'html.parser')
            # searching for 'table' with id 'regionServerDetailsTable'
            second_page = soup.find('table', id = 'regionServerDetailsTable')
            # searching for 'tbody' in 'table' with id 'regionServerDetailsTable'
            tbody = second_page.find('tbody')
            # searching every 'tr' in 'tbody' for region name
            for tr in tbody.find_all('tr'):
                # making an array with table names
                table_name = np.array(data.getText())
                # making an array with region names
                region_name = np.array(str(tr.getText().split('\n')[1]))
                # show every [7] 'tr' and separate every space with " " for region size
                td = (tr.getText().split('\n')[7]).split(sep=" ")
                # change size to GB
                if td[-1] == 'B':
                    region_size = np.array((float(td[0])/1073741824))
                if td[-1] == 'KB':
                    region_size = np.array((float(td[0])/1048576))
                if td[-1] == 'MB':
                    region_size = np.array((float(td[0])/1024))
                if td[-1] == 'GB':
                    region_size = np.array((float(td[0])))
                if td[-1] == 'TB':
                    region_size = np.array((float(td[0])*1024))
                # show every [8] 'tr' for number of story files and change value to intiger
                num_story_files = np.array(int(tr.getText().split('\n')[8]))
                # saving to csv file
                csvwriter.writerow([today, table_name, region_name, region_size, num_story_files])
    # copy csv file to the selected location
    (ret, out, err)=run_cmd(['hdfs', 'dfs', '-copyFromLocal', '/home/ciesma3/hbase-'+today+'.csv', '/tmp/sizing/hbase/mm=202111'])
    # (ret, out, err)=run_cmd(['hdfs', 'dfs', '-put', '/home/ciesma3/hbase-'+today+'.csv', '/tmp/sizing/hbase/mm=202111'])



 
html_scraping()


