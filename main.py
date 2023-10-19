import math
import random
import tkinter as tk
from tkinter import messagebox

EMPTY_FIELD = "white"
X_SIGN = "X"
O_SIGN = "O"
BOT_O_COLOR = "red"
BOT_X_COLOR = "violet"
STANDARD_EMPTY = "-"
PLAYABLE = "green"
SingleO = "orange"
SingleX = "blue"
BigO = "yellow"
BigX = "dark blue"
HugeO = "light green"
HugeX = "purple"
GiantO = "aqua"
GiantX = "dark purple"
BG = 'bg'
TEXT = 'text'
player = True
try:
    DEPTH = int(input("Depth: "))
except ValueError:
    DEPTH = "User has disappointed us all"
while not (isinstance(DEPTH, int) and 0 <= DEPTH <= 2):
    DEPTH = input("Depth (should be an integer between 0 and 2): ")
    try:
        DEPTH = int(DEPTH)
    except ValueError:
        continue
objects = []
search = []
bots_move = -1
green = -1


# giant 87 line brute force win check for small tiles
def check_won(move):
    relative_move = move % 9
    if search[move][TEXT] != STANDARD_EMPTY:  # NOQA
        # Check horizontal win for left placed last
        # (X) X  X
        # (O) O  O
        # (X) X  X
        if relative_move % 3 == 0:
            if search[move][TEXT] == search[move + 1][TEXT] == search[move + 2][TEXT]:  # NOQA
                return True
        # Check horizontal win for center placed last
        #  X (X) X
        #  O (O) O
        #  X (X) X
        if relative_move % 3 == 1:
            if search[move - 1][TEXT] == search[move][TEXT] == search[move + 1][TEXT]:  # NOQA
                return True
        # Check horizontal win for right placed last
        #  X  X (X)
        #  O  O (O)
        #  X  X (X)
        if relative_move % 3 == 2:
            if search[move - 2][TEXT] == search[move - 1][TEXT] == search[move][TEXT]:  # NOQA
                return True
        # Check vertical win for top placed last
        # (X)(O)(X)
        #  X  O  X
        #  X  O  X
        if relative_move < 3:
            if search[move][TEXT] == search[move + 3][TEXT] == search[move + 6][TEXT]:  # NOQA
                return True
        # Check vertical win for center placed last
        #  X  O  X
        # (X)(O)(X)
        #  X  O  X
        if 6 > relative_move >= 3:
            if search[move - 3][TEXT] == search[move][TEXT] == search[move + 3][TEXT]:  # NOQA
                return True
        # Check vertical win for bottom placed last
        #  X  O  X
        #  X  O  X
        # (X)(O)(X)
        if relative_move >= 6:
            if search[move - 6][TEXT] == search[move - 3][TEXT] == search[move][TEXT]:  # NOQA
                return True
        # Check backslash win for upper left placed last
        # (X) -  -
        #  -  X  -
        #  -  -  X
        if relative_move == 0:
            if search[move][TEXT] == search[move + 4][TEXT] == search[move + 8][TEXT]:  # NOQA
                return True
        # Check backslash win for center placed last
        #  X  -  -
        #  - (X) -
        #  -  -  X
        if relative_move == 4:
            if search[move - 4][TEXT] == search[move][TEXT] == search[move + 4][TEXT]:  # NOQA
                return True
        # Check backslash win for bottom right placed last
        #  X  -  -
        #  -  X  -
        #  -  - (X)
        if relative_move == 8:
            if search[move - 8][TEXT] == search[move - 4][TEXT] == search[move][TEXT]:  # NOQA
                return True
        # Check slash win for bottom left placed last
        #  -  -  X
        #  -  X  -
        # (X) -  -
        if relative_move == 6:
            if search[move - 4][TEXT] == search[move - 2][TEXT] == search[move][TEXT]:  # NOQA
                return True
        # Check slash win for center placed last
        #  -  -  X
        #  - (X) -
        #  X  -  -
        if relative_move == 4:
            if search[move - 2][TEXT] == search[move][TEXT] == search[move + 2][TEXT]:  # NOQA
                return True
        # Check slash win for upper right placed last
        #  -  - (X)
        #  -  X  -
        #  X  -  -
        if relative_move == 2:
            if search[move][TEXT] == search[move + 2][TEXT] == search[move + 4][TEXT]:  # NOQA
                return True


