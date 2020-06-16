import os

# Root folder in the docker container
md_path = "/app"

# Root folder
md_root = os.getcwd()

# MD Database
mdbase_name = "mdbase"
mdbase_definition = '{"paths": ["raw", "options"],"entities":["datastructure", "instance", "dataset","formatter", "format"],"default_branch":"default"}'
mdbase_definitions_folder = ['mdb', 'local', 'definitions']

#MD Benchmarks
mdbench_name = "bench"
mdbench_definition = '{}'

# MD Language
mdl_definition = {
    "obligatory_keys": ["raw", "options"]
}
