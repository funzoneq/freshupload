#!/usr/bin/env python
import requests, sys, os
from pprint import pprint

def copy_to_clipboard (str):
	cmd = 'echo %s | tr -d "\n" | pbcopy' % str
	os.system(cmd)

if len(sys.argv) < 2:
    sys.stderr.write('Usage: sys.argv[0] image.jpg')
    sys.exit(1)

url = 'https://ops-arnoud-5f501c08.ewr01.tumblr.net/v1/api/upload'
fn 	= sys.argv[1]

r = requests.post(url, files={'photo': open(fn, 'rb')})
result = r.json()
if result['directurl']:
	copy_to_clipboard(result['directurl'])
	print result['directurl']