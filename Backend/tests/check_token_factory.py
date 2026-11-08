import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from factories.services import token_tool_factory
from tools.symmetric_token_tool import SymmetricTokenTool
from tools.asymmetric_token_tool import AsymmetricTokenTool


token_tool = token_tool_factory()
print(f"Loaded token tool: {type(token_tool).__name__}")

assert isinstance(token_tool, (SymmetricTokenTool, AsymmetricTokenTool))
