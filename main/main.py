# -*- coding: utf-8 -*-

'''
Created on 14/11/2012

@author: Carlos

This program search a extension in URL page and stores in clipboard

'''
import urllib2
from bs4 import BeautifulSoup
import re
import xerox

class urlExtension:
    
    def __init__(self, url, extension, forbidden=[]):
        self.url = url
        self.extension = extension
        self.forbidden = forbidden
        self.linkList = '' # list of links to Clipboard

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
        webs = ['cs50.tv'] # all exceptions
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
                                print href
                                string = href  
                    except KeyError: pass
        return string
        
    
    def insertInList(self, string):        
        self.linkList += '\n' + self.listOfExceptions(string)
        
        
    def searchLink(self):
        bsLink = BeautifulSoup(self.getPage(self.url))    
        allLinks = bsLink.findAll('a')
        for link in allLinks:
            try:
                href = link['href']
                
            except KeyError: 
                href = ''
                pass
            if href:
                for ext in self.extension:              
                        if ext in href:
                            if self.forbidden:
                                for forb in self.forbidden:
                                    if forb not in href:
                                        print href                               
                                        self.insertInList(href)    
                                        
                            else:
                                print href
                                self.insertInList(href)
            
            
        
        print self.linkList
        xerox.copy(self.linkList)




            
class main():
    url = ''
    while not url:
        url = raw_input('Introduce la url en la que quieres buscar enlaces con extensiones ')
    extensions = raw_input('Introduce las extensiones a buscar (separadas por comas) ')
    extensions = re.split(',',extensions)
    print extensions
    forbidden = raw_input('Introduce las extensiones a excluir dentro de la url con esas extensiones ')
    u = urlExtension(url,extensions, forbidden)
    u.searchLink()
    
if __name__ == '__main__':
    main()