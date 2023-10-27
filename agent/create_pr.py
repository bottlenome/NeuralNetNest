import argparse
import os
import requests

def pr_github(owner, repo, title, issue_num, head, description="", base="main")
    """
    git hubのpull requestを作成する
    """
    token = os.getenv("GITHUB_TOKEN")
    if token is None:
        print("Make sure to set GUTHUB_TOKEN")
        exit()

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": "token " + token
    }

    data = {
        "title": f"{title}",
        "body": f"#{issue_num}\n{description}",
        "head": head,
        "base": base
    }
    
    res = requests.post(url, headers=headers, json=data)
    return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", type=str, default="bottlenome")
    parser.add_argument("--repo", type=str, default="NeuralNetNest")
    parser.add_argument("--title", type=str, default="test")
    parser.add_argument("--issue_num", type=int, default=1)
    parser.add_argument("--head", type=str, default="main")
    parser.add_argument("--description", type=str, default="")
    parser.add_argument("--base", type=str, default="main")
    args = parser.parse_args()

    res = pr_github(args.owner, args.repo, args.title, args.issue_num, args.head,
                    args.description, args.base)
    print(res)