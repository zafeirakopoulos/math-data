from base64 import urlsafe_b64encode, urlsafe_b64decode
from os.path import join, exists

from mdb.util.db import DB


def db_add_data(db, data, filename=None):
    if filename:
        result = db['test'].add(data, "", filename=filename)
    else:
        result = db['test'].add(data, "")
    return result


def test_it():
    # TEST DB CREATION
    db = DB("db_unit_tests")
    assert exists(db.base), "db folder not present"
    print("db creation success")

    # TEST DB ADD DATA
    res = db_add_data(db, "test_data", filename="first")
    sm, sha = urlsafe_b64decode(res['sha']).decode().split(":")

    sm_path = join(db.base, "test", sm)
    assert exists(sm_path), "table folder not present"
    print("table creation success")

    filepath = join(sm_path, "first")
    assert exists(filepath), "first file not present"

    with open(filepath, "r") as f:
        assert f.read() == "test_data\n", "file content is not same"
    print("table add success")

    # TEST DB GET DATA
    filename, bin_content = db['test'][res['sha']]
    file_content = bin_content.decode()
    assert file_content == "test_data\n", file_content
    print("table get success")

    for i in range(1000):
        print(db_add_data(db, str(i), filename=str(i)))
        pass

    # TEST DB ADD DATA(multi repo)
    res2 = db_add_data(db, "test_data", filename="second")
    sm, sha = urlsafe_b64decode(res2['sha']).decode().split(":")

    sm_path2 = join(db.base, "test", sm)
    assert sm_path != sm_path2, "no new repo"
    assert exists(sm_path2), "table folder not present"
    print("table multi repo creation success")

    filepath = join(sm_path2, "second")
    assert exists(filepath), "first file not present"

    with open(filepath, "r") as f:
        assert f.read() == "test_data\n", "file content is not same"
    print("table multi repo add success")

    # TEST DB GET DATA(multi repo)
    print(res2['sha'], sm, sha)
    filename, bin_content = db['test'][res2['sha']]
    file_content = bin_content.decode()
    assert file_content == "test_data\n", file_content
    print("table multi repo get success")
    print("table multi repo success")


if __name__ == '__main__':
    test_it()  # TODO this is just to bypass the need of sym linking to python lib folder
