import logging
from user_input import UserInput
from retriever import CommitRetriever

if __name__ == '__main__':
    logging.info('Start Commit Viewer')

    # Request and validate user input
    uinput = UserInput()
    url, branch = uinput.get()

    # Retrieve list of commits
    retriever = CommitRetriever(url, branch)
    print(retriever.get_commits())
