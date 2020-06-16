import os
import json
from md.backend.benchmarks.bench import Bench
import glob

def init_bench(md_path,mdbench_name,mdbench_definition):
    md_bench = Bench(md_path,mdbench_name,mdbench_definition)


    return md_bench
