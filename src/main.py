import logging
from user_input import UserInput

if __name__ == '__main__':
    logging.info('Start Commit Viewer')

    # Request and validate user input
    uinput = UserInput()
    url, branch = uinput.get()
