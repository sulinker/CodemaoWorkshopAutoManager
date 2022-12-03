import requests, json


class Posts:
	def __init__(self, hd):
		self.hd = hd

	def sendReview(self, id, text):
		self.review_url = f"https://api.codemao.cn/web/forums/posts/{id}/replies"
		self.data = {"content": text}
		self.result = requests.post(self.review_url, headers=self.hd, json=self.data)
		return self.result

	def getPosts(self, id):
		self.details_url = f"https://api.codemao.cn/web/forums/posts/{id}/details"
		self.result = requests.get(self.details_url)
		return [self.result, json.loads(self.result.text)]

	def sendPosts(self, title, content):
		self.data = {"title": title, "content": content}
		self.sendPosts_url = "https://api.codemao.cn/web/forums/boards/7/posts"
		self.result = requests.post(self.sendPosts_url, headers=self.hd, json=self.data)
		return [self.result, json.loads(self.result.text)]

	def getReviews(self, id, page, limit, sort="-created_at"):
		self.url = f"https://api.codemao.cn/web/forums/posts/{id}/replies?page={page}&limit={limit}&sort={sort}"
		self.result = requests.get(self.url)
		return [self.result, json.loads(self.result.text)]

	def getMyPosts(self, page, limit):
		self.url = f"https://api.codemao.cn/web/forums/posts/mine/created?page={page}&limit={limit}"
		self.result = requests.get(self.url,headers=self.hd)
		return [self.result,json.loads(self.result.text)]

class Works:
	def __init__(self, hd):
		self.hd = hd

	def like(self, id):
		self.like_url = f"https://api.codemao.cn/nemo/v2/works/{id}/like"
		self.result = requests.post(self.like_url, headers=self.hd)
		return [self.result, json.loads(self.result.text)]

	def dislike(self, id):
		self.dislike_url = f"https://api.codemao.cn/nemo/v2/works/{id}/like"
		self.result = requests.delete(self.dislike_url, headers=self.hd)
		return [self.result, json.loads(self.result.text)]

	def sendReview(self, id, text, emoji=""):
		self.sendReview_url = f"https://api.codemao.cn/creation-tools/v1/works/{id}/comment"
		self.data = {"content": text, "emoji_content": emoji}
		self.result = requests.post(self.sendReview_url, json=self.data, headers=self.hd)
		return [self.result, json.loads(self.result.text)]

	def getReviews(self, id, num, start=0):
		self.url = f"https://api.codemao.cn/creation-tools/v1/works/{id}/comments?offset={start}&limit={num}"
		self.result = requests.get(self.url, self.hd)
		return [self.result, json.loads(self.result.text)]


class WorkShop:
	def __init__(self, hd):
		self.hd = hd

	def getDetail(self, urid):
		self.url = f"https://api.codemao.cn/web/shops/{urid}"
		self.result = requests.get(self.url)
		return [self.result, json.loads(self.result.text)]

	def getwsid(self, urid):  # wsid：真正的工作室id；urid：url中的工作室id
		self.id = self.getDetail(urid)[1]
		self.id = self.id["shop_id"]
		return self.id

	def getHeadurl(self, urid):
		self.headurl = self.getDetail(urid)[1]
		self.headurl = self.headurl["preview_url"]
		return self.headurl

	def getlevel(self, urid):
		self.level = self.getDetail(urid)[1]["level"]
		return self.level

	def audit(self, wsid, user_id, 可以吗):
		self.url = "https://api.codemao.cn/web/work_shops/users/audit"
		if 可以吗:
			self.data = {'id': wsid, 'user_id': user_id, 'status': "ACCEPTED"}
		else:
			self.data = {'id': wsid, 'user_id': user_id, 'status': "UNACCEPTED"}
		self.result = requests.post(self.url, json=self.data, headers=self.hd)
		print("audit")
		return self.result

	def updateDetail(self, wsid, description, name, head_url):
		self.url = "https://api.codemao.cn/web/work_shops/update"
		self.data = {"description": description, "id": wsid, "name": name, "preview_url": head_url}
		self.result = requests.post(self.url, headers=self.hd, json=self.data)
		return self.result

	def sendReview(self, urid, text):
		self.url_fasong = f"https://api.codemao.cn/web/discussions/{urid}/comment"
		self.data = {"content": text, "rich_content": text, 'source': "WORK_SHOP"}
		self.result = requests.post(self.url_fasong, json=self.data, headers=self.hd)
		#print("send")
		return self.result

	def getWillJoin(self, wsid, offset=0, limit=40):
		self.url = f"https://api.codemao.cn/web/work_shops/users/unaudited/list?offset={offset}&limit={limit}&id={wsid}"
		self.result = requests.get(self.url,headers=self.hd)
		return [self.result,json.loads(self.result.text)]

	def getMembers(self,urid,limit=100,offset=0):
		self.url = f"https://api.codemao.cn/web/shops/{urid}/users?limit={limit}&offset={offset}"
		self.result = requests.get(self.url,headers = self.hd)
		return [self.result, json.loads(self.result.text)]

	def getReviews(self, urid, offset=0, limit=20):
		self.url = f"https://api.codemao.cn/web/discussions/{urid}/comments?source=WORK_SHOP&sort=-created_at&limit={limit}&offset={offset}"
		self.result = requests.get(self.url,headers=self.hd)
		return [self.result,json.loads(self.result.text)]

	def likeReview(self,messageid):
		self.url = f'https://api.codemao.cn/web/discussions/comments/{messageid}/liked';
		self.result = requests.put(self.url,headers=self.hd);
		return self.result;

	def replyReview(self,text,urid,messageid,parent = 0):
		self.url = f'https://api.codemao.cn/web/discussions/{urid}/comments/{messageid}/reply'
		self.data = {"parent_id": parent, "content": text, "source": "WORK_SHOP"};
		self.result = requests.post(self.url, json=self.data, headers=self.hd)
		return self.result;

	def getWorks(self,urid,offset,limit):
		self.url = f"https://api.codemao.cn/web/works/subjects/{urid}/works?&offset={offset}&limit={limit}&sort=-created_at,-id&user_id=-2&work_subject_id={urid}"
		self.result = requests.get(self.url)
		return [self.result,json.loads(self.result.text)]

	def getAllWorks(self,urid):
		self.YE = 50
		self.r = self.getWorks(urid,0,5)
		self.total = self.r[1]["total"]
		self.n = self.total//self.YE
		self.end = []
		for self.i in range(self.n+1):
			self.r = self.getWorks(urid,self.YE*self.i,self.YE)[1]['items']
			self.l = len(self.r)
			for self.j in self.r:
				self.end.append({"workId":self.j["id"],"workName":self.j["name"],"creatorId":self.j["user"]["id"],"creatorName":self.j["user"]["nickname"]})

		return self.end

	def removeWork(self,wsid,workid):
		self.url = f"https://api.codemao.cn/web/work_shops/works/remove?id={wsid}&work_id={workid}"
		self.result = requests.post(self.url,headers = self.hd)
		return self.result

	def removeMember(self,wsid,userId):
		self.url = f"https://api.codemao.cn/web/work_shops/users/remove"
		self.data = {"id":wsid,"user_id":userId}
		self.result = requests.post(self.url,headers = self.hd,json = self.data)
		return self.result

