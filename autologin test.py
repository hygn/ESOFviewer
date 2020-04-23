import browser_cookie3 as bc
import urllib
cjr = str(bc.firefox(domain_name="ebssw.kr")).split(">, <")
res = [i for i in cjr if "hoc26.ebssw.kr" in i] 
ck1 = res[0].split(" ")[1].split(" ")[0]
ck2 = res[1].split(" ")[1].split(" ")[0]
print(ck1 +"; "+ ck2)