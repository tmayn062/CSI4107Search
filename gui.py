"""GUI for Search Engine."""
import tkinter
from tkinter import messagebox
import corpus_access


class SearchEngineGUI:
    """Start the search engine GUI."""

    def __init__(self):
        """Initialize search GUI."""
        font_to_use = "courier 10 pitch"
        # GUI Code adapted from
        # https://codinginfinite.com/gui-application-in-python-tkinter-tutorial/
        # Create a root window
        self.root = tkinter.Tk()
        self.root.title("Jindalee")
        self.root.geometry("1000x800")
        # Create two frames
        # One frame for the top of the window
        # Another frame for bottom of the window
        self.top_frame = tkinter.Frame(self.root)
        self.spelling_frame = tkinter.Frame(self.root)
        self.search_frame = tkinter.Frame(self.root)
        self.collection_frame = tkinter.Frame(self.root)
        self.button_frame = tkinter.Frame(self.root)
        self.bottom_frame = tkinter.Frame(self.root)
        self.results_frame = tkinter.Frame(self.bottom_frame)
        # Create labels
        self.prompt_label = tkinter.Label(
            self.top_frame,
            text='Enter search string: ')
        self.prompt_label.config(font=(font_to_use, 24))
        self.entry = tkinter.Entry(self.top_frame, textvariable="Type here",
                                   font=(font_to_use, 24))
        self.spelling_label = tkinter.Label(
            self.spelling_frame,
            text="Did you mean X?", font=(font_to_use, 18))
        self.spelling_label.pack(side='left')
        # Pack top frame widgets
        self.prompt_label.pack(side='left')
        self.entry.pack(side='left')

        # Create the button widgets
        self.search_button = tkinter.Button(
            self.button_frame,
            text='Search',
            command=self.run_search,
            font=(font_to_use, 18))
        # root.destroy exits/destroys the main window
        self.quit_button = tkinter.Button(
            self.button_frame,
            text='Quit',
            command=self.root.destroy,
            font=(font_to_use, 18))
        # Pack the buttons
        self.search_button.pack(side='left')
        self.quit_button.pack(side='left')
        self.results_label = tkinter.Label(
            self.bottom_frame,
            text='Search results')
        self.results_label.config(font=(font_to_use, 18))
        self.results_label.pack()
        self.search_model = tkinter.IntVar()
        # Initialize search model to 1 - Boolean
        self.search_model.set(1)
        tkinter.Label(self.search_frame,
                      text="Choose a search model:",
                      justify=tkinter.LEFT,
                      font=(font_to_use, 18)).pack(side='left')
        tkinter.Radiobutton(self.search_frame,
                            text="Boolean",
                            font=(font_to_use, 18),
                            variable=self.search_model,
                            value=1).pack(side='left')
        tkinter.Radiobutton(self.search_frame,
                            text="VSM",
                            font=(font_to_use, 18),
                            variable=self.search_model,
                            value=2).pack(side='left')
        # Initialize collection to 1 - uO course_html_div_element catalogue
        self.search_collection = tkinter.IntVar()
        self.search_collection.set(1)
        tkinter.Label(self.collection_frame,
                      text="Choose a collection:",
                      justify=tkinter.LEFT,
                      font=(font_to_use, 18)).pack(side='left')
        tkinter.Radiobutton(self.collection_frame,
                            text="uO Course Catalogue",
                            font=(font_to_use, 18),
                            variable=self.search_collection,
                            value=1).pack(side='left')
        tkinter.Radiobutton(self.collection_frame,
                            text="Reuters",
                            font=(font_to_use, 18),
                            variable=self.search_collection,
                            value=2).pack(side='left')
        self.search_results = tkinter.Text(self.results_frame,
                                           state="normal",
                                           font=(font_to_use, 12))
        self.search_results.pack(side='bottom')
        # Now pack the frames also
        self.top_frame.pack()
        self.spelling_frame.pack()
        self.search_frame.pack()
        self.collection_frame.pack()
        self.button_frame.pack()
        self.results_frame.pack()
        self.bottom_frame.pack()
        self.root.mainloop()

    def run_search(self):
        """Start search (callback function for search button)."""
        # Set corpus to be used for search
        if self.search_collection.get() == 1:
            corpus = 'uOttawaCourseList.xml'
        else:
            corpus = 'reuters.xml'
            print("not yet available")
        # Set search type
        if self.search_model.get() == 1:
            search = 'Boolean'
        else:
            search = 'VSM'
        messagebox.showinfo(
            'Response',
            'You clicked the search button and typed '
            + self.entry.get() + ' ' + search + ' ' + corpus)
        # Clear previous search results
        self.search_results.delete('1.0', "end")

        docs = corpus_access.get_documents(corpus, [7, 9, 99])
        hyperlink = HyperlinkManager(self.search_results)
        if docs is None or docs == []:
            self.search_results.insert("insert", 'No documents found')
        else:
            for doc in docs:
                self.search_results.insert("insert",
                                           doc.title + '\n',
                                           hyperlink.add
                                           (click_link, doc.id, corpus))


def click_link(id, corpus):
    """Click link function."""
    doc = corpus_access.get_documents(corpus, [id])[0]
    messagebox.showinfo(
        doc.title,
        doc.doctext)


# Code for hyperlink manager modified from
# http://effbot.org/zone/tkinter-text-hyperlink.htm
class HyperlinkManager:
    """HyperlinkManager allows for hyperlinks in tkinter textbox."""

    def __init__(self, text):
        """Initialize HyperlinkManager."""
        self.text = text
        self.text.tag_config("hyper", foreground="blue", underline=1)
        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        """Reset HyperlinkManager links."""
        self.links = {}

    def add(self, action, doc_id, corpus):
        """Add an action to the manager."""
        # returns tags to use in associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = [action, doc_id, corpus]
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names("current"):
            if tag[:6] == "hyper-":
                self.links[tag][0](self.links[tag][1], self.links[tag][2])
                return
