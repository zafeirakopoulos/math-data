import json
import sys
import pprint
import collections



keywords = ["Vertex", "Graph", "Edge", "Directed", "Weighted", "Polyhedron", "Polynomial", "Polytope"]
def get_string_type():
    PY3 = sys.version_info[0] == 3
    if PY3:
        string_types = str
    else:
        string_types = basestring
    return string_types

def isastring(value):
    if isinstance(value, get_string_type()):
        words = get_string(value)
        if not words:
            raise Exception("The input is a string but none of them is meaningful. See our keywords: " + keywords)
        else:
            results = get_meaningful_string(words)
            raise Exception("The input is a string and they are possible names according to your input " + results)

    else:
        raise Exception("The input is not a string. Please enter a string and use at least one in the following keywords: " + results)

def get_string(value):
    words = value.split()
    meaningful_words = []
    for word in words:
        if word in keywords:
            meaningful_words.append(word)
    return meaningful_words

def get_meaningful_string(words):
    #ref : https://www.pythonforbeginners.com/dictionary/how-to-use-dictionaries-in-python/
    with open("dictionary.index") as dictIndex:
        index = json.load(dictIndex)
    freq_names= {}
    max_value = 1
    for word in words:
        if word in index:
            for name in index[word]:
                if name in freq_names:
                    freq_names[name] = freq_names.get(name) + 1
                    if max_value < freq_names[name]:
                        max_value = freq_names[name]
                else:
                    freq_names[name] = 1
    most_freq_names = []
    for name in freq_names:
        if freq_names[name] == max_value:
            most_freq_names.append(name)
    return most_freq_names

def update_dict(d, u):
    for k, v in u.items():

        if isinstance(d, collections.Mapping):
            if isinstance(v, collections.Mapping):
                r = update_dict(d.get(k, {}), v)
                d[k] = r
            else:
                if k in ["attributes","raw_types"]:
                    tmp = []
                    if k in d:
                        tmp = [ e for e in d[k]]
                    for e in u[k]:
                        if e not in tmp:
                            tmp.append(e)
                    d[k] = tmp
                else:
                    d[k] = u[k]
        else:
            d = {k: u[k]}
    return d

def interpret(name):
    with open("def.index") as defIndex:
        index = json.load(defIndex)
        if name not in index:
            raise Exception("Definition not found in the definition index")
        else:
            # TODO Find correct revision of the file
            filename = index[name][0]
    with open(filename+".def") as defFile:
        definition = json.load(defFile)
        if "inherits" in definition:
            # TODO resolve dependencies
            parents = definition.pop("inherits")
            for parent in parents:
                parentDef = interpret(parent)
                update_dict(parentDef,definition)
                definition = parentDef
        return definition

def is_of_type(A,B):
    if A == B :
        return True
    with open(A+".def") as Afile:
        A = json.load(Afile)
        if "inherits" in A:
            ret = False
            for parent in A["inherits"]:
                ret = ret | is_of_type(parent,B)
            return ret
    return False


def validate_type(data,T, json_def):
    #  "List", "Matrix", "Tuple"
	if T in ["Boolean"]:
		if isinstance(data, list):
			for i in range(len(data)):
				return validate_type(data[i], T, json_def)
		return (str(data) == "0") or (str(data) == "1") or (str(data) == "True") or (str(data) == "False")
	elif T in ["Integer"]:
		if isinstance(data, list):
			for i in range(len(data)):
				return validate_type(data[i], T, json_def)
		return isinstance(data, int)
	elif T in ["Number"]:
		if isinstance(data, list):
			for i in range(len(data)):
				return validate_type(data[i], T, json_def)
		return isinstance(data, float)
	elif isinstance(T, list):
		for i in range(len(data)):
			return validate_type(data[i], T[i], json_def)
	elif "{" in str(T):
		oldstr = str(T)
		newstr = oldstr.replace("{", "")
		newstr = newstr.replace("}", "")
		return validate_type(data, json_def["parameters"][newstr][0], json_def)


def validate_structure(data,T):
    #  "List", "Matrix", "Tuple"
    if T=="Matrix":
        if not isinstance(data, list):
            raise Exception("Not a Matrix")
        col = len(data)
        print(col)
        for row in data:
            if not isinstance(row, list):
                    raise Exception("Not a Matrix")
            if len(row) != col:
                raise Exception("Not a Matrix")
    if T=="List":
        if not isinstance(data, list):
            raise Exception("Not a List")
    return True

def get_iterator_of_elements(structure, data):
	if structure == "Matrix":
		if len(data)==0:
			raise Exception("Matrix is empty")
		return [ data[i][j] for i in range(len(data)) for j in range(len(data[0]))]
	elif structure == "List":
		if len(data)==0:
			raise Exception("List is empty")
		return data
	elif "Tuple" in structure:
		return data

def check_rec(structure, element, data, json_def):
    # First we check if the structure is correct
	if not validate_structure(data,structure):
		raise Exception("Data is not a " + structure)

    # Check if every entry is of element
	elements = get_iterator_of_elements(structure, data)
	if type(element)==dict:
		for e in elements:
			check_rec(element["structure"],element["element"],e, json_def)
	else:
		if not validate_type(elements,element[0], json_def):
			raise Exception("wrong element type")
	return True

def analyze_data_file(json_data, json_def):
    for data in json_data:
        if (data not in json_def) and (data != 'type'):
            raise Exception(data + " is not found in definition file")
    data_raw_types=json_def["raw_types"]
    data_attributes=json_def["attributes"]
    data_raw = json_data["raw"]
    for data_raw_type in data_raw:
        if data_raw_type not in data_raw_types:
            raise Exception(data_raw_type + " is not valid raw type")
        raw_def = json_def["raw"][data_raw_type]
        raw_data = json_data["raw"][data_raw_type]
        for attribute in data_attributes:
            if attribute not in raw_data:
                raise Exception(attribute + "  not found in data file")
        for attribute in raw_data:
            if attribute not in data_attributes:
                raise Exception(attribute + "  not found in definition file")
        for attribute in raw_data:
            check_rec( raw_def[attribute]["structure"],  raw_def[attribute]["element"], raw_data[attribute], json_data)
    return True



def validate(data):
	with open(data+".data") as dataFile:
		data_file = json.load(dataFile)
		def_file = interpret(data_file["type"])
		#pprint.pprint(data_file)
		analyze_data_file(data_file, def_file)
	return True

if __name__ == "__main__":
    # execute only if run as a script
    #pprint.pprint(interpret(sys.argv[1]))
    #print("-----------")
    pprint.pprint(interpret(sys.argv[1]))

    #print(is_of_type(sys.argv[1],sys.argv[2]))
    #isastring("Edge Graph")
    #print(isastring("Weighted Graph"))
    #validate("data/new_graph")
    #bar('graph.def', 'raw')
