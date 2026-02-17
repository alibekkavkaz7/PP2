import json

file = open("sample-data.json")
data = json.load(file)

print("Interface Status")
print("----------------------------------------")

for i in data["imdata"]:
    attrs = i["l1PhysIf"]["attributes"]

    dn = attrs["dn"]
    description = attrs["descr"]
    speed = attrs["speed"]
    mtu = attrs["mtu"]

    print("DN:", dn)
    print("Description:", description)
    print("Speed:", speed)
    print("MTU:", mtu)
    print()
