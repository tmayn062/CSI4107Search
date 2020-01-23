"""GUI for Search Engine."""
import tkinter
from tkinter import messagebox


class SearchEngine:
    """Start the search engine GUI."""

    def __init__(self):
        """Initialize search GUI."""
        # GUI Code adapted from
        # https://codinginfinite.com/gui-application-in-python-tkinter-tutorial/
        # Create a root window
        self.root = tkinter.Tk()
        self.root.title("CSI4107 Search")
        self.root.geometry("300x200")
        # Create two frames
        # One frame for the top of the window
        # Another frame for bottom of the window
        self.top_frame = tkinter.Frame(self.root)
        self.middle_frame = tkinter.Frame(self.root)
        self.bottom_frame = tkinter.Frame(self.root)
        # Create labels
        self.prompt_label = tkinter.Label(
            self.middle_frame,
            text='Enter search string: ')
        self.entry = tkinter.Entry(self.middle_frame)
        # Pack top frame widgets
        self.prompt_label.pack(side='left')
        self.entry.pack(side='left')
        # Create the button widgets
        self.search_button = tkinter.Button(
            self.bottom_frame,
            text='Search',
            command=self.run_search)
        # root.destroy exits/destroys the main window
        self.quit_button = tkinter.Button(
            self.bottom_frame,
            text='Quit',
            command=self.root.destroy)
        # Pack the buttons
        self.search_button.pack(side='left')
        self.quit_button.pack(side='left')

        # Now pack the frames also
        self.top_frame.pack()
        self.middle_frame.pack()
        self.bottom_frame.pack()
        tkinter.mainloop()

    def run_search(self):
        """Start search (callback function for search button)."""
        messagebox.showinfo(
            'Response',
            'You clicked the search button and typed ' + self.entry.get())