# giant 87 line brute force win check for big mode
def check_big_win(move, color, multiplier):
    big_square = math.floor(move / multiplier)
    if search[move][BG] == color:  # NOQA
        # Check horizontal win for left placed last
        # (X) X  X
        # (O) O  O
        # (X) X  X
        if big_square % 3 == 0:
            if search[move][BG] == search[move + multiplier][BG] == search[move + (multiplier * 2)][BG]:  # NOQA
                return True
        # Check horizontal win for center placed last
        #  X (X) X
        #  O (O) O
        #  X (X) X
        if big_square % 3 == 1:
            if search[move - multiplier][BG] == search[move][BG] == search[move + multiplier][BG]:  # NOQA
                return True
        # Check horizontal win for right placed last
        #  X  X (X)
        #  O  O (O)
        #  X  X (X)
        if big_square % 3 == 2:
            if search[move - (multiplier * 2)][BG] == search[move - multiplier][BG] == search[move][BG]:  # NOQA
                return True
        # Check vertical win for top placed last
        # (X)(O)(X)
        #  X  O  X
        #  X  O  X
        if big_square < 3:
            if search[move][BG] == search[move + (multiplier * 3)][BG] == search[move + (multiplier * 6)][BG]:  # NOQA
                return True
        # Check vertical win for center placed last
        #  X  O  X
        # (X)(O)(X)
        #  X  O  X
        if 6 > big_square >= 3:
            if search[move - (multiplier * 3)][BG] == search[move][BG] == search[move + (multiplier * 3)][BG]:  # NOQA
                return True
        # Check vertical win for bottom placed last
        #  X  O  X
        #  X  O  X
        # (X)(O)(X)
        if big_square >= 6:
            if search[move - (multiplier * 6)][BG] == search[move - (multiplier * 3)][BG] == search[move][BG]:  # NOQA
                return True
        # Check backslash win for upper left placed last
        # (X) -  -
        #  -  X  -
        #  -  -  X
        if big_square == 0:
            if search[move][BG] == search[move + (multiplier * 4)][BG] == search[move + (multiplier * 8)][BG]:  # NOQA
                return True
        # Check backslash win for center placed last
        #  X  -  -
        #  - (X) -
        #  -  -  X
        if big_square == 4:
            if search[move - (multiplier * 4)][BG] == search[move][BG] == search[move + (multiplier * 4)][BG]:  # NOQA
                return True
        # Check backslash win for bottom right placed last
        #  X  -  -
        #  -  X  -
        #  -  - (X)
        if big_square == 8:
            if search[move - (multiplier * 8)][BG] == search[move - (multiplier * 4)][BG] == search[move][BG]:  # NOQA
                return True
        # Check slash win for bottom left placed last
        #  -  -  X
        #  -  X  -
        # (X) -  -
        if big_square == 6:
            if search[move - (multiplier * 4)][BG] == search[move - (multiplier * 2)][BG] == search[move][BG]:  # NOQA
                return True
        # Check slash win for center placed last
        #  -  -  X
        #  - (X) -
        #  X  -  -
        if big_square == 4:
            if search[move - (multiplier * 2)][BG] == search[move][BG] == search[move + (multiplier * 2)][BG]:  # NOQA
                return True
        # Check slash win for upper right placed last
        #  -  - (X)
        #  -  X  -
        #  X  -  -
        if big_square == 2:
            if search[move][BG] == search[move + (multiplier * 2)][BG] == search[move + (multiplier * 4)][BG]:  # NOQA
                return True


