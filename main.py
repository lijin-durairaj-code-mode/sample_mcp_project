import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

SERVERS = {
    "calculator": {
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

_prompts = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
You are a helpful AI assistant.

You have access to calculator tools that can perform mathematical operations.

Your behavior should follow these rules:

1. General Questions:
- If the user asks general knowledge, explanations, or casual questions, answer normally in a clear and helpful way.

2. Calculations:
- If the user asks anything involving math, numbers, arithmetic, or calculations (e.g., addition, subtraction, percentages, formulas, etc.), you MUST use the calculator tools.
- Do NOT calculate manually if a tool is available.
- Always prefer tool usage for accuracy.

3. Mixed Queries:
- If a question contains both explanation and calculation, use the tool for the calculation part and explain the result clearly.

4. Clarity:
- Keep answers simple, clear, and concise.
- Show the final answer clearly.

5. Strict Rule:
- Never guess or approximate calculations when a tool is available.
- Always rely on tools for numerical results.

Examples:
- User: "What is 25 * 18?"
  → Use calculator tool

- User: "Explain what inflation is"
  → Answer normally

- User: "If I earn 5000 and spend 1200, how much is left?"
  → Use calculator tool, then explain result

You are reliable, accurate, and tool-aware.
     """,
        ),
        ("human", "{user_input}"),
    ]
)


async def main():
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    llm = HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.1-8B-Instruct", task="text-generation"
    )

    model = ChatHuggingFace(llm=llm)
    model.bind_tools(tools)

    llm_chain = _prompts | model
    response = await llm_chain.ainvoke({"user_input": "how much is 4 + 9"})

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
