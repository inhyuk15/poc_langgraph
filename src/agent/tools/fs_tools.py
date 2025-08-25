from pathlib import Path
from langchain.tools import tool
from filesystem import MCPFileHandler

WORKSPACE = "/Users/ihkang/workspace/python_proj/poc_langgraph/test_workspace"

@tool('get_workspace_info')
async def get_workspace_info():
    """Get the current workspace directory path and available operations."""
    return f"Current workspace: {WORKSPACE}\nAll paths should be relative to this workspace directory."

def debug_print(*args, verbose=False, **kwargs):
    if verbose:
        print(*args, **kwargs)

@tool('create_directory')
async def create_directory_tool(path: str, verbose=False):
    """Create a directory at `path` relative to the workspace. """
    fh = MCPFileHandler()
    async with fh.aopen(WORKSPACE) as session:
        # 상대 경로로 변환
        full_path = Path(WORKSPACE) / path
        res = await session.call_tool('create_directory', arguments={'path': str(full_path)})
        debug_print("[create_directory] args:", path, "full_path:", full_path, "res:", res, verbose=verbose)
        text_parts = [c.text for c in res.content or [] if hasattr(c, 'text')]
        text = "\n".join(text_parts) if text_parts else "ok"
        return f"created directory: {path}"

@tool('write_file')
async def write_file_tool(path: str, content: str, verbose=False):
    """Write `content` to the file at `path` (creates/overwrites). """
    fh = MCPFileHandler()
    async with fh.aopen(WORKSPACE) as session:
        # 상대 경로로 변환
        full_path = Path(WORKSPACE) / path
        res = await session.call_tool('write_file', arguments={'path': str(full_path), 'content': content})
        debug_print("[write_file] args:", path, "full_path:", full_path, "len:", len(content), "res:", res, verbose=verbose)
        return f"wrote: {path} ({len(content)} bytes)"

@tool('list_directory')
async def list_directory_tool(path: str = ".", verbose=False):
    """List contents of a directory. Use '.' for current workspace root."""
    fh = MCPFileHandler()
    async with fh.aopen(WORKSPACE) as session:
        full_path = Path(WORKSPACE) / path
        res = await session.call_tool('list_directory', arguments={'path': str(full_path)})
        debug_print("[list_directory] args:", path, "full_path:", full_path, "res:", res, verbose=verbose)
        text_parts = [c.text for c in res.content or [] if hasattr(c, 'text')]
        text = "\n".join(text_parts) if text_parts else "empty directory"
        return f"Contents of {path}:\n{text}"

