import asyncio
import os
from pathlib import Path
import shutil
import textwrap
import time
import pytest
from src.filesystem import MCPFileHandler

fh = MCPFileHandler()

TEST_DIR=r'tests/filesystem/test_dirs'

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

    async with fh.aopen(TEST_DIR) as session:
        result = await session.list_tools()
        tools = result.tools
        names = [t.name for t in tools]

        assert sorted(names) == sorted(expected)

async def test_list_directory():
    expected = ['test1', 'test2']

    async with fh.aopen(TEST_DIR) as session:
        result = await session.call_tool('list_directory', arguments={'path': os.path.abspath(TEST_DIR)})
        files = ''.join([getattr(c, 'text', '') for c in result.content]).split('\n')
        folders = [file.split(']', 1)[1].strip() for file in files if file.startswith('[DIR]')]
        
        assert(sorted(folders) == sorted(expected))

async def test_create_directory():
    async with fh.aopen(TEST_DIR) as session:
        root = Path(os.path.abspath(TEST_DIR))
        test_path = root / 'test_create_directory'
        if test_path.exists():
            shutil.rmtree(test_path)

        time.sleep(3)
        result = await session.call_tool('create_directory', arguments={'path': test_path})

        assert test_path.exists() and test_path.is_dir()

async def test_read_text_file():
    expected = r'#endif /* __ARM_ACLE_H */'
    async with fh.aopen(TEST_DIR) as session:
        root = Path(os.path.abspath(TEST_DIR))
        test_path = root / 'arm_acle.h'
        result = await session.call_tool('read_text_file', arguments={'path':test_path, 'tail':2})
        file_content = ''.join([c.text for c in result.content if hasattr(c, 'text')]).strip()
        
        assert file_content == expected


async def test_write_file():
    test_file_content = textwrap.dedent(r"""
        #include<iostream>
        int main() {
            std::cout << "hello world!" << '\n';
        }
        """).strip()
    async with fh.aopen(TEST_DIR) as session:
        root = Path(os.path.abspath(TEST_DIR))
        test_path = root / 'test_write_file.cpp'
        if test_path.exists():
            test_path.unlink()
        await asyncio.sleep(3)

        result = await session.call_tool('write_file', arguments={'path': test_path, 'content': test_file_content})
        read_result = await session.call_tool('read_text_file', arguments={'path':test_path, 'tail':3})
        file_content = ''.join([c.text for c in read_result.content if hasattr(c, 'text')]).strip()

        got_nonempty = [ln for ln in file_content.splitlines() if ln.strip() != '']

        expected_lines = [
            '    std::cout << "hello world!" << \'\\n\';',
            '}',
        ]

        assert got_nonempty[-2:] == expected_lines
        
