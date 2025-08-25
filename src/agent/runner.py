import asyncio
from .graph import create_file_ops_graph


async def run_file_ops_agent(user_message: str):
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
    
    print("Starting conversation...")
    async for event in graph.astream({'messages': msgs}, stream_mode='values'):
        last_message = event['messages'][-1]
        print(f"[{last_message.__class__.__name__}] {last_message.content}")
        
        # 툴 호출이 있는지 확인
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            print(f"Tool calls: {last_message.tool_calls}")
    
    print("Conversation ended.")
