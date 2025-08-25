"""
LangGraph 노드들을 정의하는 모듈
"""

from langgraph.graph import MessagesState, END
from langchain.chat_models import init_chat_model


async def chatbot_node(state: MessagesState, tools: list):
    """LLM과의 대화를 처리하는 노드입니다."""
    llm = init_chat_model('openai:gpt-4o').bind_tools(tools)
    ai_msg = await llm.ainvoke(state['messages'])
    return {'messages': [ai_msg]}


def should_continue(state: MessagesState):
    """다음 노드를 결정하는 조건 함수입니다."""
    last_message = state['messages'][-1]
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return 'tools'
    return END
