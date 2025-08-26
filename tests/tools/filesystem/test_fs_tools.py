import pytest
import asyncio
from src.agent.tools import fs_tools

async def test_create_and_list_directory(tmp_path):
    test_dir = "test_dir"
    # 디렉토리 생성
    result = await fs_tools.create_directory_tool.ainvoke({"path": test_dir})
    assert "created" in result or "ok" in result or "[create_directory]" in result
    # 디렉토리 목록 확인
    list_result = await fs_tools.list_directory_tool.ainvoke({"path": "."})
    assert test_dir in list_result

async def test_write_and_read_file(tmp_path):
    test_file = "test_file.txt"
    content = "hello world!"
    # 파일 쓰기
    result = await fs_tools.write_file_tool.ainvoke({"path": test_file, "content": content})
    assert "wrote" in result or "ok" in result or "[write_file]" in result
    # 파일이 디렉토리에 있는지 확인
    list_result = await fs_tools.list_directory_tool.ainvoke({"path": "."})
    assert test_file in list_result

async def test_invalid_path():
    # 워크스페이스 밖 경로 시도
    with pytest.raises(ValueError, match="Invalid path: \.\./hack \(outside workspace\)"):
        await fs_tools.create_directory_tool.ainvoke({"path": "../hack"})
