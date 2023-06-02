from github import Github
import sys
from tqdm import tqdm

class GitUser:
    def __init__(self, auth_token: str):
        """Use the auth token to log into github to grab the repository information and other useful things to help us generate graphs and profiles
        All the login code is run in this class so if stuff goes wrong we will see error messages here instead of in the git charts methods"""
        self.g = Github(auth_token)
        self.repos = list(self.g.get_user().get_repos())
        
        # Create the language information here
        self.total_languages: dict[str, int] = {}
        self.total_bytes = 0
        for repo in tqdm(self.repos, desc="Processing repos: "):
            # Skip all forked repos
            if repo.owner.name != self.g.get_user().name:
                continue
            stats = repo.get_stats_contributors()
            if stats is not None:
                first_author = stats[0].author
                if first_author.name != self.g.get_user().name:
                    continue
            for k, v in repo.get_languages().items():
                self.total_languages[k] = self.total_languages.get(k, 0) + v
                self.total_bytes += v
