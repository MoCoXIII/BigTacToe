import tkinter as tk


def clicked(button):
    print("Button clicked!")


DEPTH = 0
root = tk.Tk()

pixel_virtual = tk.PhotoImage(width=1, height=1)
button = tk.Button(root,
                   text="-",
                   bg="green",
                   image=pixel_virtual,
                   height=50 if DEPTH == 0 else 10,
                   width=50 if DEPTH == 0 else 10,
                   compound="center")
button.configure(command=lambda: clicked(button))
button.pack()

root.mainloop()
