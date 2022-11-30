import time

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
            fill_colour = "red"
            if undo:
                fill_colour = "gray"
            x_mid = (self._x1 + self._x2) // 2
            y_mid = (self._y1 + self._y2) // 2
            to_x_mid = (to_cell._x1 + to_cell._x2) // 2
            to_y_mid = (to_cell._y1 + to_cell._y2) // 2
            if self._x1 > to_cell._x1:
                line = Line(Point(self._x1, y_mid), Point(x_mid, y_mid))
                self._win.draw_line(line, fill_colour)
                line = Line(Point(to_x_mid, to_y_mid), Point(to_cell._x2, to_y_mid))
                self._win.draw_line(line, fill_colour)
            elif self._x1 < to_cell._x1:
                line = Line(Point(x_mid, y_mid), Point(self._x2, y_mid))
                self._win.draw_line(line, fill_colour)
                line = Line(Point(to_cell._x1, to_y_mid), Point(to_x_mid, to_y_mid))
                self._win.draw_line(line, fill_colour)
            elif self._y1 > to_cell._y1:
                line = Line(Point(x_mid, y_mid), Point(x_mid, self._y1))
                self._win.draw_line(line, fill_colour)
                line = Line(Point(to_x_mid, to_cell._y2), Point(to_x_mid, to_y_mid))
                self._win.draw_line(line, fill_colour)
            elif self._y1 < to_cell._y1:
                line = Line(Point(x_mid, y_mid), Point(x_mid, self._y2))
                self._win.draw_line(line, fill_colour)
                line = Line(Point(to_x_mid, to_y_mid), Point(to_x_mid, to_cell._y1))
                self._win.draw_line(line, fill_colour)


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win,
    ):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._create_cells()

    def _create_cells(self):
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                col_cells.append(Cell(self._win))
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)


def main() -> None:
    num_rows = 12
    num_cols = 16
    margin = 50
    screen_x = 800
    screen_y = 600
    cell_size_x = (screen_x - 2 * margin) / num_cols
    cell_size_y = (screen_y - 2 * margin) / num_rows
    win = Window(screen_x, screen_y)
    Maze(margin, margin, num_rows, num_cols, cell_size_x, cell_size_y, win)
    win.wait_for_close()


if __name__ == "__main__":
    main()
