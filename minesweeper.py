from turtle import mode, tracer, color, write, goto, update, done, rt, fd, lt, up, down, fillcolor, begin_fill, end_fill, write, pencolor, circle, pensize, pos, setpos, setup, ht
from mouse_handler import *
import random

class Field:
    def __init__(self, pos, covered=True, number=0, mine=False, marked=False):
        self._pos = pos
        self._covered = covered
        self._number = number
        self._mine = mine
        self._marked = marked 
        self._neighbours = []
        
    def uncover(self):
        self._covered = False

    def mark(self):
        self._marked = not self._marked

    def set_mine(self):
        self._mine = True

    def set_number(self, number):
        self._number = number

    def set_neighbours(self, neighbours):
        self._neighbours = neighbours

    def covered(self):
        return self._covered
    
    def number(self):
        return self._number

    def mine(self):
        return self._mine

    def marked(self):
        return self._marked

    def neighbours(self):
        return self._neighbours

    def pos(self):
        return self._pos


def ini_graphics(board_height, board_width):
    mode("logo")
    setup(board_width, board_height)
    tracer(0, 0)
    ht()


def hop(dx, dy):
    up()

    fd(dy)
    rt(90)
    fd(dx)
    lt(90)

    down()


def ahop(dx, dy):
    up()

    rt(90)
    fd(dx)
    lt(90)
    fd(dy)

    down()


def draw_field(field_color, field_height, field_width):
    fillcolor(field_color)
    begin_fill()
    for i in range(2):
        fd(field_height);rt(90)
        fd(field_width);rt(90)
    end_fill()
    fillcolor('black')


