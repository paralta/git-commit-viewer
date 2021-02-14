import logging
from user_input import UserInput
from retriever import CommitRetriever

if __name__ == '__main__':
    logging.info('Start Commit Viewer')

    # Request and validate user input
    logging.info('Start User Input Request')
    uinput = UserInput()
    url, branch = uinput.get()

    # Retrieve list of commits
    logging.info('Start Commit Retriever')
    retriever = CommitRetriever(url, branch)
    print(retriever.get_commits())
