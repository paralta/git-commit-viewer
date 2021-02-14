import logging
import unittest
import subprocess
from parser import CommitParser


class CommitRetriever:
    '''
    Clone git repository using url, checkout to branch and 
    '''
    url = ''
    branch = ''
    repository_dir = ''
    commits = []

    def __init__(self, url, branch):
        self.url = url
        self.branch = branch
        self.repository_dir = 'repositories/' + \
            url.split('/')[-1].replace('.git', '')

    def clone_repository(self):
        # Clone repository from url specified by user
        result = subprocess.run(
            'git clone ' + self.url, capture_output=True, cwd='repositories', shell=True)

        # Handle errors
        if result.stderr:
            err = result.stderr.decode("utf-8")
            if 'already exists and is not an empty directory' in err:
                logging.warning(err)
                return True
            elif 'Cloning into' in err and not 'not found' in err:
                return True
            else:  # e.g. repository not found
                logging.error(err)
                return False
        return True

    def checkout(self):
        # Checkout to branch specified by user
        result = subprocess.run(
            'git checkout ' + self.branch, capture_output=True, cwd=self.repository_dir, shell=True)

        # Handle errors
        if result.stderr:
            err = result.stderr.decode("utf-8")
            if 'Already on' in err:
                logging.warning(err)
                return True
            else:  # e.g. branch not found
                logging.error(err)
                return False
        return True

    def log(self):
        # Retrieve commit data
        result = subprocess.run(
            'git log', capture_output=True, cwd=self.repository_dir, shell=True)

        # Handle errors
        if result.stderr:
            return False

        # Parse raw commit data
        parser = CommitParser(result.stdout.decode("utf-8"))
        self.commits = parser.get_commits()
        return True

    def process_commits(self):
        if not self.clone_repository():
            return
        if not self.checkout():
            return
        if not self.log():
            return

    def get_commits(self):
        self.process_commits()
        return self.commits


class Test1CloneRepository(unittest.TestCase):
    def test_clone_repository(self):
        cr = CommitRetriever(
            'https://github.com/floodsung/Deep-Learning-Papers-Reading-Roadmap.git', '')
        self.assertTrue(cr.clone_repository())

    def test_clone_repository_again(self):
        cr = CommitRetriever(
            'https://github.com/floodsung/Deep-Learning-Papers-Reading-Roadmap.git', '')
        self.assertTrue(cr.clone_repository())

    def test_invalid_clone_repository(self):
        cr = CommitRetriever(
            'https://github.com/floodsung/Deep-Learning-Papers-Reading-Roadmap-invalid.git', '')
        self.assertFalse(cr.clone_repository())


class Test2CheckoutRepository(unittest.TestCase):
    def test_checkout_master(self):
        cr = CommitRetriever(
            'https://github.com/floodsung/Deep-Learning-Papers-Reading-Roadmap.git', 'master')
        self.assertTrue(cr.checkout())

    def test_checkout_invalid_branch(self):
        cr = CommitRetriever(
            'https://github.com/floodsung/Deep-Learning-Papers-Reading-Roadmap.git', 'not_a_branch')
        self.assertFalse(cr.checkout())


class Test3LogRepository(unittest.TestCase):
    def test_checkout_master(self):
        cr = CommitRetriever(
            'https://github.com/floodsung/Deep-Learning-Papers-Reading-Roadmap.git', 'master')
        self.assertTrue(cr.log())


if __name__ == '__main__':
    logging.info('Running User Input URL Validation tests')
    unittest.main()