class User:
	def __init__(self, hd):
		self.hd = hd;

	def getDetail(self,id):
		self.url = f"https://api.codemao.cn/creation-tools/v1/user/center/honor?user_id={id}"
		self.result = requests.get(self.url,headers=self.hd)
		return [self.result,json.loads(self.result.text)]

	def getLike(self,id):
		try:
			return self.getDetail(id)[1]['liked_total']
		except:
			print(self.getDetail(id))
			print(id)
			return -1


if __name__ == "__main__":
	header = {
	"cookie": "gr_user_id=c642ffc9-f09c-4055-a213-01d6d6f3b94e; _ga=GA1.2.687291060.1624162386; pt_3f199b24=uid=gd-QEr3vO1qHiyCX4BiTXw&nid=1&vid=cOMstRBBF9rygNno9V85Pw&vn=1&pvn=1&sact=1624691710269&to_flag=0&pl=yjl0539-wRuei/gcImp9fA*pt*1624691660531; SL_C_23361dd035530_KEY=be556a167e74fcde3a3444e29b25f8e99fb0c59f; Hm_lvt_1d120ad5df69bc82535c08f98ad2c1e7=1636778778; SL_C_23361dd035530_VID=eYLrFx0HdS; __ca_uid_key__=28ff84d9-4cf5-4bb6-9fc4-1ce7b4ba483e; authorization=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJDb2RlbWFvIEF1dGgiLCJ1c2VyX3R5cGUiOiJzdHVkZW50IiwiZGV2aWNlX2lkIjowLCJ1c2VyX2lkIjoxMDA0MjI0MiwiaXNzIjoiQXV0aCBTZXJ2aWNlIiwicGlkIjoiQU5OUnZIWlQiLCJleHAiOjE2NTI5NjUzODQsImlhdCI6MTY0OTA3NzM4NCwianRpIjoiODc2ZWRiZmMtNGJjMi00NTYxLWI4ODAtZTllNGEwYTg2Mzg1In0.ydgmp1MYIA3EGKvg5VPQGLBPLLqtB0pWQQrmqQwTL5w; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2212744072%22%2C%22first_id%22%3A%2217b7134af6fbc-01a99cf8a021b64-4343363-1440000-17b7134af70c1%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217b7134af6fbc-01a99cf8a021b64-4343363-1440000-17b7134af70c1%22%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfbG9naW5faWQiOiIxMjc0NDA3MiIsIiRpZGVudGl0eV9jb29raWVfaWQiOiIxN2Q5YTQ4MGY3N2ZmLTA5MWRlZmQ4YWI1ZTc2OC01N2IxOTNlLTE0NDAwMDAtMTdkOWE0ODBmNzg3MWUifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2212744072%22%7D%7D; acw_tc=707c9f7b16494674012174375e22c0a1cce7aa81f77ade7e3ccc7003af51ef"
	}
	post = Posts(header)
	works = Works(header)
	workshop = WorkShop(header)
	# rsl = post.sendPosts("测试测试测试", "aaaaaaaaaaaaaaaaaaaaaa</body>")
	# print(rsl)
	# id = json.loads(rsl[1])["id"]
	# print(id)
	# r = post.getDetails(id)[1]
	# print(r)
	# re = post.sendReview(id, r)
	# print(re)

	# re = works.like(111542484)
	# print(re)
	# re = works.dislike(111542484)
	# print(re)
	# re = works.sendReview(111542484, "测试")
	# print(re)
	# results = works.getReviews(112560902, 10, 4)
	# print(results)
	# results = post.getPosts(418861)
	# print(results)
	# results = post.getReviews(418861, 1, 8)
	# print(results)

	# result = workshop.getReviews(8129)[1]
	
	# print(result['items'][0]['is_liked'])
	# print(result['items'][0]['content'])
	# print(result['items'][0]['user']['id'])
	# print(result['items'][0]['user']['nickname'])
	# id = result['items'][0]['id']
	# print(id)
	# re = workshop.likeReview(id);
	# print(re)
	# r = workshop.replyReview('ceshi',8129,id)
	# print(r)

	r = workshop.getAllWorks(8129)
	print(r)