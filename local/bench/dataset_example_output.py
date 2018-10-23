from parser import *
import os

static_path = os.path.join(os.path.abspath("."), "example files", "dataset.json")
gen_path = os.path.join(os.path.abspath("."), "example files", "generator.json")

static_dataset = DataSet(static_path)
generator_dataset = DataSet(gen_path)


with open("static_dataset_output.txt", "w") as output:
    with stdout_redirected(output, stdout=sys.stdout):
        static_dataset.run()
        pass
    pass

with open("generator_dataset_output.txt", "w") as output:
    with stdout_redirected(output, stdout=sys.stdout):
        generator_dataset.run()
        pass
    pass
