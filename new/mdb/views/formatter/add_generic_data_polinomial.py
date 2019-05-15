import json
import string
import os
import sys
import collections
import random
import pprint
new_path = sys.path[0]
new_path = new_path[:-10] + "/language/"
sys.path[0] = new_path
path_def = new_path[:-24] + "/local/defs/"
new_path = new_path[:-24] + "/local/third_party/"
PATH = new_path   #should be changed


boolean_answer = [True, False]



class Polynomial:
    def __init__(self, data):
        self.data = data
        self.name = "Polynomial"
        self.plural = "Polynomials"
        self.attributes = dict({
                            "coefficients" : False,
                            "roots" : False
                            })
        self.options = dict({
                                  "number_variables":  "Integer",
                                  "coefficient_type" : {
 							"value": "Integer"
 						       }
                          })
        self.raw_types = dict({
                              "dense" : False,
                              "sparse" : False,
                              "roots" : False
                             })
        self.size = dict({
                             "variables":  self.options["number_variables"],
                             "degree"  : dict()
                        })
        self.raw = dict()
        self.features = dict({
                               "number of terms" : {
					"value": "infinity"
					}
                            })

    def set_attributes(self, attributes):
        self.attributes = attributes
        self.data["attributes"] = attributes

    def set_options(self, options):
        self.options = options
        self.data["options"] = options


def generatePoly():
    
    data = getPoly()
    PolyObj = Polynomial(data)
    PolyObj = generate_attributes(PolyObj)
    PolyObj.data = setAttributes(PolyObj.data, PolyObj.attributes)
    #print(PolyObj.attributes)
    #pprint.pprint(PolyObj.data)
    

def generate_attributes(PolyObj):
    while PolyObj.attributes["coefficients"] is False and PolyObj.attributes["roots"] is False:
        PolyObj.attributes["coefficients"] = random.choice(boolean_answer)
    return PolyObj
    
def generate_raw_types(PolyObj):
    print('??')        

def getPoly():
    with open(path_def+"polynomial.def") as json_file:
        data = json.load(json_file)
        return data

        

def createOutput(raw_types, data, graph_name, file_name):
    #Create a json file for the generated data
    json_name = PATH + file_name
    if isinstance(raw_types, list):
        for raw_type in raw_types:
            json_name += "_" + raw_type
    else:
        json_name += "_" + raw_types
    json_name += "_" + graph_name
    with open(json_name + '.json', 'w') as outfile:
        json.dump(data, outfile)

def setName(data, name):
    data["name"] = name
    return data
    
def setPlural(data, plural):
    data["plural"] = plural
    return data

def setAttributes(data, attributes):
    data["attributes"] = attributes
    for default in data["attributes"]:
        if data["attributes"][default] == False:
            for raw_type in data["raw"]:
                if default in data["raw"][raw_type]:
                    del data["raw"][raw_type][default]  
    return data

def setOptions(data, options):
    if len(options) != 0:
        for option in options:
            if isinstance(options[option], list):
                for sub_option in options[option]:
                    data["options"][option][sub_option] = options[option][sub_option]   
            else:
                data["options"][option] = options[option]
    return data

def setSize(data, sizes):
    for size in sizes:
        data["size"][size] = sizes[size]
    return data

def setRaw(data, raw):
    for raw_type in raw:
        if data["raw_types"][raw_type] == True:
            for attr_raw in raw[raw_type]:     
                if data["attributes"][attr_raw] == True:
                    data["raw"][raw_type][attr_raw] = raw[raw_type][attr_raw]
                else:
                   del data["raw"][raw_type][attr_raw]
    return data

def setRawTypes(data, raw_types):
    for raw_type in data["raw_types"]:
        data["raw_types"][raw_type] = False
    if isinstance(raw_types, list):
        for raw_type in raw_types:
            data["raw_types"][raw_type] = True
    else:
        data["raw_types"][raw_types] = True

    for raw_type in data["raw_types"]:
         if data["raw_types"][raw_type] == False:
             del data["raw"][raw_type] 
    return data

generatePoly()
