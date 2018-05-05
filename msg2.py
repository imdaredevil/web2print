import requests
import json
class sms2:
	def __init__(self,username,password):
		self.cred={'username': username, 'password': password};
		self.url = 'https://smsapi.engineeringtgr.com/send/'		
		self.apikey = 'cibi_VfbKwjgXBCHhQviD6URqy3'
	
	def send(self,mobileno,message):
		payload = { 'Mobile':self.cred['username'] , 'Password':self.cred['password'], 'Message':message,'To':mobileno ,'Key': self.apikey };
		response = requests.get(self.url,payload)
		print(response.text)
		response = json.loads(response.text);
		return (response['status'] == 'success')
		 	
	
