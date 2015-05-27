import jenkins
from pygerrit.rest import GerritRestAPI
from requests.auth import HTTPDigestAuth
import requests

class BuildInfo(object):

	def __init__(self,change_id):
		self.change_id=change_id

	def get_build_url(self):
		gerrit_auth = HTTPDigestAuth('shangchunlei', '60gelr2RLEd8XZQgz+XqI2lRZBMSgQQt+g7V76Yf0A')
		rest = GerritRestAPI(url='http://10.3.3.15:8080', auth=gerrit_auth)
		detail=rest.get('/changes/'+self.change_id+'/detail')
		url=detail['messages'][1]['message'].split(" ")[-1]
		return url

	def get_build_info(self):
		url=buildinfo.get_build_url()
		jenkins_auth=('jenkins', 'jenkins')
		info=requests.get(url+'consoleText',auth=jenkins_auth)
		with open('buildinfo.text','w+') as f:
			f.write(info.text)

if __name__=='__main__':
	change_id='Ib3305e6f109566293836494f3a4e297d8468e09e'
	buildinfo=BuildInfo(change_id)
	buildinfo.get_build_info()

