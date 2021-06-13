from matplotlib.patches import Ellipse

class DraggablePoint:
    lock = None
    def __init__(self, parent, x=0.1, y=0.1, size=0.1):

        self.parent = parent
        self.point = Ellipse((x, y), size, size, fc='r', alpha=0.5, edgecolor='r')
        self.x = x
        self.y = y

        parent.mapCanvas.figure.axes[0].add_patch(self.point)
        self.press = None
        self.background = None
    def get_point(self):
        return self.point