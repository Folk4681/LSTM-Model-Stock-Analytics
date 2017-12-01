from __future__ import print_function

import sys, requests, json

from pyspark.sql import SparkSession


API_FILE = "../keys.json" # specify your New York Times Archive API key here
NYT_API_KEY = json.load(open(API_FILE))['New_York_Times_Archive_API']


def main():
    print (NYT_API_KEY)


if __name__ == "__main__":
    main()