def clicked(button):
    global search, player, bots_move, green
    print(root.winfo_geometry())
    # Check if the button is proper
    if button['text'] == STANDARD_EMPTY and button['bg'] == PLAYABLE:
        search = []
        look_for_children(root, False, 0)
        # Change the button's text to "x"
        button.config(text=X_SIGN if player else O_SIGN)
        if check_won(search.index(button)):
            idx = search.index(button)
            for i in search[(idx - (idx % 9)):(idx - (idx % 9) + 9)]:
                i.configure(bg=BigX if player else BigO)
            if DEPTH == 0:
                game_over("You won against a bot playing random moves! Wasn't that easy?")
        if check_big_win(search.index(button), BigX if player else BigO, 9):
            idx = search.index(button)
            for i in search[(idx - (idx % 81)):(idx - (idx % 81) + 81)]:
                i.configure(bg=HugeX if player else HugeO)
            if DEPTH == 1:
                game_over(f"{X_SIGN} wins!" if player else f"{O_SIGN} wins!")
        if check_big_win(search.index(button), HugeX if player else HugeO, (9 * 9)):
            idx = search.index(button)
            for i in search[(idx - (idx % (9 * 9 * 9))):(idx - (idx % (9 * 9 * 9)) + (9 * 9 * 9))]:
                i.configure(bg=GiantO if player else GiantX)
            if DEPTH == 2:
                game_over(f"{X_SIGN} wins the huge game!" if player else f"{O_SIGN} wins the huge game!")
        if check_big_win(search.index(button), GiantO if player else GiantX, (9 * 9 * 9)):
            if DEPTH == 3:
                game_over("Crazy to win this far into the game.")
        if multiplayer.get():
            bots_move = search.index(button)
            player = not player
            green = 0
            look_for_children(root, True, 0)
            if green == 0:
                look_for_children(root, True, 1)
                if green == 0:
                    game_over("It's a tie! You both played well!")
        else:
            bot_move(search.index(button))


def game_over(text):
    messagebox.showinfo("Game Over", text)
    exit(0)


def bot_move(last_move):
    global search, bots_move, green, player
    # List of all buttons

    last_move_ = get_last_move_(last_move)
    search = []
    look_for_children(root, True, 0)
    buttons = []
    if DEPTH == 0:
        buttons.extend(search)
    else:
        buttons.extend(search[last_move_:(last_move_ + 8)])

    # Choose a random button that is not clicked
    choice = get_bot_move(buttons)
    bot_button = choice
    try:
        while bot_button_unavailable(bot_button):
            buttons.remove(choice)
            choice = get_bot_move(buttons)
            bot_button = choice
    except IndexError:
        try:
            search = []
            look_for_children(root, True, 0)
            buttons = []
            buttons.extend(search)
            # Choose a random button that is not clicked
            choice = get_bot_move(buttons)
            bot_button = choice
            while bot_button_unavailable(bot_button):
                buttons.remove(choice)
                choice = get_bot_move(buttons)
                bot_button = choice
        except IndexError:
            game_over("It's a draw.")
            # exit(0)
    bots_move = search.index(bot_button)

    bot_button.configure(bg=BOT_O_COLOR if player else BOT_X_COLOR)
    # Change the bots buttons text to O
    bot_button.config(text=O_SIGN if player else X_SIGN)
    if check_won(search.index(bot_button)):
        idx = search.index(bot_button)
        for i in search[(idx - (idx % 9)):(idx - (idx % 9) + 9)]:
            i.configure(bg=BigO if player else BigX)
        if DEPTH == 0:
            game_over("The computer wins against a disappointment playing random moves! Wasn't that easy?")
    if check_big_win(search.index(bot_button), BigO if player else BigX, 9):
        idx = search.index(bot_button)
        for i in search[(idx - (idx % (9 * 9))):(idx - (idx % (9 * 9)) + (9 * 9))]:
            i.configure(bg=HugeO if player else HugeX)
        if DEPTH == 1:
            game_over("Computer wins!")
    if check_big_win(search.index(bot_button), HugeO if player else HugeX, (9 * 9)):
        idx = search.index(bot_button)
        for i in search[(idx - (idx % (9 * 9 * 9))):(idx - (idx % (9 * 9 * 9)) + (9 * 9 * 9))]:
            i.configure(bg=GiantO if player else GiantX)
        if DEPTH == 2:
            game_over("Computer wins hugely! How did you mess up that badly?!")
    if check_big_win(search.index(bot_button), GiantO if player else GiantX, (9 * 9 * 9)):
        if DEPTH == 3:
            game_over("Crazy to lose this far into the game.")
    green = 0
    look_for_children(root, True, 0)
    if green == 0:
        look_for_children(root, True, 1)
        if green == 0:
            game_over("It's a tie! You played well!")


def get_bot_move(buttons):
    return random.choice(buttons)


def bot_button_unavailable(bot_button):
    return bot_button['text'] != STANDARD_EMPTY or bot_button['bg'] in [BigX, BigO, HugeX, HugeO]


