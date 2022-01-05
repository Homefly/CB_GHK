import matplotlib.pyplot as plt

class RTPlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots()  # Create a figure containing a single axes.
        plt.ion()
        plt.show(block=False)
        
    def updatePlot(self, history):
        z = list(map(float, history.getData['price'].iloc[-600:]))
        x = list(map(float, history.getData['predX'].iloc[-600:]))
        plt.cla()
        self.ax.plot(z)
        self.ax.plot(x)
        plt.pause(0.01)