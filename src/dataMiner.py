from __future__ import print_function

import os, requests, json, shutil, time, sys

API_FILE = "../keys.json"  # specify your New York Times Archive and AlphaVantage API key in this file here
DATA_STORAGE = "../data/"
NYT_Storage = "NYT_ArticlesJSON/"
ALPHAV_Storage = "Stock_Prices/"
MONTHS = 12
YEARS = [2016, 2017]
NYT_URL = "http://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key={}"
ALPHAV_URL = "https://www.alphavantage.co/query?function={}&symbol={}&outputsize={}&datatype={}&apikey={}"
SYMBOL = "SPX"
MODE = "TIME_SERIES_DAILY"
OUTPUT_SIZE = "full"
DATA_TYPE = "csv"


class NoFileException(Exception):
    def __init__(self, msg=None):
        if msg is None:
            msg = "Error reading JSON file."
        super(NoFileException, self).__init__(msg)


def loadingBar(total, progress):
    barLength, status = 20, ""
    progress = float(progress) / float(total)
    if progress >= 1.:
        progress, status = 1, "\r\n"
    block = int(round(barLength * progress))
    text = "\r[{}] {:.0f}% {}".format(
        "#" * block + "-" * (barLength - block), round(progress * 100, 0),
        status)
    sys.stdout.write(text)
    sys.stdout.flush()


def getAPIKey():
    global NYT_API_KEY, ALPHAV_API_KEY
    try:
        NYT_API_KEY = json.load(open(API_FILE))['New_York_Times_Archive_API']
        ALPHAV_API_KEY = json.load(open(API_FILE))['AlphaVantage_API']
    except NoFileException as e:
        errormsg = "Something's wrong. Perhaps your 'keys.json' file doesn't exist?"
        raise e(errormsg)


def createDataDir(data_folder):
    if os.path.exists(data_folder):
        shutil.rmtree(data_folder)
    os.makedirs(data_folder)


def mineArticles():
    count = 0
    total = len(YEARS)*MONTHS
    print("Downloading New York Times Articles...")
    for y in YEARS:
        for m in range(1, MONTHS+1):
            currentURL = NYT_URL.format(y, m, NYT_API_KEY)
            response = requests.get(currentURL)
            response.raise_for_status()
            fileName = DATA_STORAGE + NYT_Storage + str(y) + "-" + str(m) + ".json"
            with open(fileName, mode='wb') as localfile:
                localfile.write(response.content)
            count = count+1
            loadingBar(total, count)
            time.sleep(1)
    print("Done. Check your data/{} folder.".format(NYT_Storage))


def mineData():
    print("Downloading financial history of " + SYMBOL + "...")
    currentURL = "https://www.alphavantage.co/query?function={}&symbol={}&outputsize={}&datatype={}&apikey={}".format(MODE, SYMBOL, OUTPUT_SIZE, DATA_TYPE, ALPHAV_API_KEY)
    response = requests.get(currentURL)
    response.raise_for_status()
    fileName = DATA_STORAGE + ALPHAV_Storage + str(SYMBOL) + ".csv"
    with open(fileName, mode='wb') as localfile:
        localfile.write(response.content)
    print("Done. Check your data/{} folder.".format(ALPHAV_Storage))


def main():
    getAPIKey()
    createDataDir(DATA_STORAGE + NYT_Storage)
    mineArticles()
    createDataDir(DATA_STORAGE + ALPHAV_Storage)
    mineData()


if __name__ == "__main__":
    main()
