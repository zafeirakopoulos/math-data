"""Exceptions for the mathdata project.

This module contains all the Exceptions defied in the mathdata project.

Todo:
    * Create Exceptions for different parts of the project
    * Create a uniform Exception standard for the project

"""


class RequiredFieldException(Exception):
    def __init__(self, filepath, field):
        super().__init__('File "{}" does not have field "{}"'.format(filepath, field))
        self.filepath = filepath
        self.field1 = field
        pass

    pass


class SelectionalFieldException(Exception):
    def __init__(self, filepath, field1, field2):
        super().__init__('File "{}" does not have field "{}" or "{}"'.format(filepath, field1, field2))
        self.filepath = filepath
        self.field1 = field1
        self.field2 = field2
        pass

    def __reduce__(self):
        return SelectionalFieldException, (self.filepath, self.field1, self.field2)
        pass

    pass
