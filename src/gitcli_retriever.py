import multiprocessing
from retriever import CommitRetriever


class GitCLICommitRetriever:
    '''
    Retrieve commit list using git command-line interface
    '''
    url = ''
    branch = ''
    TIMEOUT_S = 5 * 60  # 5 min

    def __init__(self, url, branch):
        self.url = url
        self.branch = branch

    def process_commits(self, return_dict):
        cr = CommitRetriever(self.url, self.branch)
        c, err = cr.get_commits()
        return_dict[0] = {'commits': c, 'err': err}

    def get_commits(self):
        # Create a shared variable
        manager = multiprocessing.Manager()
        return_dict = manager.dict()

        # Start process_commits as a process
        p = multiprocessing.Process(
            target=self.process_commits, args=(return_dict,))
        p.start()

        # Wait for timeout seconds or until process finishes
        p.join(TIMEOUT_S)

        # If thread is still active when timeout finishes
        if p.is_alive():
            p.terminate()
            p.join()
            return [], 'Commit retriever timed out'

        return return_dict[0]['commits'], return_dict[0]['err']
