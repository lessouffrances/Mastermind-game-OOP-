import os.path # to check if the leaders file exists
import random # to generate a secret code
import time 
import turtle
import sys # only make sure when quit option no error display
import tkinter # only make sure when close the window no error display

MARBLE_RADIUS = 16
PEG_RADIUS = 4
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
LEADERS_FILE = 'leaders.txt'
colors = ['red', 'blue', 'green', 'yellow', 'purple', 'black']

class Point:
   '''
   Class: Point
   Attributes: x, y
   Methods: delta_x, delta_y.
   '''
   def __init__(self, x, y):
       '''
       Constructor: Create a new instance of a point,
       Parameters:
       self -- the current object,
       x -- the coordinate x of this point,
       y -- the coordinate y of this point.
       '''
       self.x = x
       self.y = y
       
   def delta_x(self, other):
       '''
       Method: get the distance between two points on the x-axis.
       Parameters:
       self -- the current point,
       other -- another point.
       returns the distance between two points on the x-axis.
       '''
       return abs(self.x - other.x)

   def delta_y(self, other):
       '''
       Method: get the distance between two points on the y-axis. 
       Parameters:
       self -- the current point,
       other -- another point.
       returns the distance between two points on the y-axis.
       '''
       return abs(self.y - other.y)

def count_bulls_and_cows(secret_code, current_guess):
    '''
    Function that evaluates the user's score.
    Parameters: secret_code and current_guess are lists of strings of 4 colors.
    Returns integers, the counts of bulls and cows.
    '''
    bulls = 0 
    cows = 0 # initial value to track the updates
    for i in range(len(current_guess)):
        if current_guess[i] == secret_code[i]:
            bulls += 1 # the colors and positions same
        if current_guess[i] in secret_code and \
           current_guess[i] != secret_code[i]:
            cows += 1 # the colors are there but not the same index
    return bulls, cows

class Marble:
    '''
    Class: Marble
    Attributes: position, color, radius
    Methods: new_pen, set_color, get_color, draw, draw_empty, erase,
    clicked_in_region.
    '''
    def __init__(self, position, color, radius):
        '''
        Constructor: Create a new instance of a marble,
        Parameters:
        self -- the current object,
        position --  reuse the class Point, the coordinates where the turtle
                    starts to draw the marble,
        color -- string, color fill in the marble,
        radius -- integer, radius of the marble.    
        '''
        self.pen = self.new_pen()
        self.pen.speed('fastest')
        self.color = color
        self.position = position
        self.visible = False
        self.is_empty = True
        self.pen.hideturtle()
        self.radius = radius
        self.pen.speed(0)  # set to the fastest drawing

    def new_pen(self):
        '''
        Method: start a turtle pen
        Parameters: self -- the current marble to be drawn.
        '''
        return turtle.Turtle()

    def set_color(self, color):
        '''
        Method: set the color of the current marble 
        Parameters: self -- the current marble,
          color -- string, the color of marble,
        returns None. 
        '''
        self.color = color
        self.is_empty = False

    def get_color(self):
        '''
        Method: get the color of the current marble 
        Parameters: self -- the current marble,
          color -- string, the color of marble,
        returns string, the color.
        '''
        return self.color

    def draw(self):
        '''
        Method: draw a color-filled marble at a specified position,
          with a specified color and radius.
        Parameters: self -- the current marble,
        returns None.
        '''
        # if self.visible and not self.is_empty:
        # return
        self.pen.up()
        self.pen.goto(self.position.x, self.position.y)
        self.visible = True
        self.is_empty = False
        self.pen.down()
        self.pen.fillcolor(self.color)
        self.pen.begin_fill()
        self.pen.circle(self.radius)
        self.pen.end_fill()

    def draw_empty(self):
        '''
        Method: draw an empty marble at a specified position and with
           a specified radius
        Parameters: self -- the current marble,
        returns None.
        '''
        self.erase()
        self.pen.up()
        self.pen.goto(self.position.x, self.position.y)
        self.visible = True
        self.is_empty = True
        self.pen.down()
        self.pen.circle(self.radius)

    def erase(self):
        '''
        Method: erase the current marble
        Parameters: self -- the current marble,
        returns None.
        '''
        self.visible = False
        self.pen.clear()

    def clicked_in_region(self, x, y):
        '''
        Method: check if the marble area is clicked
        Parameters:
        self -- the current marble,
        x -- the x coordinate of point clicked,
        y -- the y coordinate of point clicked
        returns Boolean, True if the marble area is clicked, otherwise False.
        '''
        if abs(x - self.position.x) <= self.radius * 2 and \
                abs(y - self.position.y) <= self.radius * 2:
            return True
        return False

