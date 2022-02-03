from enum import Enum, auto

class BracketMode(Enum):
    NONE_MODE=auto()
    ATTACH_MODE=auto()
    BREAK_MODE=auto()

class ASFormatter:
    headers: list[str]=[]
    def __init__(self):
        
        self.preBracketHeaderStack=None
        self.parentStack=None

        self.sourceIterator=None
        self.bracketFormatMode=BracketMode.NONE_MODE
        self.shouldPadOperators=False
        self.shouldPadParenthesies=False
        self.shouldPadBlocks=False
        self.shouldBreakOneLineBlocks=True
        self.shouldBreakOneLineStatements=True
        self.shouldConvertTabs=False
        self.shoudBreakBlocks=False
        self.shouldBreakClosingHeaderBlocks=False
        self.shoudBreakElseIfs=False
    def __del__(self):
        raise NotImplementedError
    def staticInit(self):

