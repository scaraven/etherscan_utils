#!/usr/bin/env python3
import argparse
import json
import os
import requests

parser = argparse.ArgumentParser(description='Download contracts from etherscan')
parser.add_argument('address', help='Address of contract to be read')
parser.add_argument('--key', help='API Key for etherscan', default='')
parser.add_argument('--lib', help='Download libraries', action='store_true')
args = parser.parse_args()
address, key, lib = args.address, args.key, args.lib

params = {
    "module": "contract",
    "action":"getsourcecode",
    "address":address,
    "apikey":key
}
r = requests.get("https://api.etherscan.io/api", params=params)
#get source code of all files
content = json.loads(r.text)['result'][0]['SourceCode']
#remove last and first character because json doesn't like extra curly brackets

#try opening if we have multiple files
try:
    sources = json.loads(content[1:-1])['sources']
    names = sources.keys()

    for name in names:
        #if name starts with @ then we can ignore because a library is being used
        if name[0] != '@' or lib == True:
            code = sources[name]['content']
            path = os.path.join(os.getcwd(), name)
            if os.path.isfile(path) == False:
                with open(path, 'w') as writer:
                    writer.write(code)
            else:
                print("Path exists: %s, skipping..." % (path))

except:
    #if we have an error then we have just one file and we can save directly
    name = json.loads(r.text)['result'][0]['ContractName']
    path = os.path.join(os.getcwd(), name+'.sol')
    if os.path.isfile(path) == False:
        with open(path, 'w') as writer:
            writer.write(content)
    else:
        print("Path exists: %s, skipping..." % (path))
