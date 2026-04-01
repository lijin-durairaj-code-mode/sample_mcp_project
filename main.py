import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

SERVERS = {
    "math": {
        "transport": "stdio",
        "command": "uv",
        "args": [
            "run",
            "fastmcp",
            "run",
            "D:/projects/simple_mcp_app/calculator_agent.py",
        ],
    }
}


async def main():
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    print(tools)


if __name__ == "__main__":
    asyncio.run(main())
