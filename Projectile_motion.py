import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import scipy.integrate as integrate

FPS = 120.0
TIME = 12.0

def on_close(event):
    plt.close()

class Projectile:
    def __init__(self, v0, angle, a):
        self.v0 = v0
        self.angle = angle
        self.angle = np.deg2rad(angle)
        self.v0 = np.array([[self.v0*np.cos(self.angle)], [self.v0*np.sin(self.angle)]])
        self.g = a
        self.state = [0.0, self.v0[1], 0.0, self.v0[0]]
        self.dt = 0.05
        self.t = np.arange(0.0, TIME, self.dt)
        self.limit = 0

    def fdy(self, state, t):
        #initial conditions
        y = state[0]
        dy = state[1]
        x = state[2]
        dx = state[3]
        #model equations
        ddt = [[], [], [], []]
        ddt[0] = dy
        ddt[1] = self.g*(-1)
        ddt[2] = dx
        ddt[3] = 0
        return ddt

    def simulate(self):
        self.sol = integrate.odeint(self.fdy, self.state, self.t)

    def draw(self):
        for i in range(len(self.sol[:, 0])):
            if self.sol[i, 0] < 0.0:
                self.limit = i
                break

        plt.plot(self.sol[0 : self.limit, 2], self.sol[0  :self.limit, 0], 'g--')
        plt.ylabel('y[m]')
        plt.xlabel('x[m]')

    def animate(self, fig, ax, color):
        def increment(i):
            if self.sol[[0] + i, 0] > 0:
                self.line.set_xdata(self.sol[[0] + i, 2])
                self.line.set_ydata(self.sol[[0] + i, 0])
            plt.title('Czas: ' + format(i * 0.05, '.2f') + '[s]')
            return self.line
        self.draw()
        self.line, = ax.plot([0], self.sol[[0], 2], color, marker = 'o', markersize = 10)
        self.ani = FuncAnimation(fig, increment, np.arange(1, int(TIME/0.05)), interval = (1/FPS))

fig, ax = plt.subplots()
plt.axhline(y = 0.0, color = 'black', linestyle = '-')
ax.set_autoscale_on(True)
fig.canvas.mpl_connect('close_event', on_close)

projectile_earth = Projectile(30, 45, 9.81)
projectile_earth.simulate()
projectile_earth.animate(fig, ax, 'b')

projectile_mars = Projectile(30, 45, 3.721)
projectile_mars.simulate()
projectile_mars.animate(fig, ax, 'r')

projectile_jupiter = Projectile(30, 45, 24.79)
projectile_jupiter.simulate()
projectile_jupiter.animate(fig, ax, 'y')

plt.show()