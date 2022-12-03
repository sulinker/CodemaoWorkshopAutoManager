#用于生成积分排行
#用的是计数排序（我懒），若有人积分超9999会报错（懂的都懂）
import json

with open("mark.json","r",encoding="utf-8") as f:
	mark = json.load(f)

ks = mark.keys()

ls = [];
tong = [[] for i in range(10000)];

for i in ks:
	tong[mark[i]["mark"]].append([mark[i]["name"],mark[i]["mark"]])

ming = 1;
for i in range(len(tong)-1,-1,-1):
	if tong[i] == []:
		continue;
	for j in tong[i]:
		print("第",ming,f"名：{j[0]}   {j[1]}分")
		ming+=1;