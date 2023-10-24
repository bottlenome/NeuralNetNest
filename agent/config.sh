#!/bin/bash -eu
GITHUB_OWNNER="bottlenome"
GITHUB_REPO="NeuralNetNest"
WANDB_SCORE_NAME="cv"
SCORE_DIRECTION="minimize"
EXP_CODE_PATH=${1:-"../run.py"}
LLM_MODEL="gpt-4"