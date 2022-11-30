from graphics import Line, Point, Window


class Cell(object):
    def __init__(self, win: Window):
        self.has_left_wall: bool = True
        self.has_right_wall: bool = True
        self.has_top_wall: bool = True
        self.has_bottom_wall: bool = True
        self.visited: bool = False
        self._x1: int | None = None
        self._x2: int | None = None
        self._y1: int | None = None
        self._y2: int | None = None
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
