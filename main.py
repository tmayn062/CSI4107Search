"""Search Engine Project for CSI4107."""
import gui
import corpus_preprocessing


def main():
    """Run search engine and related functions."""
    corpus_preprocessing.parse()
    gui.SearchEngineGUI()


main()
