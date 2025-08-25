from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode

from .tools.fs_tools import create_directory_tool, write_file_tool, get_workspace_info, list_directory_tool
from .nodes import chatbot_node, should_continue


def create_file_ops_graph():
    """파일 조작을 위한 LangGraph를 생성합니다."""
    graph_builder = StateGraph(MessagesState)

    tools = [create_directory_tool, write_file_tool, get_workspace_info, list_directory_tool]

    # 노드 함수들을 툴과 함께 사용할 수 있도록 래퍼 생성
    async def chatbot(state: MessagesState):
        return await chatbot_node(state, tools)

    # 노드 추가
    tool_node = ToolNode(tools)
    graph_builder.add_node('chatbot', chatbot)
    graph_builder.add_node('tools', tool_node)
    
    # 엣지 추가
    graph_builder.add_edge(START, 'chatbot')
    graph_builder.add_conditional_edges('chatbot', should_continue, {'tools': 'tools', END: END})
    graph_builder.add_edge('tools', 'chatbot')

    return graph_builder.compile()
