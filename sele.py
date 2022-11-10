from selenium import webdriver as wd
from selenium.webdriver.common.by import By
import requests as r
import time
import sys,os
from html.parser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc
class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()
def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text
br=wd.Firefox()
#l=['https://www.zhihu.com/collection/%s'%a.split('"')[0]for a in r.get('https://www.zhihu.com/people/lao-liang-83-95/collections').text.split('href="/collection/')[1:]]
did='gong-ge-cheng-52'
l=[]
h=r.get('https://www.zhihu.com/people/%s/collections'%did).text
if'<div class="Pagination">'in h:
    p=int(h.split('<div class="Pagination">')[1].split('下一页')[0].split('</button>')[-2:][0].split('>')[1])
else:p=1
for a in range(p):
    br.get('https://www.zhihu.com/people/%s/collections?page=%d'%(did,p-a))
    time.sleep(3)
    h=br.page_source
    h=['https://www.zhihu.com/collection/%s'%b.split('"')[0]for b in h.split('href="/collection/')[1:]]
    h2=[]
    for b in range(len(h)):
        h2.append(h[len(h)-1-b])
    h=h2
    l.extend(h)
fl=[]
h=r.get('https://www.zhihu.com/people/%s/collections/following'%did).text
if'<div class="Pagination">'in h:
    p=int(h.split('<div class="Pagination">')[1].split('下一页')[0].split('</button>')[-2:][0].split('>')[1])
else:p=1
for a in range(p):
    br.get('https://www.zhihu.com/people/%s/collections/following?page=%d'%(did,p-a))
    time.sleep(3)
    h=br.page_source
    h=['https://www.zhihu.com/collection/%s'%b.split('"')[0]for b in h.split('href="/collection/')[1:]]
    h2=[]
    for b in range(len(h)):
        h2.append(h[len(h)-1-b])
    h=h2
    fl.extend(h)
print(l)
print(fl)
if not os.path.exists('indexs'):
    os.makedirs('indexs')
if not os.path.exists('following_indexs'):
    os.makedirs('following_indexs')
for a in l:
    t=eval(r.get('https://api.zhihu.com/collections/%s'%(i:=a.split('/collection/')[1])).text.replace('true','True').replace('false','False').replace('null',None))
    f=open('indexs/%s.dict'%i,'w+');f.write(repr(t));f.close()
for a in fl:
    t=eval(r.get('https://api.zhihu.com/collections/%s'%(i:=a.split('/collection/')[1])).text.replace('true','True').replace('false','False').replace('null',None))
    f=open('following_indexs/%s.dict'%i,'w+');f.write(repr(t));f.close()
nnn=0
for a in l:
    nnn+=1
    print('第%d個收藏夾。'%nnn)
    if not os.path.exists(pa:='items/indexs/%s'%a.split('/collection/')[1]):os.makedirs(pa)
    br.get(a)
    time.sleep(5)
    try:nm=int(br.page_source.split('<div class="Pagination">')[1].split('<button type="button" class="Button PaginationButton PaginationButton-next Button--plain">下一页</button>')[0].split('<button type="button" class="Button PaginationButton Button--plain">')[-1:][0].split('<')[0])
    except:nm=1
    print('總計%d頁。'%nm)
    for b in range(nm):
        if os.path.exists(pp:='%s/%s.list'%(pa,str(b+1).rjust(6).replace(' ','0'))):continue
        print('第%d頁。'%(nm-b))
        br.get('%s?page=%d'%(a,nm-b))
        time.sleep(5)
        it=[{'data-za-extra-module':eval(dehtml(c.split('data-za-extra-module="')[1].split('"')[0]).replace('true','True').replace('false','False').replace('null',None))}if('//www.zhihu.com/question/'not in c)else{'data-za-extra-module':eval(dehtml(c.split('data-za-extra-module="')[1].split('"')[0]).replace('true','True').replace('false','False').replace('null',None)),'link':'https://www.zhihu.com/question/%s'%c.split('//www.zhihu.com/question/')[1].split('"')[0]}for c in br.page_source.split('<div class="Pagination">')[0].split('<div class="jsNavigable CollectionDetailPageItem css-vurnku">')[1:]]
        it2=[]
        for c in range(len(it)):
            it2.append(it[len(it)-c-1])
        it=it2
        print(it)
        f=open(pp,'w+');f.write(repr(it));f.close()
print('關注的收藏夾。')
for a in fl:
    nnn+=1
    print('第%d個收藏夾。'%nnn)
    if not os.path.exists(pa:='items/following/%s'%a.split('/collection/')[1]):os.makedirs(pa)
    br.get(a)
    time.sleep(5)
    try:nm=int(br.page_source.split('<div class="Pagination">')[1].split('<button type="button" class="Button PaginationButton PaginationButton-next Button--plain">下一页</button>')[0].split('<button type="button" class="Button PaginationButton Button--plain">')[-1:][0].split('<')[0])
    except:nm=1
    print('總計%d頁。'%nm)
    for b in range(nm):
        if os.path.exists(pp:='%s/%s.list'%(pa,str(b+1).rjust(6).replace(' ','0'))):continue
        print('第%d頁。'%(nm-b))
        br.get('%s?page=%d'%(a,nm-b))
        time.sleep(5)
        it=[{'data-za-extra-module':eval(dehtml(c.split('data-za-extra-module="')[1].split('"')[0]).replace('true','True').replace('false','False').replace('null',None))}if('//www.zhihu.com/question/'not in c)else{'data-za-extra-module':eval(dehtml(c.split('data-za-extra-module="')[1].split('"')[0]).replace('true','True').replace('false','False').replace('null',None)),'link':'https://www.zhihu.com/question/%s'%c.split('//www.zhihu.com/question/')[1].split('"')[0]}for c in br.page_source.split('<div class="Pagination">')[0].split('<div class="jsNavigable CollectionDetailPageItem css-vurnku">')[1:]]
        it2=[]
        for c in range(len(it)):
            it2.append(it[len(it)-c-1])
        it=it2
        print(it)
        f=open(pp,'w+');f.write(repr(it));f.close()
br.quit()
