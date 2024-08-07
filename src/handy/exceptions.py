class HandyError(Exception):
    pass


class LLMError(HandyError):
    pass


class ChatExists(HandyError):
    pass


class ToolNoDocString(HandyError):
    pass


class ToolDescriptionError(HandyError):
    pass


class ToolMissingParamDescription(HandyError):
    pass


class ToolCallMissingParam(HandyError):
    pass
