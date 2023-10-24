"""
action_itemの記述に沿って元コードを改修した新しいコードを生成する
"""

import argparse
from langchain.prompts import PromptTemplate 
from langchain.llms import OpenAI
from pydantic import ValidationError


template = """
以下の要約とdiffを元に，gitのコミットメッセージを生成してください。
返答内容はコミットメッセージだけとします。
要約:
{action_item}

diff:
{diff}
"""

parser = argparse.ArgumentParser()
parser.add_argument("--action_item", required=True)
parser.add_argument("--diff", required=True)
parser.add_argument("--llm_model", default="text-davinci-003", required=True)
args = parser.parse_args() 

action_item = args.action_item
diff = args.diff
llm_model = args.llm_model

prompt = PromptTemplate(template=template, input_variables=["action_item", "diff"])
prompt_text = prompt.format(action_item=action_item, diff=diff)
print(prompt_text)
llm = OpenAI(model_name=llm_model)
commit_message = llm(prompt_text)
print(commit_message)