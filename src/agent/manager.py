
import asyncio
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List
from agent.runner import Agent
from controller import Controller

from prompt_toolkit.application import get_app

class AppStatus(Enum):
    RUNNING = auto() # agent running
    PENDING = auto() # waiting user input
    STOPPED = auto() # App stopped

@dataclass
class AppState:
    status: AppStatus = AppStatus.STOPPED
    logs: List[str] = field(default_factory=list)
    

class AppManager:
    def __init__(self):
        # 컴포넌트들 초기화
        from ui.renderer import Renderer  # 순환참조 방지: 지연 import
        self.renderer = Renderer()
        self.agent = Agent()
        self.controller = Controller(self.renderer)

        self.state = AppState()  # 생성자 호출로 변경
        self.queue = self.renderer.queue
        self._stop = asyncio.Event()
        self._app = self.renderer.application()
    
    @property
    def status(self) -> AppStatus:
        return self.state.status
    
    @status.setter
    def status(self, value: AppStatus):
        self.state.status = value
    
    async def run(self):
        """애플리케이션 실행"""
        # UI 태스크와 Agent 처리 태스크 동시 실행
        self.status = AppStatus.PENDING
        await asyncio.gather(
            self._ui_task(),
            self._agent_loop()
        )
    
    async def _ui_task(self):
        """UI 실행"""
        await self._app.run_async()
    
    async def _agent_loop(self):
        """Agent 작업 처리 루프"""
        while not self._stop.is_set():
            try:
                user_input = await asyncio.wait_for(self.queue.get(), timeout=0.1)
            except asyncio.TimeoutError:
                continue

            self.status = AppStatus.PENDING
            if user_input is not None:
                # 내부 명령어(quit 등) 처리
                self._process_user_input(user_input)
                
                if self.status != AppStatus.STOPPED:
                    self.status = AppStatus.RUNNING
                    async for msg in self.agent.run_file_ops_agent(user_input):
                        self.state.logs.append(msg)
                        if get_app().is_running:
                            self.renderer.render(self.state)

            # 입력 대기 중에도 상태 반영
            if get_app().is_running:
                self.renderer.render(self.state)
    
    def _process_user_input(self, user_input: str):
        cmd = user_input.strip()
        if not cmd:
            return
        if cmd == 'quit':
            self.status = AppStatus.STOPPED
            