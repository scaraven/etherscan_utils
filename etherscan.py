#!/usr/bin/env python3
import argparse
import json
import os
import requests

parser = argparse.ArgumentParser(description='Download contracts from etherscan')
parser.add_argument('address', help='Address of contract to be read')
parser.add_argument('--key', help='API Key for etherscan', default='')
parser.add_argument('--lib', help='Download libraries', action='store_true')
parser.add_argument('--path', help='Path for files', default='')
args = parser.parse_args()
address, key, lib, path = args.address, args.key, args.lib, args.path
print(path)

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
sources = json.loads(content[1:-1])['sources']
names = sources.keys()

for name in names:
    #if name starts with @ then we can ignore because a library is being used
    if name[0] != '@' or lib == True:
        code = sources[name]['content']
        file_name = name.split('/')[-1]
        dir_path = '/'.join(name.split('/')[0:-1])
        full_dir_path = os.path.join(path, dir_path)
        if os.path.isdir(full_dir_path) == False:
            os.makedirs(full_dir_path)
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path) == False:
            with open(file_path, 'w') as writer:
                writer.write(code)
        else:
            print("Path exists: %s, skipping..." % (file_path))

"""
except:
    #if we have an error then we have just one file and we can save directly
    name = json.loads(r.text)['result'][0]['ContractName']
    path = os.path.join(os.getcwd(), name+'.sol')
    if os.path.isfile(path) == False:
        with open(path, 'w') as writer:
            writer.write(content)
    else:
        print("Path exists: %s, skipping..." % (path))
"""
