import json, sys
data = json.load(open("weeks.json"))
tpl = open("template.html").read()
out = tpl.replace("/*__DATA__*/", json.dumps(data, separators=(",",":")))
open("bigfoot-tracker.html","w").write(out)
print("built", len(out), "bytes")
