import argparse
import openai
import json
import os
import requests
from github import Github, PullRequest

github_client: Github
parameters: dict

from github import Github

def commit_file_to_repo(file_path, file_content, commit_message):
    """
    Commit a file to a given GitHub repository.

    Args:
    github_token (str): GitHub access token.
    repo_name (str): Repository name in the format 'username/repository'.
    file_path (str): Path within the repository to place the file.
    file_content (str): Content to write to the file.
    commit_message (str): Commit message.

    Returns:
    bool: True if commit is successful, False otherwise.
    """
    try:
        repo_name = r'anabramo/simple-repo-ranker'
        # Get the repository
        repo = github_client.get_repo(repo_name)
        
        # Check if the file already exists in the repository
        try:
            contents = repo.get_contents(file_path)
            # If the file exists, update it
            repo.update_file(contents.path, commit_message, file_content, contents.sha)
            print("File updated in the repository.")
        except:
            # If the file does not exist, create it
            repo.create_file(file_path, commit_message, file_content)
            print("File created in the repository.")
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



def repo_rankings(parameters: dict):

    repositories = [r'pandas-dev/pandas', r'facebook/react' ]

    data = {}
    for repo in repositories:
        data[repo] = extract_repo_data(repo, parameters)

    with open('repo_data.json', 'w') as fp:
        json.dump(data, fp)

    print(data)

    commit_file_to_repo('data.json', json.dumps(data), 'Update ranking data')

    return data


def generate_ai_report(data):
    try:
        response = openai.ChatCompletion.create(
            model=parameters['model'],
            messages=[
                {
                    "role" : "user",
                    "content" : (f"{parameters['prompt']}:\n```{data}```")
                }
            ],
            temperature=parameters['temperature']
        )

    except Exception as ex:
        message = f"Fail code review process for file.\n\n`{str(ex)}`"

    return response


def extract_repo_data(repo: str, parameters: dict):
    # Get the repository object from GitHub
    repository = github_client.get_repo(repo)
    
    # Get contributors list, this might return a lot of data
    # You can limit the number of contributors you fetch by using `.get_contributors()[:N]` where N is the number of top contributors you want
    contributors = repository.get_contributors()
    
    top_contributors = []
    for contributor in contributors:
        # You might want to store more detailed information about each contributor
        top_contributors.append({
            'login': contributor.login,
            'contributions': contributor.contributions
        })
    
    # Return top contributors data
    return {'top_contributors': top_contributors}


def make_prompt() -> str:
    review_prompt = f"Review this json file with a list of repository information and return a list of repositories by quality"

    return review_prompt



if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--openai-api-key', help='Your OpenAI API Key')
    parser.add_argument('--github-token', help='Your Github Token')
    parser.add_argument('--openai-engine', default="gpt-3.5-turbo", help='GPT-3.5 model to use. Options: text-davinci-003, text-davinci-002, text-babbage-001, text-curie-001, text-ada-001')
    parser.add_argument('--openai-temperature', default=0.0, help='Sampling temperature to use. Higher values means the model will take more risks. Recommended: 0.5')
    parser.add_argument('--openai-max-tokens', default=4096, help='The maximum number of tokens to generate in the completion.')
    
    args = parser.parse_args()

    openai.api_key = args.openai_api_key
    github_client = Github(args.github_token)

    review_parameters = {
        "prompt" : make_prompt(),
        "temperature" : float(args.openai_temperature),
        "max_tokens" : int(args.openai_max_tokens),
        "model" : args.openai_engine
    }

    repo_rankings(parameters=review_parameters)