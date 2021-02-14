import logging
import unittest


class UserInput:
    '''
    Request and validate user input
    '''

    def validate_url(self, url):
        if url and 'https://github.com/' in url and '.git' in url:
            return True
        else:
            return False

    def get(self):
        # Request GitHub url
        while True:
            url = str(input('Please enter GitHub url: '))
            if self.validate_url(url):
                break
            else:
                logging.error('Invalid url!')

        # Request branch name
        branch = str(
            input('Please enter branch name [press enter for master]: '))
        if not branch:
            branch = 'master'

        return url, branch


class TestUrlValidation(unittest.TestCase):
    def test_empty(self):
        ui = UserInput()
        self.assertFalse(ui.validate_url(''))

    def test_not_valid_url(self):
        ui = UserInput()
        self.assertFalse(ui.validate_url('freeCodeCamp/freeCodeCamp'))

    def test_not_valid_url_start(self):
        ui = UserInput()
        self.assertFalse(ui.validate_url('freeCodeCamp/freeCodeCamp.git'))

    def test_not_valid_url_end(self):
        ui = UserInput()
        self.assertFalse(ui.validate_url(
            'https://github.com/freeCodeCamp/freeCodeCamp'))

    def test_valid_url(self):
        ui = UserInput()
        self.assertTrue(ui.validate_url(
            'https://github.com/freeCodeCamp/freeCodeCamp.git'))


if __name__ == '__main__':
    logging.info('Running User Input URL Validation tests')
    unittest.main()
