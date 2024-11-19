import pygame
import time
from typing import Tuple, List
from .offset import Offset2D
from ..physic import Body, System

class Ui:
    DIMENSION = 2
    """This render can only render 2D.
    """

    def __init__(self,
                 system: System,
                 *,
                 screen_size: Tuple[int, int],
                 background_color: Tuple [int, int, int] = (255, 255, 255),
                 fps: int = 60,
                 step_per_render: int = 1,
                 offset: Tuple[int, int] = (0, 0),
                 scale: float = 1
                 ) -> None:
        # register system
        self.system = system

        # init pygame
        pygame.init()
        self.screen_size = screen_size
        self.w, self.h = self.screen_size
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Render Objects")
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.running = True
        self.paused = False

        # params
        self.bg_color = background_color
        self.offset = offset if isinstance(offset, Offset2D) else Offset2D(offset)
        self.scale = scale
        self.step_per_render = step_per_render

        # handle event
        self.mouse_pos = None

    def _handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:      # HANDLE KEY PRESS
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == 1073741911:       # Key +
                    self.step_per_render += 1
                elif event.key == 1073741910:       # Key -
                    self.step_per_render = max(1, self.step_per_render - 1)
                elif event.key == 97:               # A
                    print(f"Number of planets : {len(self.system.bodies)}")
                else:
                    print(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_pos = pygame.mouse.get_pos()

            elif event.type == pygame.MOUSEBUTTONUP:
                new_pos = pygame.mouse.get_pos()
                if event.button == 1 and self.mouse_pos is not None:
                    offset = (new_pos[0] - self.mouse_pos[0], new_pos[1] - self.mouse_pos[1])
                    self.offset.set((
                        self.offset.x - offset[0] / self.scale,
                        self.offset.y - offset[1] / self.scale))

            elif event.type == pygame.MOUSEWHEEL:
                scale_factor = 0.9 if event.y == 1 else 1.1
                self.scale *= scale_factor

    def render_frame(self, bodies: List[Body]) -> None:
        self.screen.fill(self.bg_color)
        for obj in bodies:
            x = obj.position.coords[0] / self.scale - self.offset.x
            y = obj.position.coords[1] / self.scale - self.offset.y
            pygame.draw.circle(self.screen, (0, 0, 255), (int(x), int(y)), int(obj.radius / self.scale))
        pygame.display.update()

    def single_step(self):
        try:
            # calc loop render time
            start = time.time()

            # render the frame
            self.render_frame(self.system.bodies)

            # engine calulate new position
            self.system.run_n_step(self.step_per_render)

            # print(f"Frame rendered in {time.time() - start}")

        except KeyboardInterrupt:
            print("USER STOP RENDERING")
            self.running = False

    def run(self) -> None:
        while self.running:
            # ensure constant frame rate
            self.clock.tick(self.fps)

            # handle input
            self._handle_input()

            # display only if not pause
            if not self.paused:
                self.single_step()
