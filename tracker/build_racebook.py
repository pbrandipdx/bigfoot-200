import json
data=json.load(open("weeks.json"))
head=open("racebook_head.html").read()
body=open("racebook_body.html").read()
js=open("racebook_js.html").read().replace("/*__DATA__*/", json.dumps(data,separators=(",",":")))
open("racebook.html","w").write(head+"\n"+body+"\n"+js)
print("built racebook.html")
