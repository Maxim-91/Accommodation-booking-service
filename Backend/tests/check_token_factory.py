from factories.services import token_tool_factory
from tools.symmetric_token_tool import SymmetricTokenTool
from tools.asymmetric_token_tool import AsymmetricTokenTool

token_tool = token_tool_factory()

print(type(token_tool).__name__)

assert isinstance(token_tool, (SymmetricTokenTool, AsymmetricTokenTool))
