import json
import sys
import pprint
import collections
from interpreter import *

def split(data):
    # interpret should be resolve (also in the other file of ocurse)
    definition = interpret(data["type"])

    if ("name" in data) and ("plural" in data):
        names = [data["name"],data["plural"]]
        print("Names:")
        for name in names:
            print("  " + name)

    if "features" in data:
        features = data["features"]
        print("Features:")
        for feature in features:
            print("  " + feature + " : " + features[feature])


if __name__ == "__main__":
    with open(sys.argv[1]+".data") as dataFile:
        data = json.load(dataFile)
        split(data)
