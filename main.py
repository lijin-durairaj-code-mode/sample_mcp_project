import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain.agents import create_react_agent
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain_core.messages import HumanMessage
from langchain_core.output_parsers import StrOutputParser
import json

from prompts.llm_prompts import _prompts, final_response_prompt

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


_question = "how much is 5 plus 3"

final_llm = HuggingFaceEndpoint(repo_id="meta-llama/Llama-3.1-8B-Instruct")

final_result_model = ChatHuggingFace(llm=final_llm)


async def main():
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()
    tool_map = {tool.name: tool for tool in tools}
    llm = HuggingFaceEndpoint(repo_id="Qwen/Qwen2.5-7B-Instruct")

    model = ChatHuggingFace(llm=llm)
    model_with_tools = model.bind_tools(tools)
    model = _prompts | model_with_tools
    response = await model.ainvoke({"user_input": _question})

    tool_messages = []
    for response_tools in response.tool_calls:

        func_name = response_tools["name"]
        func_args = response_tools.get("args") or {}
        func_id = response_tools["id"]
        result = await tool_map[func_name].ainvoke(func_args)
        tool_messages.append(
            ToolMessage(tool_call_id=func_id, content=json.dumps(result))
        )

    final_response_prompt.format(question=_question, context=result)
    fr = final_response_prompt | final_result_model | StrOutputParser()
    result = await fr.ainvoke({"question": _question, "context": result})

    print(result)


if __name__ == "__main__":
    asyncio.run(main())
