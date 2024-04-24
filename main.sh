#!/bin/sh -l
python /main.py --openai-api-key "$1" --github-token "$2" --openai-engine "$5" --openai-temperature "$6" --openai-max-tokens "$7"