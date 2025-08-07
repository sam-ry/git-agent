# git-agent
summarizes recent commit history
# GitHub Commit Summary AI Agent

This Python-based AI Agent connects to your GitHub account, fetches your recent commits from past few days, and summarizes them using the OpenRouter API with the LLaMA 3 70B Instruct model.

Ideal for developers who want a natural language summary of their recent work.

---

## Requirements

- Python 3.8+
- GitHub Personal Access Token (PAT)
- OpenRouter API Key

---

## Setup Instructions

### 1. Get GitHub Personal Access Token (PAT)

1. Go to [GitHub Settings → Developer Settings → Personal Access Tokens](https://github.com/settings/tokens).
2. Choose either:
   - **Fine-grained tokens**, or
   - **Tokens (classic)**
3. Click **"Generate new token"**.
4. Select the following scopes:
   - `read:user`
   - `repo` (only if you want to access private repositories)
5. Generate and **copy the token**.

---

### 2. Get OpenRouter API Key

1. Go to [OpenRouter](https://openrouter.ai).
2. Create a new API key and **copy it**.

---

### 3. Create a `.env` File

In your project root directory, create a file named `.env` with the following contents:

```env
GITHUB_USERNAME=your-github-username
GITHUB_TOKEN=your-github-pat
OPENROUTER_API_KEY=your-openrouter-api-key
