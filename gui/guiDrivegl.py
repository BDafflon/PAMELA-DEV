from pyglet.gl import (
    glBegin, glEnd, glColor3f,
    glVertex2f, GL_TRIANGLES)

from gui.guigl import GuiGL

# Define some colors

BLACK = [0, 0, 0]
WHITE = [1, 1, 1]
GREEN = [0, 1, 0]
RED = [1, 0, 0]
BLUE = [0, 0, 1]
_CHANGE_VECTOR_LENGTH = 15.0
colors = [WHITE, GREEN, RED, BLUE]


class GuiDriveGL(GuiGL):
    def __init__(self, map):
        GuiGL.__init__(self, map)
        self.title = "GUI Boids Simulation"

    def render_agent(self, b):
        glBegin(GL_TRIANGLES)
        if b.type == "Robot":
            glColor3f(*colors[1])
        else:
            if b.type == "StandardAgent":
                glColor3f(*colors[2])
        glVertex2f(-(5), 0.0)
        glVertex2f(5, 0.0)
        glVertex2f(0.0, 5 * 3.0)
        glEnd()
