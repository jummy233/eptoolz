"""
In memory buffer to hold on editing idf objects.
"""

from io import StringIO


class IdfBuffer(StringIO):

    def __init__(self, output: str):
        """
        Parameters:
            output: output path of idf file.
        """
        self.output = output

    def flush(self):
        ...



