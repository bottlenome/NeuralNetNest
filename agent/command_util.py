import subprocess

# ユーティリティ関数: コマンド実行とエラーチェック
def run_command(cmd, capture_output=False):
    try:
        result = subprocess.run(cmd, capture_output=capture_output, text=True, shell=True, check=True)
        if capture_output:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command failed: {cmd}. Error: {e}")