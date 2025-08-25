import asyncio
from dataclasses import dataclass
from enum import Enum, auto

from dotenv import load_dotenv
from agent.graph import create_file_ops_graph

load_dotenv()

def debug_print(*args, verbose=False, **kwargs):
    if verbose:
        print(*args, **kwargs)

class Agent():
    def __init__(self, verbose=False):
        self.verbose = verbose

    async def run_file_ops_agent(self, user_message: str):
        """파일 조작 에이전트를 실행합니다."""
        graph = create_file_ops_graph()
        msgs = [
            {"role": "system", "content": (
                "You are a file-ops agent. Always use the provided tools to change files. "
                "IMPORTANT: Use get_workspace_info tool first to understand your working directory. "
                "All paths should be relative to the workspace root. "
                "After each action, return a short confirmation."
            )},
            {"role": "user", "content": user_message}
        ]
        async for event in graph.astream({'messages': msgs}, stream_mode='values'):
            last_message = event['messages'][-1]
            debug_print(f"[{last_message.__class__.__name__}] {last_message.content}", verbose=self.verbose)
            yield f"[{last_message.__class__.__name__}] {last_message.content}"

#--------------- test
if __name__ == '__main__':
    agent = Agent()
    asyncio.run(agent.run_file_ops_agent("Create a default C++ project structure"))