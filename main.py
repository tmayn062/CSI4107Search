"""Search Engine Project for CSI4107."""
import gui
import corpusPreProcessing


def main():
    """Run search engine and related functions."""
    corpusPreProcessing.parse()
    gui.SearchEngine()


main()
