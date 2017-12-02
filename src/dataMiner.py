from __future__ import print_function

import os, requests, json, shutil, time, sys

API_FILE = "../keys.json"  # specify your New York Times Archive API key here
DATA_STORAGE = "../data/NYT_Articles"
MONTHS = 12
YEARS = [2016, 2017]
baseURL = "http://api.nytimes.com/svc/archive/v1/{}/{}.json?api-key={}"


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
    global NYT_API_KEY
    try:
        NYT_API_KEY = json.load(open(API_FILE))['New_York_Times_Archive_API']
    except NoFileException as e:
        errormsg = "Something's wrong. Perhaps your 'keys.json' file doesn't exist?"
        raise e(errormsg)


def createDataDir():
    if os.path.exists(DATA_STORAGE):
        shutil.rmtree(DATA_STORAGE)
    os.makedirs(DATA_STORAGE)


def mineData():
    count = 0
    total = len(YEARS)*MONTHS
    print("Downloading New York Times Articles...")
    for y in YEARS:
        for m in range(1, MONTHS+1):
            currentURL = baseURL.format(y, m, NYT_API_KEY)
            response = requests.get(currentURL)
            response.raise_for_status()
            fileName = DATA_STORAGE + "/" + str(y) + "-" + str(m) + ".json"
            with open(fileName, mode='wb') as localfile:
                localfile.write(response.content)
            count = count+1
            loadingBar(total, count)
            time.sleep(0.5)
    print("Done. Check your data folder.")

def main():
    getAPIKey()
    createDataDir()
    mineData()


if __name__ == "__main__":
    main()
