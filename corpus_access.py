"""Access corpus of documents."""
import xml.etree.ElementTree as xml


class Document:
    """Document holds all the document info from a corpus."""

    def __init__(self, id, title, doctext):
        """Document init."""
        self.id = id
        self.title = title
        self.doctext = doctext

    def __str__(self):
        """Print document."""
        return self.title


def get_documents(corpus_filename, list_doc_ids):
    """Return a list of documents using a given list of doc ids."""
    """order of doc ids is preserved"""
    # XML parse code adapted from
    # https://stackabuse.com/reading-and-writing-xml-files-in-python/
    tree = xml.parse(corpus_filename)
    root = tree.getroot()
    doc_list = []
    for i in list_doc_ids:
        doc_to_add = Document(i,
                              root[i][0].text+' '+root[i][1].text,
                              root[i][2].text)
        doc_list.append(doc_to_add)
    return doc_list
