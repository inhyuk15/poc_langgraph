import pytest
from src.filesystem import MCPFileHandler

fh = MCPFileHandler()

async def test_tool_list():
    expected = [
        'read_file',
        'read_text_file',
        'read_media_file',
        'read_multiple_files',
        'write_file',
        'edit_file',
        'create_directory',
        'list_directory',
        'list_directory_with_sizes',
        'directory_tree',
        'move_file',
        'search_files',
        'get_file_info',
        'list_allowed_directories'
    ]

    async with fh.aopen('tests/filesystem/test_dirs') as session:
        result = await session.list_tools()
        tools = result.tools
        names = [t.name for t in tools]

        assert len(names) == len(expected)

    