import os,time
import requests as r
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
br=wd.Firefox()
def cyreq(li):
    time.sleep(1)
    return req(li)
def req(li):
    try:return r.get(li)
    except:return cyreq(li)
def dp(li,pa):
    if not(pa[-4:]=='.htm'or pa[-5:]=='.html'):raise TypeError
    h=req(li).text
    imgs=[a.split('>')[0]for a in h.split('<img')[1:]if'src'in a.split('>')[0]]
    if not os.path.exists(p:='%s/%s_Images'%('/'.join(pa.split('/')[:-1]),'.'.join(pa.split('/')[-1:][0].split('.')[:-1]))):os.makedirs(p)
    for a in imgs:
        dwed=False
        ln=a.split('src="')[1].split('"')[0]
        if not ln[:5]=='https':
            if'data-original'in a:
                dwed=True
                ln2=a.split('data-original="')[1].split('"')[0]
                h=h.replace(ln,ln2)
                ln=ln2
            if(('data-actualsrc'in a)and(not dwed))or ln=='':
                dwed=True
                try:ln2=a.split('data-actualsrc="')[1].split('"')[0]
                except:ln2=''
                h=h.replace(ln,ln2)
                ln=ln2
            if(('src'in a)and(not dwed))or ln=='':
                dwed=True
                ln2=a.split('src="')[1].split('"')[0]
                h=h.replace(ln,ln2)
                ln=ln2
            if('.jpg'in a)and(not dwed):
                dwed=True
                ln2=a.split('.jpg')[0].split('https://')[-1:][0]
                ln='https://%s.jpg'%ln2
            if ln=='':
                continue
        try:d=r.get(ln).content
        except:
            if('你似乎来到了没有知识存在的荒原'in h)and('秒后自动跳转至知乎首页'in h):print(li);print('error');quit()
            print(ln)
            f=open('error.htm','w+');f.write(h.replace('.js',''));f.close();quit()
        f=open(p2:='%s/%s'%(p,ln.split('/')[-1:][0].split('?')[0]),'wb+');f.write(d);f.close()
        h=h.replace(ln,'.%s'%'/'.join(p2.split('/'.join(pa.split('/')[:-1]))[1:]).replace('//','/%s'%'.'.join(pa.split('/')[-1:][0].split('.')[:-1])))
        if('data-original'in a)and(not dwed):
            d=r.get(ln:=a.split('data-original="')[1].split('"')[0]).content
            f=open(p2:='%s/%s'%(p,ln.split('/')[-1:][0].split('?')[0]),'wb+');f.write(d);f.close()
            h=h.replace(ln,'.%s'%'/'.join(p2.split('/'.join(pa.split('/')[:-1]))[1:]).replace('//','/%s'%'.'.join(pa.split('/')[-1:][0].split('.')[:-1])))
        print(ln,p2)
    f=open(pa,'w+');f.write(h.replace('.js',''));f.close()
def di(li,pa):
    if not(pa[-4:]=='.htm'or pa[-5:]=='.html'):raise TypeError
    br.get(li)
    a=br.page_source
    np=0
    pl=[b.split('"')[0]for b in a.split('data-original="')[1:]]
    if'<em class="Thumbnail-Surplus-Sign">'in a:
        npx=br.find_elements(By.XPATH,'//*[@class="Thumbnail-Surplus-Sign"]')
        try:npx[len(npx)-1-np].click()
        except:br.execute_script("window.scrollBy(0, -128);");npx[len(npx)-1-np].click()
        while True:
            if'class="ImageGallery-arrow-right ImageGallery-arrow-disabled"'in br.page_source:break
            br.find_element(By.XPATH,'//*[@class="Zi Zi--ArrowRight"]').click()
            try:plz=br.page_source.split('class="ImageGallery-Img ImageGallery-fixed ImageGallery-CursorZoomIn"')[1].split('data-original="')[1].split('"')[0]
            except:
                time.sleep(2)
                plz=br.page_source.split('<div class="ImageGallery-Inner">')[1]
                plz=plz.split('data-original="')[1].split('"')[0]
            pl.append(plz)
        br.find_element(By.XPATH,'//*[@class="Zi Zi--Close"]').click()
        np+=1
    pl2=[]
    for b in pl:
        if b not in pl2:pl2.append(b)
    pl=pl2
    pn=0
    p3='%s/%s_Images'%('/'.join(pa.split('/')[:-1]),'.'.join(pa.split('/')[-1:][0].split('.')[:-1]))
    if not os.path.exists(p3):os.makedirs(p3)
    pl2=[]
    for b in pl:
        pn+=1
        d=r.get(b,stream=True,timeout=5)
        lp='%s/%s'%(p3,b.split('/')[-1:][0].split('?')[0])
        pl2.append(lp)
        f=open(lp,'wb+');f.write(d.content);f.close()
    h=br.page_source.replace('.js','')
    for b in pl2:
        h=h.replace(h.split(b.split('/')[-1:][0])[0].split('src="')[-1:][0].split('"')[0],'.%s'%b.split('/'.join(p3.split('/')[:-1]))[1])
    f=open(pa,'w+');f.write(h);f.close()
def dzv(li,pa):
    h=req(li).text
    pd='/'.join(pa.split('/')[:-1])
    if not os.path.exists(pd):os.makedirs(pd)
    p='%s/%s.mp4'%(pd,'.'.join(pa.split('/')[-1:][0].split('.')[:-1]))
    os.system('yt-dlp %s -o%s'%(li,p))
    f=open(pa,'w+');f.write(h.replace('.js',''));f.close()
