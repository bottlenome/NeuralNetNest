#!/bin/bash -eu
source config.sh

# mainブランチ同期
git checkout main
git pull origin main
# agent用の親ブランチ作成・チェックアウト
# parent_branch=agent$(date +"%Y%m%d%H%M%S")
# git checkout -b $parent_branch
# git push -u origin $parent_branch

# 実験ループ
while true; do
    # githubのissuesから実験内容を取得
    IFS=$'\n' read -d '' -r -a values < <(python get_action_item.py --owner $GITHUB_OWNNER --repo $GITHUB_REPO && printf '\0')
    issue_number=${values[0]}
    action_item=${values[1]}

    echo ${values[0]}
    echo ${values[1]}
    # openのissuesがなかったらループを抜けて終了
    if [ "$issue_number" -eq -1 ]; then
        break
    fi

    issue_summary=$(python get_issue_summary.py --owner $GITHUB_OWNNER --repo $GITHUB_REPO --issue_number $issue_number)
    # 子ブランチ作成・チェックアウト
    child_branch=feature-$issue_number$issue_summary
    git checkout -b $child_branch
    if [ $? -ne 0 ]; then
        git checkout $child_branch
    fi

    # 実験内容から新しいexpコードを生成
    python generate_new_exp_code.py --exp_code_path $EXP_CODE_PATH --action_item "$action_item" --llm_model $LLM_MODEL
    if [ $? -ne 0 ]; then
        echo "Failed to generate new exp code" 1>&2
        break
    fi

    # expコードの実行
    # Check EXP_CODE_PATH is python file or not
    python $EXP_CODE_PATH
    if [ $? -ne 0 ]; then
        echo "Failed to run exp code" 1>&2
        break
    fi

    # wandbのNotesに実験内容を書き込み
    # python write_wandb_latest_run_notes.py --notes $action_item

    # 変更点をgithubに登録
    git add -u
    # make commit message
    commit_message=$(python make_commit_message.py --action_item "$action_item" --diff "$(git diff main $EXP_CODE_PATH)" --llm_model $LLM_MODEL)
    git commit -m "$commit_message"
    git push -u origin $child_branch

    # PRを作成
    python create_pr.py --owner $GITHUB_OWNNER --repo $GITHUB_REPO --title "for issue $issue_number" --issue_num $issue_number --head $child_branch --base main

    git checkout main
    break
done