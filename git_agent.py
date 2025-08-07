import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Get commits from the last few days
def get_last_week_commits():
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    # since = (datetime.utcnow() - timedelta(days=7)).isoformat() + "Z"
    since = (datetime.now(timezone.utc) - timedelta(days=60)).isoformat()
    repos_url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos"
    repos = requests.get(repos_url, headers=headers).json()

    all_commits = []

    for repo in repos:
        repo_name = repo['name']
        commits_url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{repo_name}/commits?since={since}"
        commits = requests.get(commits_url, headers=headers).json()

        for commit in commits:
            commit_msg = commit.get("commit", {}).get("message", "")
            commit_date = commit.get("commit", {}).get("author", {}).get("date", "")
            if commit_msg:
                all_commits.append(f"[{repo_name}] {commit_date[:10]}: {commit_msg}")

    print(f"Collected {len(all_commits)} commit(s).")
    return all_commits

# Send commits to OpenRouter to get a summary
def summarize_with_llama(commits):
    if not commits:
        return "No commits found in the past month."

    text_block = "\n".join(commits)
    prompt = f"Summarize the following Git commit messages:\n{text_block}"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "meta-llama/llama-3-70b-instruct",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error from OpenRouter: {response.text}"

if __name__ == "__main__":
    print("Fetching commits from GitHub...")
    commits = get_last_week_commits()

    print("Summarizing with LLaMA-3 via OpenRouter...\n")
    summary = summarize_with_llama(commits)

    print("Your Commit Summary:\n")
    print(summary)