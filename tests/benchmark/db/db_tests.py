from mdbutil.benchmark.db import DB

if __name__ == '__main__':
    db = DB("db")

    # test add
    db['test'].add('test_file1.json', 'adding test file 1')
    db['test'].add('test_file2.json', 'adding test file 2')
