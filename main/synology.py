'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Created on 25/11/2012

@author: Carlos
'''
import urllib, urllib2
from requests import session
import json
import base64

class synology():
    def __init__(self, ip, account, password):
        self.ip = ip
        self.account = account
        self.password = password
        self.session = session()
        
    def login(self):       
        login = self.session.post(self.ip + '/webapi/auth.cgi', data={"api": "SYNO.API.Auth", "version": "2", "method": "login", "account": self.account, "passwd": base64.b64decode(self.password), "session": "DownloadStation", "format": "cookie"})
        o = json.loads(login.text)
        if o["success"] == True:
            return True
        else:
            error = o['error']['code']
            if error == 400:
                print 'No such account or incorrect password'
            elif error == 401:
                print 'Guest account disabled'
            elif error == 402:
                print 'Account disabled'
            elif error == 403:
                print 'Wrong password'
            elif error == 404:
                print 'Permission denied'
            return False
    def logout(self):
        logout = self.session.post(self.ip + '/webapi/auth.cgi', data={"api": "SYNO.API.Auth", "version": "1", "method": "logout", "session": "DownloadStation"})
        o = json.loads(logout.text)
        if o["success"] == True:
            return True
        else:
            print o
            return False
    def addDownload(self, url):
        if self.login():
            request = self.session.post(self.ip + '/webapi/DownloadStation/task.cgi', data={"api": "SYNO.DownloadStation.Task", "version": "1", "method": "create", "uri": url})
            o = json.loads(request.text)
            if o["success"] == True:
                print 'add success'
                return True
            else:
                print o
                print 'error adding'
                return False
            self.logout()
            
        else:
            print "No se ha podido entrar en la sesion"
            
    