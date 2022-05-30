import csv
from datetime import datetime


def under_preasure():
    path = 'preasure.csv'
    with open(path, 'a') as f:
        writer = csv.writer(f)
        today = datetime.now().strftime("%d.%m.%Y %H:%M")
        higher = input("Higher value of pressure: ")
        lower = input("Lower value of pressure: ")
        pulse = input("Heart rate value: ")
        row = (today, higher, lower, pulse)
        writer.writerow(row)
        print("Check file: " + path)

if __name__ == '__main__':
    under_preasure()