for a in os.walk('indexs'):
    for b in a[2]:
        if b[-5:]=='.dict':
            op='%s/%s'%(a[0],b)
            tp=op.replace('indexs','indexs_htm').replace('.dict','.htm')
            if not os.path.exists(tp):
                f=open(op,'r');dc=eval(f.read());f.close()
                dp(dc['collection']['url'].replace('api','www').replace('collections','collection'),tp)
for a in os.walk('following_indexs'):
    for b in a[2]:
        if b[-5:]=='.dict':
            op='%s/%s'%(a[0],b)
            tp=op.replace('following_indexs','following_indexs_htm').replace('.dict','.htm')
            if not os.path.exists(tp):
                f=open(op,'r');dc=eval(f.read());f.close()
                dp(dc['collection']['url'].replace('api','www').replace('collections','collection'),tp)
def da(li,pa):
    if not(pa[-4:]=='.htm'or pa[-5:]=='.html'):raise TypeError
    br.get(li)
    cl=br.find_element(By.XPATH,'//*[@class="Button Modal-closeButton Button--plain"]')
    if cl:cl.click()
    br.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    h=br.page_source
    imgs=[a.split('>')[0]for a in h.split('<img')[1:]if'src'in a.split('>')[0]]
    if not os.path.exists(p:='%s/%s_Images'%('/'.join(pa.split('/')[:-1]),'.'.join(pa.split('/')[-1:][0].split('.')[:-1]))):os.makedirs(p)
    for a in imgs:
        dwed=False
        ln=a.split('src="')[1].split('"')[0]
        if not ln[:5]=='https':
            if'data-original'in a:
                dwed=True
                ln2=a.split('data-original="')[1].split('"')[0]
                h=h.replace(ln,ln2)
                ln=ln2
            elif'data-actualsrc'in a:
                dwed=True
                ln2=a.split('data-actualsrc="')[1].split('"')[0]
                h=h.replace(ln,ln2)
                ln=ln2
        try:d=r.get(ln).content
        except:
            if('你似乎来到了没有知识存在的荒原'in h)and('秒后自动跳转至知乎首页'in h):print(li);print('error');quit()
            continue
            #print(ln)
            #f=open('error.htm','w+');f.write(h.replace('.js',''));f.close();quit()
        f=open(p2:='%s/%s'%(p,ln.split('/')[-1:][0].split('?')[0]),'wb+');f.write(d);f.close()
        h=h.replace(ln,'.%s'%'/'.join(p2.split('/'.join(pa.split('/')[:-1]))[1:]).replace('//','/%s'%'.'.join(pa.split('/')[-1:][0].split('.')[:-1])))
        if('data-original'in a)and(not dwed):
            d=r.get(ln:=a.split('data-original="')[1].split('"')[0]).content
            f=open(p2:='%s/%s'%(p,ln.split('/')[-1:][0].split('?')[0]),'wb+');f.write(d);f.close()
            h=h.replace(ln,'.%s'%'/'.join(p2.split('/'.join(pa.split('/')[:-1]))[1:]).replace('//','/%s'%'.'.join(pa.split('/')[-1:][0].split('.')[:-1])))
        print(ln,p2)
    f=open(pa,'w+');f.write(h.replace('.js',''));f.close()
'''
def catch_comments(i,t):
    print(t,i)
    if t=='answer':
        return eval(r.get('https://www.zhihu.com/api/v4/answers/%s/comments'%i).text.replace('true','True').replace('false','False'))
    elif t=='article':
        return eval(r.get('https://www.zhihu.com/api/v4/articles/%s/comments'%i).text.replace('true','True').replace('false','False'))
    elif t=='pin':
        return eval(r.get('https://www.zhihu.com/api/v4/pins/%s/comments'%i).text.replace('true','True').replace('false','False'))
    elif t=='zvideo':
        return eval(r.get('https://www.zhihu.com/api/v4/zvideos/%s/comments'%i).text.replace('true','True').replace('false','False'))
    else:raise TypeError
'''
for a in os.walk('items'):
    for b in a[2]:
        op='%s/%s'%(a[0],b)
        tp=op.replace('items','downloads')[:-5]
        if not os.path.exists(tp):os.makedirs(tp)
        f=open(op,'r');tl=eval(f.read());f.close()
        '''
        tl2=[]
        tll=len(tl)
        for c in range(tll):
            if tl[tll-c-1] not in tl2:tl2.append(tl[tll-c-1])
        tl=tl2
        '''
        tll=len(tl)
        for c in range(tll):
            i=tl[c]
            '''
            rcc=True
            ed='%s/%s_comments.dict'%(tp,str(c+1).rjust(6).replace(' ','0'))
            if os.path.exists(ed):rcc=False
            if not os.path.exists(pp:='/'.join(ed.split('/')[:-1])):os.makedirs(pp)
            if rcc:
                print(i['data-zop']['type'],'comments cathcing...')
                co=catch_comments(str(i['data-zop']['itemId']),i['data-zop']['type'])
                print(ed)
                f=open(ed,'w+');f.write(repr(co));f.close()
            '''
            ed='%s/%s.htm'%(tp,str(c+1).rjust(6).replace(' ','0'))
            if os.path.exists(ed):continue
            print(i['data-zop']['type'],'identity catching...')
            if i['data-zop']['type']=='answer':
                dp('%s/answer/%s'%(i['link'],i['data-zop']['itemId']),ed)
            elif i['data-zop']['type']=='article':
                da('https://zhuanlan.zhihu.com/p/%s'%i['data-zop']['itemId'],ed)
            elif i['data-zop']['type']=='pin':
                di('https://www.zhihu.com/pin/%s'%i['data-zop']['itemId'],ed)
            else:
                dzv('https://www.zhihu.com/zvideo/%s'%i['data-zop']['itemId'],ed)
