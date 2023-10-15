from github import Github
from github.Repository import Repository
import threading
from queue import Queue

class GitUser:
    def __init__(self, auth_token: str):
        """Use the auth token to log into github to grab the repository information and other useful things to help us generate graphs and profiles
        All the login code is run in this class so if stuff goes wrong we will see error messages here instead of in the git charts methods"""
        self.g = Github(auth_token)
        usr = self.g.get_user()
        self.repos = list(usr.get_repos())

        # Create the language information here
        result_queue = Queue()
        threads = []

        with open("diagrams/forks.txt", 'r') as f:
            forks = f.readlines()
        forks = [f.strip() for f in forks]

        def process_repo(repo: Repository):
            if repo.owner.name != usr.name:
                return
            if repo.name in forks:
                return
            print("    " + repo.name)
            # stats = repo.get_stats_contributors()
            # if stats is not None:
            #     first_author = stats[0].author
            #     if first_author.name != usr.name:
            #         return
            for k, v in repo.get_languages().items():
                result_queue.put((k, v))

        # Use multithreading because we make soooo many request calls inside process repo
        print("The following repos will be counted:")
        for repo in self.repos:
            thread = threading.Thread(target=process_repo, args=(repo,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # Process the language info to expose to other modules
        self._total_languages: dict[str, int] = {}
        self._total_bytes = 0

        while not result_queue.empty():
            k, v = result_queue.get()
            self._total_languages[k] = self._total_languages.get(k, 0) + v
            self._total_bytes += v

    @property
    def total_bytes(self):
        """Total number of bytes of code in the repo"""
        return self._total_bytes
    
    def __getitem__(self, k):
        """Total number of languages"""
        return self._total_languages.get(k, 0)
    
    def languages(self):
        return sorted(self._total_languages.items(), key=lambda x: x[1], reverse=True)
