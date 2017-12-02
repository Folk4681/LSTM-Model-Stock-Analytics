from __future__ import print_function

import sys, requests, json

from pyspark.sql import SparkSession

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


def getAPIKey():
    global NYT_API_KEY
    try:
        NYT_API_KEY = json.load(open(API_FILE))['New_York_Times_Archive_API']
    except NoFileException as e:
        errormsg = "Something's wrong. Perhaps your 'keys.json' file doesn't exist?"
        raise e(errormsg)





def main():
    getAPIKey()
    print(NYT_API_KEY)
    


if __name__ == "__main__":
    main()
