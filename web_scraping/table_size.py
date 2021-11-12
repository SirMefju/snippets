from bs4 import BeautifulSoup
import csv
from datetime import datetime
from requests import get


# data source
URL = 'http://dev-datalake-master01.hestia.polska:16010/master-status'
page = get(URL)
# parsing html with beautifulsoup
bs = BeautifulSoup(page.content, 'html.parser')


def table_name():
    # inicialize array for names in csv file
    names = []
    # appending 'date' for the first column
    names.append('date')
    # searching for 'div' with id 'tab_userTables'
    table_name = bs.find('div', id = 'tab_userTables')
    # searching every 'a' in table_name
    for table_name in table_name.find_all('a')[:-1]:
        a = table_name.getText().strip()
        # appending table's name for the first column
        names.append(a)
    
    # saving to csv file
    with open('file.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(names)   


def table_size():
    # initalize array for the size
    table_of_size = []
    # insert the date
    with open('file.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # current time
        today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        table_of_size.append(today)    
    # searching for 'div' with id 'tab_userTables'  
    name = bs.find('div', id = 'tab_userTables')
    # searching every 'a' in table_name
    for link in name.find_all('a')[:-1]:
        # replacement for the next link
        x = URL.replace('master-status', '')
        # href is an atribute with 'a'
        url2 = x + link['href']
        next_page = get(url2)
        # parsing html with beautifulsoup
        soup = BeautifulSoup(next_page.content, 'html.parser')
        # searching the new page
        second_page = soup.find('table', id = 'regionServerDetailsTable')
        # deleting every break lines
        for e in soup.find_all('br'):
           e.extract()
        # searching every [4] 'th' 
        for th in second_page.find_all('th')[4]:
            # show every th, replace '(', ')' and separate every space with " "
            txt = str(th.replace('(','').replace(')','')).split(sep = " ")
            # change size to GB
            if txt[-1] == 'B':
                table_of_size.append((float(txt[0])/1073741824))
            if txt[-1] == 'KB':
                table_of_size.append((float(txt[0])/1048576))
            if txt[-1] == 'MB':
                table_of_size.append((float(txt[0])/1024))
            if txt[-1] == 'GB':
                table_of_size.append((float(txt[0])))
            if txt[-1] == 'TB':
                table_of_size.append((float(txt[0])*1024))

    # saving to csv file  
    with open('file.csv', 'a', encoding='utf-8', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(table_of_size)


# opening csv file
def readline():
    with open('file.csv', 'r', encoding='utf-8') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            print(row)


# table_name()
table_size()