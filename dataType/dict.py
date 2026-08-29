d = {
    "a":10,
    "b":20,
    "c":30
}
print(d)

d["d"] = 40
print(d)

di =  [{"Name":"adi","Age":25},
    {"Name":"lakshita","Age":21},
    {"Name":"gaurav","Age":25},
    {"Name":"Dhattu","Age":22}]

print(di)

print(d.keys())

for key in di:
    print(key)

for k in di:
    print(k["Name"])

for k in di:
   print(k["Age"])

#sort dict
x = sorted(di,key=lambda x:x["Name"])
print(x)

for i in di:
    i["Name"] = i["Name"].lower()
print("lower case")
print(di)

y = sorted(di, key=lambda x: x["Age"], reverse=True)
print(y)
