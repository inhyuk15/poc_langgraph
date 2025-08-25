from ui.renderer import Renderer

class Controller:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.queue = self.renderer.queue