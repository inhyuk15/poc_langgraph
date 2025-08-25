import asyncio
from contextlib import AsyncExitStack, contextmanager, asynccontextmanager
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = {
    "command": "npx",
    "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "."
    ],
}

class MCPFileHandler:
    def __init__(self):
        self.path = ''

    @asynccontextmanager
    async def aopen(self, path: str='.'):
        self.path = os.path.abspath(path)
        params = list(server_params['args'])
        params[-1] = self.path

        params = StdioServerParameters(
            command=server_params["command"],
            args=params,
            env=None
        )

        async with AsyncExitStack() as stack:
            stdio, write = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(stdio, write))
            await session.initialize()
            yield session

#------------ test
async def main():
    fs = MCPFileHandler()
    async with fs.aopen('.') as session:
        tools = await session.list_tools()
        print("tools:")
        print(list(tool.name for tool in tools.tools))

if __name__ == "__main__":
    asyncio.run(main())