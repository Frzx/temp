import os
import asyncio
import httpx

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4.1-mini")
MCP_TOKEN = "RHXzMF7x6dXlhSQ9UeEFSu6BNiP-PZE4yJgu_Ij9FR8"

async def main():
    async with httpx.AsyncClient(
        headers={"Authorization": f"Bearer {MCP_TOKEN}"}
    ) as http_client:
        async with streamable_http_client(
            url="http://localhost:3000/mcp",
            http_client=http_client,
        ) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await load_mcp_tools(session)
                agent = create_agent(
                    model=llm,
                    tools=tools,
                )

                result = await agent.ainvoke(
                    {"messages": [{"role": "user", "content": "give me all the databases available. And at least three rows of a table from any database"}]}
                )
                print(result["messages"][-1].content)

asyncio.run(main())