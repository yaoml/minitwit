import httplib
conn = httplib.HTTPConnection("shorturl.baiku.cn")
conn.request("GET", "/?url=http://www.baidu.com/")
r1 = conn.getresponse()
print r1.status, r1.reason
data1 = r1.read()
print data1
conn.close()