class MyShape:
    '''
    Class: Myshape
    Attributes: screen, position, gif_image, width, height
    Methods: clicked_in_region.
    '''
    def __init__(self, screen, position, gif_image, width, height):
        '''
        Constructor: Create a new instance of a shape,
        Parameters:
        self -- the current object,
        position -- reuse class Point, position of the shape,
        gif_name -- string, name of the shape,
        width -- integer, width of the shape,
        height -- integer, height of the shape.
        '''
        screen.register_shape(gif_image)            
        self.turtle = turtle.Turtle(shape=gif_image)
        self.turtle.penup()
        self.position = position
        self.turtle.goto(position.x, position.y)
        self.turtle.stamp() # stamp the gif on canvas
        self.turtle.hideturtle()
        self.width = width
        self.height = height

    def clicked_in_region(self, x, y):
        '''
        Method: check if the shape area is clicked
        Parameters: 
        self -- the current shape,
        x -- the x coordinate of point clicked,
        y -- the y coordinate of point clicked
        returns Boolean, True if the shape area is clicked, otherwise False.
        '''
        if self.position.x - self.width // 2 <= x <= self.position.x + self.width // 2 \
           and self.position.y - self.height // 2 <= y <= self.position.y + self.height // 2:
            return True
        else:
            return False

def read_leaders():
    '''
    Function that reads the leaders file,
    Parameters: None,
    Returns a list of leaders and scores.
    '''
    if not os.path.exists(LEADERS_FILE):
        return [] # if file does not exists
    with open(LEADERS_FILE, 'r') as f:
        leaders = eval(f.read()) # leaders being read as a list
    return leaders

def write_leaders(leaders):
    '''
    Function that writes to the leaders file,
    Parameters: a list of tuples,
    Returns None.
    '''
    with open(LEADERS_FILE, 'w') as f:
        f.write(str(leaders))

