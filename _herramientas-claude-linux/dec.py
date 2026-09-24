import json,base64,sys,os
src,dst=sys.argv[1],sys.argv[2]
d=json.load(open(src))
open(dst,'wb').write(base64.b64decode(d['content']))
print(dst, os.path.getsize(dst), d.get('title'))
