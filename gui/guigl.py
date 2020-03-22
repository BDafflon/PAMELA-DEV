import math
import pyglet
from pyglet.gl import (
    Config,
    glEnable, glBlendFunc, glLoadIdentity, glClearColor,
    GL_BLEND, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, GL_COLOR_BUFFER_BIT, GL_POLYGON, gl, glVertex3f)

from pyglet.gl import (
    glPushMatrix, glPopMatrix, glBegin, glEnd, glColor3f,
    glVertex2f, glTranslatef, glRotatef,
    GL_LINE_LOOP, GL_LINES, GL_TRIANGLES)

from pyglet.window import key, mouse

# Define some colors
from pyglet.window.mouse import LEFT
from setuptools.msvc import winreg

from helper import util
from helper.vector2D import Vector2D

BLACK = [0, 0, 0]
WHITE = [1, 1, 1]
GREEN = [0, 1, 0]
RED = [1, 0, 0]
BLUE = [0, 0, 1]
_CHANGE_VECTOR_LENGTH = 15.0
colors = [BLACK, GREEN, RED, BLUE]


class GuiGL():
    def __init__(self, map):
        self.kill = False
        self.printFustrum = False
        self.printVel = False
        self.width = 1
        self.height = 1
        self.margin = 0
        self.environment = map
        self.title = "GUI"
        self.fullscreen = False;
        self.scaleFactor=1

    def get_window_config(self):
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_default_screen()

        template = Config(double_buffer=True, sample_buffers=1, samples=4)
        try:
            config = screen.get_best_config(template)
        except pyglet.window.NoSuchConfigException:
            template = Config()
            config = screen.get_best_config(template)

        return config

    def stop2(self):
        self.kill = True
        print("stop")

    def run2(self):
        show_debug = False
        show_vectors = False

        mouse_location = (0, 0)
        window = pyglet.window.Window(
            fullscreen=self.fullscreen,
            caption=self.title,
            resizable=True)

        window.set_minimum_size(1280,720)
        window.set_maximum_size(1280,720)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # window.push_handlers(pyglet.window.event.WindowEventLogger())

        def update(dt):
            self.environment.update(dt)

        # schedule world updates as often as possible
        pyglet.clock.schedule(update)


        @window.event
        def on_draw():
            if self.kill:
                pyglet.app.exit()

            glClearColor(0.1, 0.1, 0.1, 1.0)
            window.clear()
            glLoadIdentity()

            for b in self.environment.agents:
                self.drawAgent(b)
            for o in self.environment.objects:
                self.drawObject(o)

        @window.event
        def on_key_press(symbol, modifiers):
            if symbol == key.Q:

                pyglet.app.exit()
                return "toto"
            elif symbol == key.D:
                nonlocal show_debug
                show_debug = not show_debug
            elif symbol == key.V:
                nonlocal show_vectors
                show_vectors = not show_vectors

        @window.event
        def on_mouse_drag(x, y, *args):
            nonlocal mouse_location
            mouse_location = x, y

        @window.event
        def on_mouse_leave(x, y):
            o = self.environment.getFirstObjectByName("Attractor")
            print("leave")
            if o is not None:
                o.location = Vector2D(-1000, -1000)

        @window.event
        def on_mouse_release(x, y, button, modifiers):
            nonlocal mouse_location
            o = self.environment.getFirstObjectByName("Attractor")
            if o is not None:
                o.location = Vector2D(-1000, -1000)

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.LEFT:
                print("The Left Mouse Was Pressed")

            elif button == mouse.RIGHT:
                print("Right Mouse Was Pressed")

        @window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
            o = self.environment.getFirstObjectByName("Attractor")
            if o is not None:
                o.location = Vector2D(x, y)

        @window.event
        def on_mouse_motion(x, y, *args):
            nonlocal mouse_location
            mouse_location = x, y


        pyglet.app.run()

    def render_velocity(self, b):
        glColor3f(0.6, 0.6, 0.6)
        glBegin(GL_LINES)
        glVertex2f(0.0, 0.0)
        glVertex2f(0.0, b.body.fustrum.radius)
        glEnd()

    def render_view(self, b):
        glColor3f(0.6, 0.1, 0.1)
        glBegin(GL_LINE_LOOP)

        step = 10
        # render a circle for the boid's view
        for i in range(-b.body.fustrum.angle, b.body.fustrum.angle + step, step):
            glVertex2f(b.body.fustrum.radius/self.scaleFactor * math.sin(math.radians(i)),
                       (b.body.fustrum.radius/self.scaleFactor * math.cos(math.radians(i))))
        #glVertex2f(0.0, 0.0)
        glEnd()

    def render_agent(self, b):
        glBegin(GL_TRIANGLES)
        glColor3f(*colors[1])
        glVertex2f(-(5), 0.0)
        glVertex2f(5, 0.0)
        glVertex2f(0.0, 5 * 3.0)
        glEnd()

    def renderObject(self, b):
        glBegin(GL_POLYGON)
        glColor3f(*colors[1])
        glVertex2f(-(5), -5)
        glVertex2f(5, -5)
        glVertex2f(5, 5)
        glVertex2f(-5, 5)
        glEnd()

    def drawObject(self, o):
        glPushMatrix()
        # apply the transformation for the boid
        glTranslatef(o.location.x/self.scaleFactor, o.location.y/self.scaleFactor, 0.0)

        # render the object itself
        self.renderObject(o)
        glPopMatrix()

    def drawAgent(self, b):
        glPushMatrix()
        # apply the transformation for the boid
        glTranslatef(b.body.location.x/self.scaleFactor, b.body.location.y/self.scaleFactor, 0.0)

        # a = signedAngle()
        glRotatef(math.degrees(math.atan2(b.body.velocity.x, b.body.velocity.y)), 0.0, 0.0, -1.0)

        # render the boid's velocity
        if self.printVel:
            self.render_velocity(b)

        # render the boid's view
        if self.printFustrum:
            self.render_view(b)

        # render the boid itself
        self.render_agent(b)
        glPopMatrix()

