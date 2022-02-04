from enum import Enum, auto
from as_streamiter import ASStreamIterator

class BracketMode(Enum):
    NONE_MODE=auto()
    ATTACH_MODE=auto()
    BREAK_MODE=auto()

class ASFormatter:
    headers: list[str]=[]
    nonParenHeaders: list[str]=[]
    # used for verilog
    preprocessorHeaders:list[str]=[]
    preCommandHeaders:list[str]=[]
    operators:list[str]=[]
    verilogBlockBegin:list[str]=[]
    verilogBlockEnd:list[str]=[]
    calledInitStatic:bool

    def __init__(self):
        self.staticInit()
        
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
        if ASFormatter.calledInitStatic:
            return
        
        ASFormatter.calledInitStatic=True

        
