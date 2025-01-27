import os
from pprint import pprint

from dotenv import load_dotenv
from github import Github
from github import Auth
from github import Repository
from dataclasses import dataclass, field

@dataclass
class GitHubManager:

    github_auth: Auth.Token = field(init=False)
    g: Github = field(init=False)
    github_repo: Repository.Repository = field(init=False)


    def __post_init__(self):
        # Load environment variables from .env file
        load_dotenv()
        # print(os.getenv("GITHUB_API_KEY"))
        self.github_auth = Auth.Token(os.getenv("GITHUB_API_KEY", ""))
        self.g = Github(auth=self.github_auth)
        self.github_username = self.g.get_user().login
        # self.github_username = os.getenv("GITHUB_USERNAME", "")
        print(self.github_username)

        self.github_repo = self.g.get_repo(f"{self.github_username}/{os.getenv('GITHUB_REPO', '')}")
        print(self.github_repo)
        # self.repo = self.g.get_repo(f"{self.github_username}/{self.github_repo}")


    def get_file(self, file_path):
        """Retrieve the content of a file."""
        file_content = self.github_repo.get_contents(file_path)
        return file_content

    # def checkout_file(self, file_path):
    #     """Retrieve the content of a file."""
    #     file_content = self.github_repo.get_contents(file_path)
    #     return file_content.decoded_content.decode()
    #
    # def checkin_file(self, file_path, content, commit_message):
    #     """Upload or update a file in the repository."""
    #     self.repo.update_file(file_path, commit_message, content, self.repo.get_contents(file_path).sha)
    #
    # def create_branch(self, branch_name):
    #     """Create a new branch in the repository."""
    #     source_branch = self.repo.get_branch("main")  # Assuming 'main' is the default branch
    #     self.repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source_branch.commit.sha)
    #
    # def list_branches(self):
    #     """List all branches in the repository."""
    #     return [branch.name for branch in self.repo.get_branches()]
    #
    # def get_repo_info(self):
    #     """Get repository information."""
    #     return {
    #         "name": self.repo.name,
    #         "description": self.repo.description,
    #         "url": self.repo.html_url,
    #         "branches": self.list_branches()
    #     }

# Example usage
if __name__ == "__main__":
    manager = GitHubManager()
    pprint(manager)
    # print(manager.checkout_file("path/to/your_file.html"))

    f = manager.get_file(os.getenv("GITHUB_FILE_PATH", ""))
    pprint(type(f))
    pprint(dir(f))
    print('rawdata:')
    pprint(f.raw_data)
    pprint(f.raw_data['content'])
    pprint(f.decoded_content)

