from md.md_def import *
from functools import reduce
import json

class MathDataLanguage:
    """A MathData language."""

    def __init__(self, active_db):
        """Initializes a MathDataLanguage object.

        :returns: A MathDataLanguage instance"""
        self.db = active_db

    def valid_name(self,name):
        if isinstance(name,str):
            # TODO check if safe
            # TODO check if valif accirding to MDL specs
            return True
        return false

    def get_size(self, string, instance):
        if "@" not in string:
            raise Exception("Not a size string, @ missing.")
        if string.split("@")[1]=="any":
            return -1
        keys = string.split("@")[1].split(".")
        return reduce(lambda c, k: c.get(k, {}), keys, instance)

    def check_element_type(self, item, element_type  ):
        print("\nChecking")
        print(item)
        print(element_type)
        return True

    def validate_instance(self, instance_key,datastructure_key):
        instance = json.loads(self.db.retrieve_instance(instance_key))
        datastructure = json.loads(self.db.retrieve_datastructure(datastructure_key))

        # Check if instance has obligatory keys according to language definition
        for key in mdl_definition["obligatory_keys"]:
            if key not in instance.keys():
                raise Exception("Obligatory key " + key + " not found.")

        if not self.valid_name(instance["name"]):
            raise Exception("Invalid name.")

        attributes = datastructure["attributes"]
        attributes = [ a for a in attributes if attributes[a]]

        # Check if raw representations are valid
        rtypes = [t for t in instance["raw types"] if instance["raw types"][t]]
        print(rtypes)
        for rtype in rtypes:
            print("raw type: ", rtype)
            if rtype not in datastructure["raw types"]:
                raise Exception("Invalid raw type.")
            if rtype not in instance["raw"]:
                raise Exception("Raw type not found in instance.")
            raw_representation = instance["raw"][rtype]
            raw_definition = datastructure["raw"][rtype]

            for attribute in attributes:
                if attribute not in raw_representation:
                    raise Exception(attribute + " missing from instance.")

                print("\n\n For ", attribute)
                structure = raw_definition[attribute]["structure"]
                if structure == "AST":
                    pass
                elif structure == "scalar":
                    pass
                elif isinstance(structure,list):
                    structure = [self.get_size(s,instance) for s in structure]
                    tmp=raw_representation[attribute]
                    for s in structure:
                        if s!=-1:
                            if len(tmp)!=s:
                                raise Exception("Mismatch in dimension.")
                        self.check_element_type(tmp,raw_definition[attribute]["element"])
                        tmp = tmp[0]


        return "False"
