import asyncio
from dotenv import load_dotenv
from agent import run_file_ops_agent

load_dotenv()


async def main():
    """메인 함수 - 파일 조작 에이전트를 실행합니다."""
    user_message = "Create a default C++ project structure"
    await run_file_ops_agent(user_message)


if __name__ == '__main__':
    asyncio.run(main())