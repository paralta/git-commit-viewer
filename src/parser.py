import re
import logging
import unittest


class CommitParser:
    '''
    Build a commit dictionary with SHA, message, author and date for each entry
    '''
    raw_input = ''
    commits = []

    def __init__(self, raw):
        self.raw_input = raw

    def parse_commit(self, raw_commit_info):
        # Split each commit line
        raw_commit_info = raw_commit_info.split('\n')
        if len(raw_commit_info) < 5:
            logging.error('Incomplete commit information')
            return False

        # Init index to iterate over commit information lines
        indx = 0

        # Parse SHA info
        sha = raw_commit_info[indx].replace('commit', '').replace(' ', '')

        # Parse author info (remove email info)
        while raw_commit_info[indx].find('Author:') == -1:
            indx = indx + 1
            if indx == len(raw_commit_info):
                logging.error(
                    'Author information not found for at least one commit')
                return False
        author = raw_commit_info[indx].replace('Author:', '').lstrip()
        author = re.sub("[\<].*?[\>]", "", author)

        # Parse data info
        while raw_commit_info[indx].find('Date:') == -1:
            indx = indx + 1
            if indx == len(raw_commit_info):
                logging.error(
                    'Date information not found for at least one commit')
                return False
        date = raw_commit_info[indx].replace('Date:', '').lstrip()

        # Parse multiple message info
        indx = indx + 1
        if indx == len(raw_commit_info):
            logging.error(
                'Message information not found for at least one commit')
            return False
        message = []
        for i in raw_commit_info[indx:]:
            j = i.lstrip().rstrip()
            if j:
                message.append(j)

        # Add commit info to dict
        self.commits.append({'sha': sha, 'author': author,
                             'date': date, 'message': message})
        return True

    def parse(self):
        # Split commits
        raw_input_list = self.raw_input.split('\n\ncommit ')

        # Parse information for each commit
        for i in raw_input_list:
            if not self.parse_commit(i):
                return False
        return True

    def get_commits(self):
        if self.parse():
            return self.commits
        else:
            return []


class TestCommitInformationParser(unittest.TestCase):
    def test_commit(self):
        cp = CommitParser(
            'commit abcd\nAuthor: someone\nDate:   someday\n\n    some message')
        self.assertEqual(cp.get_commits(), [
                         {'sha': 'abcd', 'author': 'someone', 'date': 'someday', 'message': ['some message']}])

    def test_invalid_commit(self):
        cp = CommitParser('')
        self.assertEqual(cp.get_commits(), [])


if __name__ == '__main__':
    logging.info('Running User Input URL Validation tests')
    unittest.main()
