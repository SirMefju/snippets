from bs4 import BeautifulSoup
import csv
from datetime import datetime
from requests import get


# data source
URL = 'http://dev-datalake-master01.hestia.polska:16010/master-status'
page = get(URL)
# parsing html with beautifulsoup
bs = BeautifulSoup(page.content, 'html.parser')


def names():
    # inicialize array for names in csv file
    names_with_region = []
    # appending 'date' for the first column
    names_with_region.append('date')
    # searching for 'div' with id 'tab_userTables'
    table_name = bs.find('div', id = 'tab_userTables')
    # searching every 'a' in table_name
    for table_name in table_name.find_all('a')[:-1]:
        # replacement for the next link
        x = URL.replace('master-status', '')
        # href is an atribute with 'a'
        url2 = x + table_name['href']
        next_page = get(url2)
        # parsing html with beautifulsoup
        soup = BeautifulSoup(next_page.content, 'html.parser')
        # searching for 'table' with id 'regionServerDetailsTable'
        second_page = soup.find('table', id = 'regionServerDetailsTable')
        # searching tag 'a' 
        for region_name in second_page.find_all('a'):
            # appending table and every region name to array
            names_with_region.append([table_name.getText(),region_name.getText()])
        
    # saving to csv file
    with open('regions.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(names_with_region)


def region_size():
    # initalize array for the every region size
    region_size = []
    # insert the date
    with open('file.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # current time
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        region_size.append(today)
    # searching for 'div' with id 'tab_userTables'
    table_name = bs.find('div', id = 'tab_userTables')
    # searching every 'a' in table_name
    for size in table_name.find_all('a')[:-1]:
        # replacement for the next link
        x = URL.replace('master-status', '')
        # href is a atribute with 'a'
        url2 = x + size['href']
        page = get(url2)
        # parsing html with beautifulsoup
        soup = BeautifulSoup(page.content, 'html.parser')
        # searching for 'table' with id 'regionServerDetailsTable'
        second_page = soup.find('table', id = 'regionServerDetailsTable')
        # searching for 'tbody' in 'table' with id 'regionServerDetailsTable'
        tbody = second_page.find('tbody')
        # searching every 'tr' in 'tbody'
        for tr in tbody.find_all('tr'):
            # show every [7] 'tr' and separate every space with " "
            td = (tr.getText().split('\n')[7]).split(sep=" ")
            # change size to GB
            if td[-1] == 'B':
                region_size.append((float(td[0])/1073741824))
            if td[-1] == 'KB':
                region_size.append((float(td[0])/1048576))
            if td[-1] == 'MB':
                region_size.append((float(td[0])/1024))
            if td[-1] == 'GB':
                region_size.append((float(td[0])))
            if td[-1] == 'TB':
                region_size.append((float(td[0])*1024))
                   
    # saving to csv file
    with open('regions.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(region_size)


# opening csv file
def readline():
    with open('region.csv', 'r', encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            print(row)


# names()
region_size()