def get_last_move_(last_move):
    return ((last_move % 9) * 9) + (math.floor(last_move / 81) * 81)


def look_for_children(here, bot, green_override):
    global search, green
    if here.children:
        for child in here.children.values():
            if isinstance(child, tk.Button):
                search.append(child)
                if bot and (child['bg'] == BOT_O_COLOR or child['bg'] == BOT_X_COLOR):
                    continue
                elif child['bg'] == BigX:
                    continue
                elif child['bg'] == BigO:
                    continue
                elif child['bg'] == HugeX:
                    continue
                elif child['bg'] == HugeO:
                    continue
                elif child['text'] == X_SIGN:
                    child.configure(bg=SingleX)
                elif child['text'] == O_SIGN:
                    child.configure(bg=SingleO)
                elif green_override == 1:
                    child.configure(bg=PLAYABLE)
                    green = 1
                elif (bot and get_last_move_(bots_move) <= search.index(child) <= get_last_move_(
                        bots_move) + 8):
                    child.configure(bg=PLAYABLE)
                    green = 1
                else:
                    child.configure(bg=EMPTY_FIELD)
            else:
                if child.children:
                    look_for_children(child, bot, green_override)


class Board:
    def __init__(self, master):
        self.frame = tk.Frame(master)
        self.create_item_grid(DEPTH, root)

    def create_frame(self, depth, parent):
        global pixel_virtual
        frame = tk.Frame(parent,
                         highlightbackground="black",
                         highlightthickness=7 if DEPTH == 0 else 5 if DEPTH < 3 else 1)
        if depth > 0:
            self.create_item_grid(depth - 1, frame)
        else:
            button = tk.Button(frame,
                               text=STANDARD_EMPTY,
                               bg=PLAYABLE,
                               image=pixel_virtual,
                               height=100 if DEPTH == 0 else 50 if DEPTH == 1 else 15,
                               width=100 if DEPTH == 0 else 50 if DEPTH == 1 else 15,
                               compound="center")
            button.configure(command=lambda: clicked(button))
            button.pack()
        return frame

    def create_item_grid(self, depth, parent):
        for i in range(3):
            for j in range(3):
                item = self.create_frame(depth, parent)
                item.grid(row=i + 1, column=j)

    def iterate_nested_list(self, nested_list):
        sub_items = []
        for item in nested_list:
            if isinstance(item, list):
                self.iterate_nested_list(item)
            else:
                sub_items.append(item)
        return sub_items


def reset_geometry(me):
    root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
    me.destroy()


def are_you_sure():
    sure_thing = tk.Toplevel()
    sure_thing.title("Are you sure?")
    are_you_sure_label = tk.Label(sure_thing, text="Are you sure you want to close this window?")
    i_am_sure = tk.Button(sure_thing, text="Yes, close the game window.", command=lambda: exit(1))
    not_so_sure = tk.Button(sure_thing, text="No, just resize and reposition it.")
    not_so_sure.configure(command=lambda me=sure_thing: reset_geometry(me))
    are_you_sure_label.pack()
    i_am_sure.pack()
    not_so_sure.pack()
    sure_thing.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.attributes('-topmost', True)
    pixel_virtual = tk.PhotoImage(width=1, height=1)
    board = Board(root)
    root.configure(bg="black")
    root.title("BigTacToe by MoCoXIII")
    width = 0
    height = 0
    white_bar_thickness = 30
    if DEPTH == 0:
        width = 366
        height = 391
    if DEPTH == 1:
        width = 642
        height = 667
    if DEPTH == 2:
        width = 1011
        height = 1036
    x_pos = root.winfo_screenwidth() // 2 - width // 2 - white_bar_thickness // 2
    y_pos = root.winfo_screenheight() // 2 - height // 2 - white_bar_thickness // 2
    spacer = tk.Label(root, text="I am useless.")
    # reset_geometry(spacer)
    root.protocol("WM_DELETE_WINDOW", lambda: are_you_sure())
    multiplayer = tk.BooleanVar(root, False)
    multiplayer_checkbox = tk.Checkbutton(root, text="Multiplayer Mode", variable=multiplayer, bg="light gray",
                                          fg="black")
    multiplayer_checkbox.grid(row=0, column=0, columnspan=3)
    root.mainloop()
