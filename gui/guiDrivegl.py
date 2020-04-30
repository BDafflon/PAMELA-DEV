from pyglet import image
from pyglet.gl import (
    glBegin, glEnd, glColor3f,
    glVertex2f, GL_TRIANGLES, GL_POLYGON)

from environment.application.Drive.agentState import AgentState
from environment.application.Drive.agentType import AgentType
from gui.guigl import GuiGL

# Define some colors

BLACK = [0, 0, 0]
WHITE = [1, 1, 1]
GREEN = [0, 1, 0]
RED = [1, 0, 0]
BLUE = [0, 0, 1]
_CHANGE_VECTOR_LENGTH = 15.0
colors = [BLACK, GREEN, RED, BLUE]


class GuiDriveGL(GuiGL):
    def __init__(self, map):
        GuiGL.__init__(self, map)
        self.title = "GUI Drive Simulation"
        self.txt =""



    def render_agent(self, b):
        glBegin(GL_TRIANGLES)
        if b.stat == AgentState.SEIN:
            glColor3f(*colors[1])
        else:
            if b.stat == AgentState.INFECTE:
                glColor3f(*colors[2])
            else:
                if b.stat == AgentState.RETABLI:
                    glColor3f(*colors[3])
                else:
                    if b.stat == AgentState.MORT:
                        glColor3f(*colors[0])

        glVertex2f(-(5)/ self.scaleFactor, 0.0)
        glVertex2f(5/ self.scaleFactor, 0.0)
        glVertex2f(0.0, 5 * 3.0/ self.scaleFactor)
        glEnd()


    def renderObject(self, b):
        glBegin(GL_POLYGON)
        glColor3f(*colors[1])

        w = 10/ self.scaleFactor
        h = 10/ self.scaleFactor



        if b.type == "Wall":

            h = b.aabb.height/ self.scaleFactor
            w = b.aabb.width/ self.scaleFactor
            glColor3f(*colors[0])


        else:
            if b.type == "Dropoff":
                h = b.aabb.height/ self.scaleFactor
                w = b.aabb.width/ self.scaleFactor

                glColor3f(*colors[2])

            else:
                if b.type == "Pickup":
                    h = b.aabb.height/ self.scaleFactor
                    w = b.aabb.width/ self.scaleFactor

                    glColor3f(*colors[3])

        glVertex2f(0, 0)
        glVertex2f(w, 0)
        glVertex2f(w, h)
        glVertex2f(0, h)

        glEnd()
