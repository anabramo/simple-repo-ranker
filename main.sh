#!/bin/sh -l
python /main.py --openai-api-key "$1" --github-token "$2" --openai-engine "$3" --openai-temperature "$4" --openai-max-tokens "$5"