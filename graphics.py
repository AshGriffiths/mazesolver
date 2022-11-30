from tkinter import Tk, BOTH, Canvas


class Point(object):
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class Line(object):
    def __init__(self, p1: Point, p2: Point):
        self.__p1: Point = p1
        self.__p2: Point = p2

    def draw(self, canvas: Canvas, fill_colour: str) -> None:
        canvas.create_line(
            self.__p1.x,
            self.__p1.y,
            self.__p2.x,
            self.__p2.y,
            fill=fill_colour,
            width=2,
        )
        canvas.pack(fill=BOTH, expand=1)


class Window(object):
    def __init__(self, width: int, height: int):
        self.__root = Tk()
        self.__root.title("Maze Solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running: bool = False

    def is_running(self) -> bool:
        return self.__running

    def set_running(self, state: bool) -> None:
        self.__running = state

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.set_running(True)
        while self.is_running():
            self.redraw()
        print("window closed...")

    def close(self) -> None:
        self.set_running(False)

    def draw_line(self, line: Line, fill_colour: str = "black") -> None:
        line.draw(self.__canvas, fill_colour)