class hasID():
    """
        items in SMA​Algorithm​PlatformAlgorithm​Interface​AIDM  which have an ID.
    """
    ID: int

    def __init__(self, node_id: int):
        assert isinstance(node_id, int), 'node_id is not an int: {0}'.format(node_id)
        self.ID = node_id

    def get_id(self):
        return self.ID


class hasCode():
    """

    """
    Code: str

    def __init__(self, code_string: str):
        assert isinstance(code_string, str), 'code_string is not an str: {0}'.format(code_string)
        self.Code = code_string

    def get_code(self):
        return self.Code


class hasDebugString():
    """

    """
    DebugString: str

    def __init__(self, debug_string: str = ''):
        assert isinstance(debug_string, str), 'debug_string is not an str: {0}'.format(debug_string)
        self.DebugString = debug_string

    def get_debug_string(self):
        return self.DebugString


class AlgorithmNode(hasID, hasCode, hasDebugString):
    def __init__(self, node_id, code_string, debug_string):
        hasID.__init__(self, node_id)
        hasCode.__init__(self, code_string)
        hasDebugString.__init__(self, debug_string)