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
        self.root.title("Jindalee")
        self.root.geometry("800x600")
        # Create two frames
        # One frame for the top of the window
        # Another frame for bottom of the window
        self.top_frame = tkinter.Frame(self.root)
        self.middle_frame = tkinter.Frame(self.root)
        self.bottom_frame = tkinter.Frame(self.root)
        # Create labels
        self.prompt_label = tkinter.Label(
            self.top_frame,
            text='Enter search string: ')
        self.prompt_label.config(font=("Helvetica", 24))
        self.entry = tkinter.Entry(self.top_frame, textvariable="Type here",
                                   font=("Helvetica", 24))
        # Pack top frame widgets
        self.prompt_label.pack(side='left')
        self.entry.pack(side='left')
        # Create the button widgets
        self.search_button = tkinter.Button(
            self.middle_frame,
            text='Search',
            command=self.run_search,
            font=("Helvetica", 18))
        # root.destroy exits/destroys the main window
        self.quit_button = tkinter.Button(
            self.middle_frame,
            text='Quit',
            command=self.root.destroy,
            font=("Helvetica", 18))
        # Pack the buttons
        self.search_button.pack(side='left')
        self.quit_button.pack(side='left')
        self.results_label = tkinter.Label(
                                self.bottom_frame,
                                text='Search results')
        self.results_label.config(font=("Helvetica", 18))
        self.results_label.pack(side='left')
        # Now pack the frames also
        self.top_frame.pack()
        self.middle_frame.pack()
        self.bottom_frame.pack()
        self.root.mainloop()

    def run_search(self):
        """Start search (callback function for search button)."""
        messagebox.showinfo(
            'Response',
            'You clicked the search button and typed ' + self.entry.get())
