# followed this tutorial for working with csv files in pandas
# https://www.shanelynn.ie/python-pandas-read_csv-load-data-from-csv-files/

import pandas as pd

def read_file():
    file_name = "tweets.csv"
    print("reading", file_name)
    data = pd.read_csv(file_name)
    print(data['text'])

    

def main():
    read_file()

if __name__ == "__main__":
    main()

