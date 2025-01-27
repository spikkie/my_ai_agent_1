import os
import logging
from pprint import pprint

from dotenv import load_dotenv
from github import Github, Auth, Repository, GithubException

from dataclasses import dataclass, field

# Configure logging
logging.basicConfig(filename='error.log', level=logging.ERROR)


@dataclass
class GitHubManager:
    github_auth: Auth.Token = field(init=False)
    g: Github = field(init=False)
    github_repo: Repository.Repository = field(init=False)


    def __post_init__(self):
        try:
            # Load environment variables from .env file
            load_dotenv()

            self.github_auth = Auth.Token(os.getenv("GITHUB_API_KEY", ""))
            self.g = Github(auth=self.github_auth)

            self.github_username = self.g.get_user().login
            print(self.github_username)

            self.github_repo = self.g.get_repo(f"{self.github_username}/{os.getenv('GITHUB_REPO', '')}")
            print(self.github_repo)
            # self.repo = self.g.get_repo(f"{self.github_username}/{self.github_repo}")

        except GithubException as e:
            logging.error("Failed to initialize GitHubManager: %s", str(e))
            raise


    def get_file(self, file_path):
        try:
            """Retrieve the content of a file."""
            file_content = self.github_repo.get_contents(file_path)
            return file_content
        except GithubException as e:
            logging.error("Failed to get file content: %s", str(e))
            raise


    def update_file(self, file_path, new_content, commit_message="Update file"):
        try:
            """Update the content of a file in the repository."""
            file_content = self.github_repo.get_contents(file_path)
            self.github_repo.update_file(
                file_content.path,
                commit_message,
                new_content,
                file_content.sha
            )
        except GithubException as e:
            logging.error("Failed to update file: %s", str(e))
            raise


    def modify_file_content(self, file_path):
        try:
            """Modify the content of a file."""
            file_content = self.get_file(file_path)
            current_content = file_content.decoded_content.decode()
            # Example modification: append a line
            new_content = current_content + "\n<!-- Modified by AI Agent -->"
            self.update_file(file_path, new_content)
        except Exception as e:
            logging.error("Failed to modify file content: %s", str(e))
            raise


@dataclass
class SimpleAgent:
    github_manager: GitHubManager

    def perform_task(self, file_path: str):
        try:
            # Retrieve file content
            file_content = self.github_manager.get_file(file_path)
            print("Original Content:", file_content.decoded_content.decode())

            # Modify file content
            self.github_manager.modify_file_content(file_path)
            print("File content modified and updated in the repository.")

        except Exception as e:
            logging.error("Error in performing task: %s", str(e))
            print("An error occurred while performing the task.")



if __name__ == "__main__":

    # Step 3
    manager = GitHubManager()

    agent = SimpleAgent(manager)
    agent.perform_task(os.getenv("GITHUB_FILE_PATH", ""))



    # Step 2
    # manager = GitHubManager()
    # pprint(manager)
    # print(manager.checkout_file("path/to/your_file.html"))

    # f = manager.get_file(os.getenv("GITHUB_FILE_PATH", ""))
    # pprint(type(f))
    # pprint(dir(f))
    # print('rawdata:')
    # pprint(f.raw_data)
    # pprint(f.raw_data['content'])
    # pprint(f.decoded_content)

    # mod_file  = manager.modify_file_content(os.getenv("GITHUB_FILE_PATH", ""))

