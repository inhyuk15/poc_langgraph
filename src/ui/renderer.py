import asyncio
from prompt_toolkit.widgets import TextArea, Frame
from prompt_toolkit.layout import VSplit, HSplit, Layout
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.application.current import get_app



class Renderer:
    """
    - renderer(state): TextArea에 텍스트 반영
    - get_user_input(): 입력창 내용을 가져오고 비우기
    """
    def __init__(self):
        self.log_area = TextArea(text='', scrollbar=True, read_only=True)
        self.status_area = TextArea(text='Status: -', read_only=True)

        self.input_area = TextArea(scrollbar=True, height=1, prompt="> ", multiline=False)
        self.queue = asyncio.Queue()
        
        main_area = VSplit([
            Frame(self.log_area, title="Chat"),
            Frame(self.status_area, title='Status', width=20)
        ])
        root = HSplit([main_area, Frame(self.input_area, title="Input")])

        self.kb = KeyBindings()
        self.app = Application(layout=Layout(root), key_bindings=self.kb, full_screen=True)
        self.set_focus_input()

        # 기본 엔터 입력 바인딩
        @self.kb.add('enter')
        async def _(event):
            text = self.get_user_input()
            await self.queue.put(text)

        @self.kb.add('c-c')
        async def _(event):
            event.app.exit()

    def set_focus_input(self):
        self.app.layout.focus(self.input_area)
    
    def application(self) -> Application:
        return self.app
    
    def render(self, state):
        # AppStatus는 state.status의 타입이므로 문자열 비교로 대체
        self.log_area.text = '\n'.join(state.logs[-100:])
        self.status_area.text = f'status: {str(state.status)}'
        get_app().invalidate()
    
    def get_user_input(self) -> str:
        text = self.input_area.text
        self.input_area.text = ''
        return text
    