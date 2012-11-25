# -*- coding: utf-8 -*-

'''
Created on 14/11/2012

@author: Carlos Simón <jcarlosimonv@gmail.com>

With this program you can 

'''
import urllib2
from bs4 import BeautifulSoup
import re
import xerox
from youtube import *
from synology import synology
import base64

class InvalidProtocol(Exception):
    def __init_(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class URLChecking:
    def __init__(self, url):
        self.url = url
        self.PROTOCOLS = ['ftp', 'smtp']

    def checkURL(self):
        if not (self.url.startswith('http://') or self.url.startswith('https://'))  :
            if self.url.startswith('www'):
                self.url = 'http://' + self.url
                return self.url                              
            for protocol in self.PROTOCOLS:
                if self.url.startswith(protocol):
                    print 'Wrong protocol. Only accept http protocol'
                    return False       
        else:
            return self.url


class urlExtension:
    
    def __init__(self, url, extension, forbidden=[], syn = 'N', syndata= dict()):
        self.url = url
        self.extension = extension
        self.forbidden = forbidden
        self.linkList = '' # list of links to Clipboard
        self.commaList = '' # list of links to synlogoy
        self.syn = {}
        if syn == 'Y' and syndata:
            self.syn = synology(syndata['ip'], syndata['username'], syndata['password'])
        print self.forbidden



    def getPage(self, url):
        ''' Hace la peticion a la URL '''        
        
        req = urllib2.Request(url)        
        try:            
            response = urllib2.urlopen(req)
            return response.read()
        except urllib2.URLError, e:            
            return False
            print 'Error code: ', e.code
            
            
    def listOfExceptions (self, string):
        webs = ['cs50.tv', '/descargar.php']
        # webs[0] = CS50
        # webs[1] = mejorenvo
        # all exceptions
        if webs[0] in string:
            if '2012' in string:
                string = re.sub('http://cs50.tv', 'http://downloads.cs50.net', string)
            else:
                DW_VALUE = ['#download', '?download'] # Options to search in url that are interesting
                cs50tv = self.getPage(string)            
                cs50tv = BeautifulSoup(cs50tv)
                linksExceptions = cs50tv.findAll('a')
                for ln in linksExceptions:
                    try:
                        href = ln['href']
                        for value in DW_VALUE:
                            if value in href:                            
                                # print href
                                string = href  
                    except KeyError: pass
        if webs[1] in string:
            if 'mejorenvo.com' in self.url:                     
                string = 'http://www.mejorenvo.com' + string;
        return string
        
    
    def insertInList(self, string):
        linkExcept =  self.listOfExceptions(string)
        self.linkList += '\n' + linkExcept
        self.commaList += ',' + linkExcept
        
        
    def searchLink(self):
        try:
            bsLink = BeautifulSoup(self.getPage(self.url))        
        except InvalidProtocol:
            print 'You must provide a valid protocol. Ej. HTTP'
            while not self.url:
                self.url = raw_input('Insert URL: ')
                bsLink = BeautifulSoup(self.getPage(self.url))
        allLinks = bsLink.findAll('a')
        # print allLinks
        for link in allLinks:
            try:
                href = link['href']                
            except KeyError: 
                href = ''
                pass
            if href:
                for ext in self.extension:
                                 
                    if ext in href:
                        
                        if len(self.forbidden) == 0:                            
                            for forb in self.forbidden:
                                if forb not in href:
                                    print href                               
                                    self.insertInList(href)                                       
                        else:                            
                            # print href
                            self.insertInList(href)      
        
#        try:
#            xerox.copy(self.linkList)
#            print 'Links copied on clipboard'
#            print self.linkList 
#        except XclipNotFound:
#            print self.linkList
        
        if self.syn:
            self.syn.addDownload(self.commaList)


class main():
    url = ''
    synology = ''
    while not url:
        url = raw_input('Insert URL: ')
        url = URLChecking(url).checkURL()        
    
    extensions = raw_input('Insert search extensions (comma separated): ')
    extensions = re.split(',',extensions)
    # print extensions
    forbidden = raw_input('Insert forbidden keywords on URL (comma separated): ')
    forbidden = re.split(',', forbidden)
    
    synology = raw_input('Do you want to send links to synology: (Y/N) ')
    if synology == 'Y':
        ip = raw_input('Input URL of Synology DiskStation: ')
        username = raw_input('Insert username of synology (You must have rights to DownloadStation): ')
        password = base64.b64encode(raw_input('Input your password'))
        syndata = {'ip': ip, 'username': username, 'password': password}
        u = urlExtension(url,extensions, forbidden, synology, syndata)
    else:
        u = urlExtension(url,extensions, forbidden)
    u.searchLink()
    
if __name__ == '__main__':
    main()