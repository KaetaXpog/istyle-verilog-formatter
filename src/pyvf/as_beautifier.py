from as_resource import ASResource
from as_streamiter import ASStreamIterator


class ASBeautifier(ASResource):
    headers: list[str] = []
    nonParenHeaders: list[str] = []
    # used for verilog
    preprocessorHeaders: list[str] = []
    verilogBlockBegin: list[str] = []
    verilogBlockEnd: list[str] = []
    calledInitStatic: bool

    def __init__(self):
        self.initStatic()

        waitingBeautifierStack = None
        activeBeautifierStack = None
        waitingBeautifierStackLengthStack = None
        activeBeautifierStackLengthStack = None

        headerStack = None
        tempStacks = None
        blockParenDepthStack = None

        inStatementIndentStack = None
        inStatementIndentStackSizeStack = None
        parenIndentStack = None
        sourceIterator = None

        isMinimalConditinalIndentSet = False
        shouldForceTabIndentation = False

        self.setSpaceIndentation(4)
        self.setMaxInStatementIndentLength(40)

        self.setSwitchIndent(False)

        self.setBlockIndent(False)
        self.setBracketIndent(False)

        self.setLabelIndent(False)
        self.setEmptyLineFill(False)

        self.setPreprocessorIndent(False)

    def __del__(self):
        raise NotImplementedError

    def initStatic(self):
        if ASBeautifier.calledInitStatic:
            return

        ASBeautifier.calledInitStatic = True

        ASBeautifier.headers.append(ASBeautifier.AS_IF)
        ASBeautifier.headers.append(ASBeautifier.AS_ELSE)
        ASBeautifier.headers.append(ASBeautifier.AS_FOR)
        ASBeautifier.headers.append(ASBeautifier.AS_WHILE)
        ASBeautifier.headers.append(ASBeautifier.AS_INITIAL)
        ASBeautifier.headers.append(ASBeautifier.AS_FOREVER)
        ASBeautifier.headers.append(ASBeautifier.AS_ALWAYS)
        ASBeautifier.headers.append(ASBeautifier.AS_REPEAT)
        ASBeautifier.nonParenHeaders.append(ASBeautifier.AS_ELSE)
        ASBeautifier.nonParenHeaders.append(ASBeautifier.AS_INITIAL)
        ASBeautifier.nonParenHeaders.append(ASBeautifier.AS_FOREVER)
        ASBeautifier.nonParenHeaders.append(ASBeautifier.AS_ALWAYS)
        ASBeautifier.nonParenHeaders.append(ASBeautifier.AS_REPEAT)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_CASE)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_CASEX)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_CASEZ)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_GENERATE)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_FUNCTION)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_FORK)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_TABLE)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_TASK)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_SPECIFY)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_PRIMITIVE)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_MODULE)
        ASBeautifier.verilogBlockBegin.append(ASBeautifier.AS_BEGIN)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_ENDCASE)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_ENDGENERATE)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_ENDFUNCTION)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_JOIN)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_ENDTASK)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_ENDTABLE)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_ENDSPECIFY)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_ENDPRIMITIVE)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_ENDMODULE)
        ASBeautifier.verilogBlockEnd.append(ASBeautifier.AS_END)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_CELLDEFINE)
        ASBeautifier.preprocessorHeaders.append(
            ASBeautifier.PRO_DEFAULT_NETTYPE)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_DEFINE)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_ELSE)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_ELSIF)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_ENDCELLDEFINE)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_ENDIF)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_ENDPROTECT)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_IFDEF)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_IFNDEF)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_INCLUDE)
        ASBeautifier.preprocessorHeaders.append(
            ASBeautifier.PRO_NOUNCONNECTED_DRIVE)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_PROTECT)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_RESETALL)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_TIMESCALE)
        ASBeautifier.preprocessorHeaders.append(
            ASBeautifier.PRO_UNCONNECTED_DRIVE)
        ASBeautifier.preprocessorHeaders.append(ASBeautifier.PRO_UNDEF)

    def initIter(self, iter: ASStreamIterator):
        self.sourceIterator = iter
        self.init()

    def init(self):
        self.waitingBeautifierStack: list[ASBeautifier] = []
        self.activeBeautifierStack: list[ASBeautifier] = []

        self.waitingBeautifierStackLengthStack: list[int] = []
        self.activeBeautifierStackLengthStack: list[int] = []

        self.headerStack: list[str] = []
        self.tempStacks: list[list[str]] = []
        self.tempStacks.append([])

        self.blockParenDepthStack: list[int] = []

        self.inStatementIndentStack: list[int] = []
        self.inStatementIndentStackSizeStack: list[int] = []
        self.inStatementIndentStackSizeStack.append(0)
        self.parenIndentStack: list[int] = []

        self.previousLastLineHeader: str = ""

        self.isInQuote = False
        self.isInComment = False
        self.isInStatement = False
        self.isInCase = 0
        self.isInQuestion = False
        self.isInHeader = False

        self.isInConditional = False
        self.parenDepth = 0

        self.leadingWhiteSpaces = 0
        self.prevNonSpaceCh = '{'
        self.currentNonSpaceCh = '{'
        self.prevNonLegalCh = '{'
        self.currentNonLegalCh = '{'
        self.prevFinalLineSpaceTabCount = 0
        self.prevFinalLineTabCount = 0

        self.backslashEndsPrevLine = False
        self.isInDefine = False
        self.isInDefineDefinition = False
        self.defineTabCount = 0

    def setTabIndentation(self, length: int = 4, forceTabs=False):
        pass

    def setSpaceIndentation(self, length: int = 4):
        pass

    def setMaxInStatementIndentLength(self, max: int):
        pass

    def setMinConditionIndentLength(self, min: int):
        pass

    def setSwitchIndent(self, state: bool):
        pass

    def setCaseIndent(self, state: bool):
        pass

    def setBracketIndent(self, state: bool):
        pass

    def setBlockIndent(self, state: bool):
        pass

    def setLabelIndent(self, state: bool):
        pass

    def setEmptyLineFill(self, state: bool):
        pass

    def setPreprocessorIndent(self, state: bool):
        pass
