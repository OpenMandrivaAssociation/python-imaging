#!/bin/sh
json() {
	python -c "
import json,sys   
try:
	print(json.load(sys.stdin)$@)
except IndexError:
	pass
"
}

curl --fail https://pypi.org/pypi/pillow/json 2>/dev/null |json "['info']['version']"
