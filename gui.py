"""
Title: GUI for Search Engine

Project: CSI4107 Project
Version: Vanilla System
Component: Module 1

Created: 23 Jan 2020
Last modified: 10 Feb 2020

Author: Tiffany Maynard
Status: In progress

Description: Allow a user to access search engine capabilities

"""
import tkinter
from tkinter import messagebox
import config
import corpus_access
import vsm_retrieval
import boolean_search

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
        # Create frames
        top_frame = tkinter.Frame(self.root)
        spelling_frame = tkinter.Frame(self.root)
        search_frame = tkinter.Frame(self.root)
        collection_frame = tkinter.Frame(self.root)
        button_frame = tkinter.Frame(self.root)
        bottom_frame = tkinter.Frame(self.root)
        results_frame = tkinter.Frame(bottom_frame)
        # Create labels
        prompt_label = tkinter.Label(
            top_frame,
            text='Enter search string: ')
        prompt_label.config(font=(font_to_use, 24))
        self.entry = tkinter.Entry(top_frame, textvariable="Type here",
                                   font=(font_to_use, 24))
        self.spelling_label = tkinter.Label(
            spelling_frame,
            text="Did you mean X?", font=(font_to_use, 18))
        self.spelling_label.pack(side='left')
        # Pack top frame widgets
        prompt_label.pack(side='left')
        self.entry.pack(side='left')

        # Create the button widgets
        self.search_button = tkinter.Button(
            button_frame,
            text='Search',
            command=self.run_search,
            font=(font_to_use, 18))
        # root.destroy exits/destroys the main window
        self.quit_button = tkinter.Button(
            button_frame,
            text='Quit',
            command=self.root.destroy,
            font=(font_to_use, 18))
        # Pack the buttons
        self.search_button.pack(side='left')
        self.quit_button.pack(side='left')
        self.results_label = tkinter.Label(
            bottom_frame,
            text='Search results')
        self.results_label.config(font=(font_to_use, 18))
        self.results_label.pack()
        self.search_model = tkinter.IntVar()
        # Initialize search model to 1 - Boolean
        self.search_model.set(1)
        tkinter.Label(search_frame,
                      text="Choose a search model:",
                      justify=tkinter.LEFT,
                      font=(font_to_use, 18)).pack(side='left')
        tkinter.Radiobutton(search_frame,
                            text="Boolean",
                            font=(font_to_use, 18),
                            variable=self.search_model,
                            value=1).pack(side='left')
        tkinter.Radiobutton(search_frame,
                            text="VSM",
                            font=(font_to_use, 18),
                            variable=self.search_model,
                            value=2).pack(side='left')
        # Initialize collection to 1 - uO course_html_div_element catalogue
        self.search_collection = tkinter.IntVar()
        self.search_collection.set(1)
        tkinter.Label(collection_frame,
                      text="Choose a collection:",
                      justify=tkinter.LEFT,
                      font=(font_to_use, 18)).pack(side='left')
        tkinter.Radiobutton(collection_frame,
                            text="uO Course Catalogue",
                            font=(font_to_use, 18),
                            variable=self.search_collection,
                            value=1).pack(side='left')
        tkinter.Radiobutton(collection_frame,
                            text="Reuters",
                            font=(font_to_use, 18),
                            variable=self.search_collection,
                            value=2).pack(side='left')
        self.search_results = tkinter.Text(results_frame,
                                           state="normal",
                                           font=(font_to_use, 12))
        self.search_results.pack(side='bottom')
        # Now pack the frames also
        top_frame.pack()
        spelling_frame.pack()
        search_frame.pack()
        collection_frame.pack()
        button_frame.pack()
        results_frame.pack()
        bottom_frame.pack()
        self.root.mainloop()

    def run_search(self):
        """Start search (callback function for search button)."""
        # Set corpus to be used for search
        if self.search_collection.get() == 1:
            corpus = config.UOTTAWA
        else:
            corpus = config.REUTERS
            print("Reuters not yet available")
        # Set search type
        if self.search_model.get() == 1:
            search = 'Boolean'
        else:
            search = 'VSM'

        # messagebox.showinfo(
        #     'Response',
        #     'You clicked the search button and typed '
        #     + self.entry.get() + ' ' + search + ' ' + corpus)
        if search == 'VSM':
        #do VSM search
            docs_retrieved = vsm_retrieval.retrieve(self.entry.get(), corpus)
        else:
        #do boolean search
            docs_retrieved = boolean_search.boolean_search_module(
                self.entry.get(), corpus)
        # Clear previous search results
        self.search_results.delete('1.0', "end")

        docs = corpus_access.get_documents(corpus, docs_retrieved)
        hyperlink = HyperlinkManager(self.search_results)
        if docs is None or docs == []:
            self.search_results.insert("insert", 'No documents found')
        else:
            for doc in docs:
                self.search_results.insert("insert",
                                           doc.title + '\n',
                                           hyperlink.add
                                           (self.click_link, doc.doc_id, corpus))
    def click_link(self, click_id, corpus):
        """Click link function."""
        doc = corpus_access.get_documents(corpus, [click_id])[0]
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
