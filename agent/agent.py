import subprocess
import os

# ユーティリティ関数: コマンド実行とエラーチェック
def run_command(cmd, capture_output=False):
    result = subprocess.run(cmd, capture_output=capture_output, text=True, shell=True, check=False)
    if result.returncode != 0:
        raise Exception("Command failed: " + cmd)
    if capture_output:
        return result.stdout.strip()

# 設定を読み込む
from config import *

# mainブランチ同期
run_command("git checkout main")
run_command("git pull origin main")

while True:
    # GitHubのissuesから実験内容を取得
    action_item_output = run_command(f"python get_action_item.py --owner {GITHUB_OWNNER} --repo {GITHUB_REPO}", capture_output=True)
    issue_number, action_item = action_item_output.split('\n')
    
    print(issue_number)
    print(action_item)

    # openのissuesがなかったらループを抜けて終了
    if int(issue_number) == -1:
        break

    issue_summary = run_command(f"python get_issue_summary.py --owner {GITHUB_OWNNER} --repo {GITHUB_REPO} --issue_number {issue_number}", capture_output=True)
    child_branch = f"feature-{issue_number}{issue_summary}"

    EXP_CODE_PATH = run_command(f"python get_exp_code_path.py --issue_summary '{issue_summary}' --llm_model {LLM_MODEL}", capture_output=True)
    
    # 子ブランチ作成・チェックアウト
    try:
        run_command(f"git checkout -b {child_branch}")
    except:
        run_command(f"git checkout {child_branch}")

    # 実験内容から新しいexpコードを生成
    run_command(f"python generate_new_exp_code.py --exp_code_path {EXP_CODE_PATH} --action_item '{action_item}' --llm_model {LLM_MODEL}")

    # expコードの実行
    run_command(f"python {EXP_CODE_PATH}")

    # 変更点をGitHubに登録
    run_command("git add -u")
    commit_message = run_command(f"python make_commit_message.py --action_item '{action_item}' --diff '$(git diff main {EXP_CODE_PATH})' --llm_model {LLM_MODEL}", capture_output=True)
    run_command(f"git commit -m '{commit_message}'")
    run_command(f"git push -u origin {child_branch}")

    # PRを作成
    run_command(f"python create_pr.py --owner {GITHUB_OWNNER} --repo {GITHUB_REPO} --title 'for issue {issue_number}' --issue_num {issue_number} --head {child_branch} --base main")

    run_command("git checkout main")
    break