def draw_cricle(mine_color, field_height, field_width, radius):
    fillcolor(mine_color)
    posx, posy = pos()
    hop(field_width//2+radius,field_height//2)
    begin_fill()
    circle(radius)
    end_fill()
    hop(-(field_width//2+radius),-field_height//2)
    up()
    setpos(posx, posy) # because of rounding when height of field is odd
    down()
    fillcolor('black')


def draw_mine(field_height, field_width):
    draw_cricle('red', field_height, field_width, field_height/4)


def draw_mark(field_height, field_width):
    draw_cricle('brown', field_height, field_width, field_height/8)


def draw_cross(field_height, field_width):
    pensize(3)
    posx, posy = pos()
    goto(posx + field_width, posy + field_height)
    hop(-field_width, 0)
    goto(posx + field_width, posy)
    hop(-field_width, 0)
    pensize(1)


def draw_number(number, field_height, field_width):
    dx = field_width//2
    dy = field_height//2
    hop(dx, dy)
    write(number, move=False, align="center", font=("Arial", 8, "normal"))
    hop(-dx, -dy)


def draw_game_info(board_width, board_height, font_size, info):
    dy = board_height
    hop(0, dy+1)
    pencolor('white')
    draw_field('white', font_size*3, board_width)

    pencolor('black') 
    dx = board_width//2
    hop(dx, font_size)
    write(info, move=False, align="center", font=("Arial", font_size, "normal"))

    hop(-dx, -(dy+font_size+1))


def mark_field(field_height, field_width, field, left_mines):
    if left_mines == 0:
        return 0
    if field.covered():
        field.mark()
        if field.marked():
            draw_mark(field_height, field_width)
            return left_mines - 1
        else:
            draw_field("chartreuse", field_height, field_width)
            return left_mines + 1
    return left_mines


def uncover_field(field_height, field_width, field):
    (dx,dy) = field_to_left_down_coordinates(field.pos()[0], field.pos()[1], field_height, field_width)
    hop(dx, dy)
    field.uncover()
    draw_field('greenyellow', field_height, field_width)
    if field.mine():
        draw_mine(field_height, field_width)
        if field.marked():
            draw_mark(field_height, field_width)
            hop(-dx, -dy)
            return True
        hop(-dx, -dy)
        return False
    elif field.marked():
        draw_mark(field_height, field_width)
        draw_cross(field_height, field_width)
        hop(-dx, -dy)
        return False
    elif field.number() > 0:
        draw_number(field.number(), field_height, field_width)
        hop(-dx, -dy)
        return True
    else: 
        hop(-dx, -dy)
        return uncover_area(field_height, field_width, field)


def uncover_area(field_height, field_width, field):
    win = True
    list_to_check = [field]
    while len(list_to_check) > 0:
        field = list_to_check[0]
        list_to_check.remove(field)
        neighbours = field.neighbours()
        for n in neighbours:
            if n.covered():
                if not n.marked():
                    if not uncover_field(field_height, field_width, n):
                        win = False
                if n.number() == 0:
                    list_to_check.append(n)
    return win
    

def uncover_all_fields(fields, field_height, field_width):
    win = True
    nrows = len(fields)
    ncols = len(fields[0])
    for row in range(nrows):
        for col in range(ncols):
            if not uncover_field(field_height, field_width, fields[row][col]):
                win = False
    if win:
        info = "YOU WIN!"
    else:
        info = "YOU LOSE!"
    draw_game_info(ncols*field_width, nrows*field_height, 12, info)


def draw_board(field_height, field_width, board_height, board_width, all_mines):
    # align to start positiom
    dy = field_height*board_height//2
    dx = field_width*board_width//2
    rt(180)
    hop(dx, dy)
    rt(180)

    left_mines = all_mines
    info = "All mines: {}. Left mines: {}.".format(all_mines, all_mines)
    draw_game_info(board_width*field_width, board_height*field_height, 12, info)
    
    for h in range(board_height):
        for w in range(board_width):
            draw_field("chartreuse", field_height, field_width)
            # next column
            hop(field_width, 0)
        # next row
        hop(-field_width*board_width, field_height)
    # align to start position
    hop(0, -(board_height)*field_height)
    fillcolor('black')
    update()


def set_mines(fields):
    random.seed()
    nrows = len(fields)
    ncols = len(fields[0])
    fields_number = nrows*ncols
    mines_number = random.randint(fields_number//10, fields_number//7)
    set_mines_number = 0

    while set_mines_number < mines_number:
        idx = random.randint(0, fields_number-1)
        field = fields[idx//ncols-1][idx%ncols-1]
        if not field.mine():
            field.set_mine()
            set_mines_number = set_mines_number + 1

    return mines_number


def set_numbers(fields):
    nrows = len(fields)
    ncols = len(fields[0])

    for row in range(nrows):
        for col in range(ncols):
            field = fields[row][col]
            if not field.mine():
                neighbours = field.neighbours()
                number = 0
                for n in neighbours:
                    if n.mine():
                        number = number + 1
                fields[row][col].set_number(number)


def set_neighbours(fields):
    nrows = len(fields)
    ncols = len(fields[0])

    for row in range(nrows):
        for col in range(ncols):
            neighbours = [(x,y) for x in range(-1,2) for y in range(-1,2)]
            neighbours.remove((0,0))

            if row == 0:
                neighbours = [(x,y) for (x,y) in neighbours if x != -1]
            if row == nrows-1:
                neighbours = [(x,y) for (x,y) in neighbours if x != 1]
            if col == 0:
                neighbours = [(x,y) for (x,y) in neighbours if y != -1]
            if col == ncols-1:
                neighbours = [(x,y) for (x,y) in neighbours if y != 1]
            
            neighbour_list = []
            for (r,c) in neighbours:
                    neighbour_list.append(fields[row+r][col+c])
            fields[row][col].set_neighbours(neighbour_list)


def coordinates_to_field(x, y, field_height, field_width, rows, cols):
    x = x + field_width*cols//2
    y = y + field_height*rows//2
    row = int(y//field_height)
    col = int(x//field_width)
    if row < 0 or row > rows-1 or col < 0 or col > cols-1:
        return (-1,-1)
    return (row,col)


def field_to_left_down_coordinates(row, col, field_height, field_width):
    x = col*field_width
    y = row*field_height
    return(x,y)


def the_game(field_height, field_width, rows, cols, font_size):
    fields = [[Field(pos = (r,c)) for c in range(cols)] for r in range(rows)]
    set_neighbours(fields)
    all_mines_number = set_mines(fields)
    left_mines_number = all_mines_number
    set_numbers(fields)
    draw_board(field_height, field_width, rows, cols, all_mines_number)

    game_over = False
    while not game_over:
        event, x, y = give_event()
        (row,col) = coordinates_to_field(x, y, field_height, field_width, rows, cols)
        (dx,dy) = field_to_left_down_coordinates(row,col, field_height, field_width)

        if row > -1:
            if event == "l_klik":
                field = fields[row][col]
                if field.marked():
                    field.mark()
                uncover_field(field_height, field_width, field)
                if field.mine():
                    game_over = True
                
                update()

            elif event == "r_klik":
                hop(dx,dy)
                left_mines_number = mark_field(field_height, field_width, fields[row][col], left_mines_number)
                hop(-dx, -dy)
                info = "All mines: {}. Left mines: {}.".format(all_mines_number, left_mines_number)
                draw_game_info(cols*field_width, rows*field_height, font_size, info)
                if left_mines_number == 0:
                    game_over = True

                update()

            else:
                print("Nieobsługiwane event: " + event)

    # handle game over
    uncover_all_fields(fields, field_height, field_width)
    update()


def main():
    
    field_height = 51
    field_width = 60
    rows = 11
    columns = 12
    font = 12

    ini_graphics(field_height*rows + 12*font, field_width*columns + 12*font)
    ini_myszki()
    the_game(field_height, field_width, rows, columns, font)
    done()


main()
    
