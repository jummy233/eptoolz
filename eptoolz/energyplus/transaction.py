"""
handle the transaction of IdfObject.
all operations in IdfObject are not directly act on idf/epJson file
unless you commit the change
"""


class EPTransaction:

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def commit(self):
        ...

    def rollback(self):
        ...
