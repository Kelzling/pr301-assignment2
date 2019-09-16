from TIGr import AbstractDrawer
import turtle

'''
Output Interpreted Commands with Turtle.py
Class Written by Kelsey Vavasour and Thomas Baines
Doctests Written by Kelsey Vavasour and Jess Ward
'''


class TurtleDrawer(AbstractDrawer):
    """ Concretion of AbstractDrawer using the Turtle library to execute drawing commands """
    def __init__(self):
        self.my_turtle = turtle.Turtle()
        self.pen_colours = ("black", "red", "orange", "yellow", "green", "blue", "indigo", "violet")
        # TODO add dictionary of "directions" corresponding to their degrees - used in the go_down and go_along

    def select_pen(self, pen_num):
        """
        Sets the pen colour, between 0 and 7 (black and the colours of the rainbow)
        >>> t.select_pen(2)
        >>> t.select_pen(-5) #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Pen number was -5, must be between 0 and 7
        >>> t.select_pen(9) #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Pen number was 9, must be between 0 and 7
        """
        if pen_num in range(0, len(self.pen_colours) - 1):
            self.my_turtle.pencolor(self.pen_colours[pen_num])
            return f"Set Pen Colour To {self.pen_colours[pen_num]}"
        else:
            raise ValueError(f"Pen Number was {pen_num}, must be between 0 and {len(self.pen_colours) - 1}")

    def pen_down(self):
        self.my_turtle.pendown()
        return "Pen Down"

    def pen_up(self):
        self.my_turtle.penup()
        return "Pen Up"

    def go_along(self, along):
        """ if along is negative, this will move backwards
        :param int along: the distance to travel
         >>> t.go_along(20)
         >>> t.go_along(-200)
         """
        self.my_turtle.setheading(0)
        self.my_turtle.forward(along)
        return f"Moved Pen Along {along}"

    def go_down(self, down):
        """
        if down is negative, the turtle will move up
        :param int down: the distance to travel
        :return:
        >>> t.go_down(42)
        >>> t.go_down(-50)
        """
        self.my_turtle.setheading(270)
        self.my_turtle.forward(down)
        return f"Moved Pen Down {down}"

    def draw_line(self, direction, distance):
        """
        Draws a line of given distance pointing in the provided direction
        :param int direction: the heading to face, in degrees (must be between 0 - 360)
        :param int distance: the distance to travel
        :return:
        >>> t.draw_line(72, 90)
        >>> t.draw_line(666, 42) #doctest: +IGNORE_EXCEPTION_DETAIL
        Traceback (most recent call last):
        ValueError: Direction given was 666, must be between 0 - 360
        >>> t.draw_line(-75, 43)
        Traceback (most recent call last):
        ValueError: Direction given was -75, must be between 0 - 360
        >>> t.draw_line(45, -100)
        """
        if direction in range(0, 360):
            self.my_turtle.setheading(direction)
            self.my_turtle.forward(distance)
            return f"Moved Pen {distance} in direction {direction}"
        else:
            raise ValueError(f"Direction given was {direction}, must be between 0 - 360")


if __name__ == "__main__":
    import doctest
    doctest.testmod(extraglobs={'t': TurtleDrawer()}, verbose=True)
