from tkinter import Tk, BOTH, Canvas
from typing import Optional


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


class Cell(object):
    def __init__(self, win: Window):
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self.visited: bool = False
        self._x1: Optional[int] = None
        self._x2: Optional[int] = None
        self._y1: Optional[int] = None
        self._y2: Optional[int] = None
        self._win: Window = win

    def draw(self, x1: int, y1: int, x2: int, y2: int):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self._win.draw_line(line)
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self._win.draw_line(line)
        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self._win.draw_line(line)
        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self._win.draw_line(line)

    def draw_move(self, to_cell, undo: bool = False):
        if self._win is None:
            return
        if self._x1 and self._y1 and self._x2 and self._y2:
            x_mid = (self._x1 + self._x2) // 2
            y_mid = (self._y1 + self._y2) // 2

            to_x_mid = (to_cell._x1 + to_cell._x2) // 2
            to_y_mid = (to_cell._y1 + to_cell._y2) // 2

            fill_colour = "red"
            if undo:
                fill_colour = "gray"

            # moving left
            if self._x1 > to_cell._x1:
                line = Line(Point(self._x1, y_mid), Point(x_mid, y_mid))
                self._win.draw_line(line, fill_colour)
                line = Line(Point(to_x_mid, to_y_mid), Point(to_cell._x2, to_y_mid))
                self._win.draw_line(line, fill_colour)

            # moving right
            elif self._x1 < to_cell._x1:
                line = Line(Point(x_mid, y_mid), Point(self._x2, y_mid))
                self._win.draw_line(line, fill_colour)
                line = Line(Point(to_cell._x1, to_y_mid), Point(to_x_mid, to_y_mid))
                self._win.draw_line(line, fill_colour)

            # moving up
            elif self._y1 > to_cell._y1:
                line = Line(Point(x_mid, y_mid), Point(x_mid, self._y1))
                self._win.draw_line(line, fill_colour)
                line = Line(Point(to_x_mid, to_cell._y2), Point(to_x_mid, to_y_mid))
                self._win.draw_line(line, fill_colour)

            # moving down
            elif self._y1 < to_cell._y1:
                line = Line(Point(x_mid, y_mid), Point(x_mid, self._y2))
                self._win.draw_line(line, fill_colour)
                line = Line(Point(to_x_mid, to_y_mid), Point(to_x_mid, to_cell._y1))
                self._win.draw_line(line, fill_colour)


def main() -> None:
    win = Window(800, 600)
    c1 = Cell(win)
    c1.has_right_wall = False
    c1.draw(50, 50, 100, 100)

    c2 = Cell(win)
    c2.has_left_wall = False
    c2.has_bottom_wall = False
    c2.draw(100, 50, 150, 100)

    c1.draw_move(c2)

    c3 = Cell(win)
    c3.has_top_wall = False
    c3.has_right_wall = False
    c3.draw(100, 100, 150, 150)

    c2.draw_move(c3)

    c4 = Cell(win)
    c4.has_left_wall = False
    c4.draw(150, 100, 200, 150)

    c3.draw_move(c4, True)
    win.wait_for_close()


if __name__ == "__main__":
    main()