class MasterMind:
    '''
    Class: MasterMind
    Attributes: None
    Methods: move_pointer, draw_rectangles, draw_rectangle,
    check_color_button_clicked, check_color_buttons_clicked,
    check_option_buttons_clicked,on_mouse_clicked,
    update_leaders,process_submit, process_reset, process_quit.
    '''
    def __init__(self):
        '''
        Constructor: Create a new instance of a MasterMind Game,
        Parameters:
        self -- the current object.   
        '''
        self.screen = turtle.Screen()
        self.screen.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen.title('CS5001 MasterMind Code Game')
        self.pointer = turtle.Turtle()
        self.pointer.speed('fastest')
        self.pointer.hideturtle()

        self.draw_rectangles() # draw three boards
        self.color_marbles: list[list[None | Marble]] = [[None for _ in range(4)] for _ in range(10)]
        self.peg_marbles: list[list[Marble | None]] = [[None for _ in range(4)] for _ in range(10)]
        self.init_color_marbles() # color marbles set up
        self.init_peg_marbles() # peg marbles set up 
        self.color_buttons: list[None | Marble] = [None for _ in range(len(colors))]
        self.init_button_marbles() # button marbles setup
        self.option_buttons: dict[str, MyShape] = {}
        self.init_option_buttons() # option buttons set up

        self.screen.onclick(self.on_mouse_clicked)# register clicks on canvas
        self.leaders = read_leaders() # read the leaders board when the game starts
        self.init_leader_board()# leader board set up
        self.username = self.screen.textinput('CS5001 MasterMind Code Game', 'Your username:')
        self.secret_code = random.sample(colors, 4) # generate random secret code
        print(self.secret_code) # just for human eyes to compare
        self.button_clicked: list[bool] = [False for _ in range(len(colors))]
        self.color_button_enabled: list[bool] = [True for _ in range(len(colors))]
        self.option_button_enabled: dict[str, bool] = {'submit': False, 'reset': True}
        self.current_guess = [] # an empty list to keep track of guesses
        self.current_round = 0 # update the number of rounds
        self.pointer.color('red') 
        self.move_pointer() # turtle pointer moves along the guesses
        self.screen.mainloop() 

    def move_pointer(self):
        '''
        Method: indicate and move along the row of current guess,
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        x = -310
        y = 290 - self.current_round * 50 
        self.pointer.up()
        self.pointer.setpos(x, y) # go to the starting position that fits the board
        self.pointer.down()
        self.pointer.showturtle()

    def init_option_buttons(self):
        '''
        Method: set up the option buttons
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        self.option_buttons['submit'] = MyShape(self.screen, Point(10, -290), 'checkbutton.gif', 60, 60)
        self.option_buttons['reset'] = MyShape(self.screen, Point(70, -290), 'xbutton.gif', 60, 60)
        self.option_buttons['quit'] = MyShape(self.screen, Point(240, -290), 'quit.gif', 200, 100) # reuse class

    def init_button_marbles(self):
        '''
        Method: set up the marble buttons
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        start_x = -280
        start_y = -290
        for i, color in enumerate(colors):
            x = start_x + i * 40
            y = start_y
            self.color_buttons[i] = Marble(Point(x, y), color, MARBLE_RADIUS) # reuse class Marble
            self.color_buttons[i].draw()

    def init_color_marbles(self):
        '''
        Method: set up the color marbles
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        start_x = -280
        start_y = 275
        for row in range(10):
            for col in range(4):
                x = col * 50 + start_x
                y = start_y - row * 50
                self.color_marbles[row][col] = Marble(Point(x, y), 'white', MARBLE_RADIUS) # reuse class Marble
                self.color_marbles[row][col].draw()

    def init_peg_marbles(self):
        '''
        Method: set up the peg marbles
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        start_x = -50
        start_y = 300
        for row in range(10):
            y = start_y - row * 50
            for i in range(4):
                xi = start_x + i % 2 * 32
                yi = y - i // 2 * 20
                self.peg_marbles[row][i] = Marble(Point(xi, yi), 'white', PEG_RADIUS) # reuse class Marble
                self.peg_marbles[row][i].draw()

    def draw_rectangles(self):
        '''
        Method: draw three boards of marbles, buttons and leaders
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        self.draw_rectangle(turtle.Turtle(), 5, 'black', -340, 340, 400, 570) # reuse Method 
        self.draw_rectangle(turtle.Turtle(), 5, 'blue', 100, 340, 220, 570)
        self.draw_rectangle(turtle.Turtle(), 5, 'black', -340, -240, 670, 100)

    def draw_rectangle(self, pen: turtle.Turtle, pensize, color, x, y, width, height):
        '''
        Method: draw a single board
        Parameters: 
        self -- the current game object,
        pen -- turtle.Turtle,
        pensize -- the size of the pen,
        color -- the color of the pen,
        x -- the coordinate of x where the pen starts to draw,
        y -- the coordinate of y where the pen starts to draw,
        width -- width of the board,
        height -- height of the board,
        returns None.
        '''
        pen.pensize(pensize)
        pen.speed('fastest')
        pen.color(color)
        pen.up()
        pen.goto(x, y)
        pen.down()
        pen.forward(width)
        pen.right(90)
        pen.forward(height)
        pen.right(90)
        pen.forward(width)
        pen.right(90)
        pen.forward(height)
        pen.hideturtle()

    def check_color_button_clicked(self, i, button, x, y):
        '''
        Method: check if a color button is clicked
        Parameters: 
        self -- the current game object,
        i -- the index of the color button, 
        button -- the marble of the button, 
        x -- the coordinate of x where the user clicks,
        y -- the coordinate of y where the user clicks,
        returns Boolean, True if clicked.
        '''
        if not button.clicked_in_region(x, y) or not self.color_button_enabled[i]:
            return False # the color button is neither clicked nor functioning
        button.draw_empty() # the color is gone
        self.color_button_enabled[i] = False # turn off the button 
        self.current_guess.append(button.color) # get the color to make the guess list
        self.color_marbles[self.current_round][len(self.current_guess) - 1].color = button.color
        self.color_marbles[self.current_round][len(self.current_guess) - 1].draw()# color fills 
        if len(self.current_guess) == 4: # if guess counts to 4
            for j in range(len(colors)):
                self.color_button_enabled[j] = False # turn off all color buttons
            self.option_button_enabled['submit'] = True # turn on submit button
        return True

    def check_color_buttons_clicked(self, x, y):
        '''
        Method: check if color buttons are clicked
        Parameters: 
        self -- the current game object,
        x -- the coordinate of x where the user clicks,
        y -- the coordinate of y where the user clicks,
        returns Boolean, True if clicked.
        '''
        for i, button in enumerate(self.color_buttons): # iterate all the color buttons
            if self.check_color_button_clicked(i, button, x, y): # the method above reused
                return True
        return False

    def process_submit(self):
        '''
        Method: process the submission of each round
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        self.option_button_enabled['submit'] = False # not functioning
        bulls, cows = count_bulls_and_cows(self.secret_code, self.current_guess) # function reused
        for i in range(bulls):
            self.peg_marbles[self.current_round][i].color = 'black'
            self.peg_marbles[self.current_round][i].draw() # draw black pegs for bulls
        for i in range(bulls, bulls + cows):
            self.peg_marbles[self.current_round][i].color = 'red'
            self.peg_marbles[self.current_round][i].draw() # draw red pegs for cows
        if bulls == 4: # the user wins
            for i in range(len(colors)):
                self.color_button_enabled[i] = False # turn off color buttons
            self.option_button_enabled['submit'] = False # turn off
            self.option_button_enabled['reset'] = False # turn off
            MyShape(self.screen, Point(0, 0), 'winner.gif', 183, 84) # gif displays
            self.update_leaders() # update username and score
            return
        self.current_round += 1 # otherwise round plus 1
        if self.current_round == 10:
            self.option_button_enabled['reset'] = False # turn off 
            MyShape(self.screen, Point(0, 0), 'Lose.gif', 183, 84) # the user loses
            return
        self.move_pointer() # move pointer set up
        self.current_guess.clear() # renew the tracker for the next round
        for i in range(len(colors)):
            self.color_button_enabled[i] = True # turn on color buttons
            self.color_buttons[i].draw() # colors go back
 
    def process_reset(self):
        '''
        Method: process the reset of each round
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        self.option_button_enabled['submit'] = False # turn off submit button
        self.current_guess.clear() # renew the tracker 
        for marble in self.color_marbles[self.current_round]:
            marble.draw_empty() # clear the chosen marbles
        for i in range(len(colors)):
            self.color_button_enabled[i] = True # turn on color buttons
            self.color_buttons[i].draw() # colors go back

    def process_quit(self):
        '''
        Method: process quit
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        MyShape(self.screen, Point(0, 0), 'quitmsg.gif', 184, 84) # gif displays
        for i in range(len(colors)):
            self.color_button_enabled[i] = False # turn off color buttons
        self.option_button_enabled['submit'] = False 
        self.option_button_enabled['reset'] = False # turn off option buttons
        time.sleep(1)
        sys.exit(0) # see bottom Note in design.txt 

    def check_option_buttons_clicked(self, x, y):
        '''
        Method: check if option buttons are clicked
        Parameters: 
        self -- the current game object,
        x -- the coordinate of x where the user clicks,
        y -- the coordinate of y where the user clicks,
        returns None.
        '''
        for name, button in self.option_buttons.items():
            if not button.clicked_in_region(x, y):
                continue # there is no click
            if name == 'submit' and self.option_button_enabled['submit']:
                self.process_submit() # if submit is functioning and clicked
                return
            elif name == 'reset' and self.option_button_enabled['reset']:
                self.process_reset() # if reset is functioning and clicked
                return
            elif name == 'quit':
                self.process_quit() # if quit is functioning and clicked
                return

    def on_mouse_clicked(self, x, y):
        '''
        Method: Put two sets of buttons into use by clicking
        Parameters: 
        self -- the current game object,
        x -- the coordinate of x where the user clicks,
        y -- the coordinate of y where the user clicks,
        returns None.
        '''
        if self.check_color_buttons_clicked(x, y):
            return
        self.check_option_buttons_clicked(x, y) # combine two types of clicks

    def init_leader_board(self):
        '''
        Method: draw leader board and display leaders file
        Parameters: 
        self -- the current game object,
        x -- the coordinate of x where the user clicks,
        y -- the coordinate of y where the user clicks,
        returns None.
        '''
        pen = turtle.Turtle() 
        pen.up()
        pen.setpos(120, 290)
        pen.down()
        pen.write('Leaders:', font=("Courier", 24, "bold"))
        for i, leader in enumerate(self.leaders): # enumerate the sorted list
            pen.up()
            pen.setpos(120, 260 - 30 * i)
            pen.down()
            pen.write(f'{leader[0]} {leader[1]}', font=("Courier", 24, "bold"))
        pen.hideturtle()

    def update_leaders(self):
        '''
        Method: append the new leader information, sort the list, and write to the leaders file
        Parameters: 
        self -- the current game object,
        returns None.
        '''
        leader = (self.current_round + 1, self.username) # score and username
        self.leaders.append(leader) # append a new leader
        self.leaders = sorted(self.leaders, key=lambda x: x[0])[:5] # sorting based on the score , take top 5
        write_leaders(self.leaders) # write to the leaders file

def main():
   try:
      MasterMind()
   except tkinter.TclError:
      sys.exit()
   except turtle.Terminator:
      sys.exit() # only aim to make sure there is no error when close the window before input a username
if __name__ == "__main__":
    main()
