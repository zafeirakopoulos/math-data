import git

class Library(object):

    self.name 
    self.path
    self.location

    def __init__(self, name, location="local", path):
        self.name = name
        self.location = location
        if location == "local":
            self.path =
        elif location == "mdata.org":
            self.path =
        elif location == "github":

    def

    def verify(self):
        required = [self.name,self.path]
        for r in required:
            if not isset(r):
                return False
        return True
