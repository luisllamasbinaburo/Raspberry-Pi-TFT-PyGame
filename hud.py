import sys, math, pygame, random, time, os
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT
from operator import itemgetter

import getpass
if getpass.getuser() != 'root': sys.exit("Must be run as root.")

class Renderer:
    def __init__(self, win_width = 240, win_height = 320):       
        os.putenv('SDL_FBDEV',   '/dev/fb1')
        pygame.init()
        pygame.mouse.set_visible(False)
        
        pygame.display.set_caption("Rendering")
        self.screen = pygame.display.set_mode((win_width, win_height))
        self.clock = pygame.time.Clock()

        self.font_size = 24
        self.font = pygame.font.SysFont(None, 24)

        self.background_color = (30, 30, 30)
        self.outline_color = (255, 255, 255)
        self.fill_color = (0, 255, 0)
        self.font_color = (255, 255, 255)

        self.value = 50.0
        self.max_value = 100.0
        self.radius = 100
        self.thickness = 20
        self.center_x = win_width // 2
        self.center_y = win_height // 2
  
    def draw(self):
        angle = math.radians(360 * self.value / self.max_value)

        end_x = int(self.center_x + self.radius * math.sin(angle))
        end_y = int(self.center_y - self.radius * math.cos(angle))

        self.screen.fill(self.background_color)

        pygame.draw.circle(self.screen, self.outline_color, (self.center_x, self.center_y), self.radius, self.thickness)
        pygame.draw.arc(self.screen, self.fill_color, (self.center_x - self.radius, self.center_y - self.radius, self.radius * 2, self.radius * 2), - math.pi / 2, angle - math.pi / 2, self.thickness)

        text = self.font.render(f"{self.value:.1f}/{self.max_value:.1f}", True, self.font_color)
        text_rect = text.get_rect(center=(self.center_x, self.center_y))
        self.screen.blit(text, text_rect)

    def run(self):       
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.value += 0.1
            self.draw()
            pygame.display.flip()
           
            self.clock.tick(60)

if __name__ == "__main__":
    Renderer().run()