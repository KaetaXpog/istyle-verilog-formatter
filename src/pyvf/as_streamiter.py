class ASStreamIterator:
    def __init__(self,f):
        self.infile=f
        self.linecount=0
        self.lines: list[str]=self.infile.readlines()
    def __del__(self):
        try:
            self.infile.close()
        finally:
            pass
    def hasMoreLines(self)->bool:
        return len(self.lines)>0
    def nextLine(self)->str:
        """without '\r' or '\n' in the returned line"""
        return self.lines.pop(0)
