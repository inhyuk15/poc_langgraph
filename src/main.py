import asyncio
from dotenv import load_dotenv
from agent.manager import AppManager

load_dotenv()


async def main():
    """메인 함수 - 파일 조작 에이전트를 실행합니다."""
    app_manager = AppManager()
    await app_manager.run()

if __name__ == '__main__':
    asyncio.run(main())