
from pathlib import Path
from langchain.tools import tool
from filesystem import MCPFileHandler
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

WORKSPACE = "C:\\Users\\user\\Desktop\\workspace\\edith\\poc_langgraph\\test_workspace"

def resolve_and_validate_path(path: str) -> Path:
    """Resolve path relative to WORKSPACE and ensure it does not escape the workspace root."""
    base = Path(WORKSPACE).resolve()
    full_path = (base / path).resolve()
    if not str(full_path).startswith(str(base)):
        raise ValueError(f"Invalid path: {path} (outside workspace)")
    return full_path

@asynccontextmanager
async def workspace_session() -> AsyncGenerator[Any, None]:
    fh = MCPFileHandler()
    async with fh.aopen(WORKSPACE) as session:
        yield session

def debug_print(*args, verbose: bool = False, **kwargs):
    if verbose:
        print(*args, **kwargs)

async def call_workspace_tool(tool_name: str, arguments: dict, verbose: bool = False) -> str:
    try:
        async with workspace_session() as session:
            res = await session.call_tool(tool_name, arguments=arguments)
            debug_print(f"[{tool_name}] args: {arguments} res: {res}", verbose=verbose)
            text_parts = [c.text for c in getattr(res, 'content', []) if hasattr(c, 'text')]
            return "\n".join(text_parts) if text_parts else "ok"
    except Exception as e:
        return f"[ERROR] {tool_name}: {e}"

@tool('get_workspace_info')
async def get_workspace_info():
    """Get the current workspace directory path and available operations."""
    return f"Current workspace: {WORKSPACE}\nAll paths should be relative to this workspace directory."

@tool('create_directory')
async def create_directory_tool(path: str, verbose: bool = False) -> str:
    """Create a directory at `path` relative to the workspace."""
    full_path = resolve_and_validate_path(path)
    result = await call_workspace_tool('create_directory', {'path': str(full_path)}, verbose=verbose)
    return f"[create_directory] {path}: {result}"

@tool('write_file')
async def write_file_tool(path: str, content: str, verbose: bool = False) -> str:
    """Write `content` to the file at `path` (creates/overwrites)."""
    full_path = resolve_and_validate_path(path)
    result = await call_workspace_tool('write_file', {'path': str(full_path), 'content': content}, verbose=verbose)
    return f"[write_file] {path} ({len(content)} bytes): {result}"

@tool('list_directory')
async def list_directory_tool(path: str = ".", verbose: bool = False) -> str:
    """List contents of a directory. Use '.' for current workspace root."""
    full_path = resolve_and_validate_path(path)
    result = await call_workspace_tool('list_directory', {'path': str(full_path)}, verbose=verbose)
    return f"[list_directory] {path}:\n{result if result else 'empty directory'}"

