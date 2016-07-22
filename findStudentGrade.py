#coding=utf-8

import urllib
import urllib2
import cookielib
import re
import os
import getpass
def getName(loginPage):         # get the name
               Sname = r'<span id="xhxm">(.+)同学</span>'
               Sname = re.compile(Sname)
               try:
                    return Sname.findall(loginPage)[0]
               except IndexError, e:
                    raise e
                    print "User-name or password error, try again!"
                    main()
def getVIEW(page):
        view=r'name="__VIEWSTATE" value="(.+)" '
        view=re.compile(view)
        return view.findall(page)[0]
def Print(grade):
    string=r"<td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.?)</td><td>(.*)</td><td>(.*)</td><td>(.*)</td><td>(.?)</td><td>(.?)</td>"
    string=re.compile(string)
    result={}
    subject=[]
    a=string.findall(grade)
    #print a
    for i in a:
        for j in range(15):
            subject.append(i[j])
        result[subject[3]]=subject
        subject=[]
    for i in result.keys():
        j=result[i]
        print '%-10s%-2s%-10s%-8s%6s%8s%10s%6s%6s%5s%10s%-10s%-15s%s%s' % tuple(j)
        print " "

def main():
    loginUrl='http://222.24.62.120/default4.aspx'
    getinfoUrl="http://222.24.62.120/xs_main.aspx?xh="
    Id=raw_input("Please input your id:")
    Password=getpass.getpass("Please input password:")
    print 'Loading.......'
    #page=urllib2.urlopen(loginUrl).read()
    RadioButtonList1=u"学生".encode('gb2312','replace')
    Button1=u" 登 录 ".encode('gb2312','replace')
    postdata=urllib.urlencode({
                    '__VIEWSTATE':'dDwxMTE4MjQwNDc1Ozs+YofaNxf5dpXqcC3ZAqYdKfPCdbw=',
                    'TextBox1':Id,
                    'TextBox2':Password,
                    'RadioButtonList1':RadioButtonList1,
                    'Button1':Button1})
    Headers={'Host': '222.24.62.120',
             'Connection': 'keep-alive',
             'Content-Length': '156',
             'Cache-Control': 'max-age=0',
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
             'Origin': 'http://222.24.62.120',
             'Upgrade-Insecure-Requests': '1',
             'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36',
             'Content-Type': 'application/x-www-form-urlencoded',
             'Referer': 'http://222.24.62.120/default4.aspx',
             'Accept-Encoding': 'gzip, deflate',
             'Accept-Language': 'zh-CN,zh;q=0.8'}

    filename='cookie.txt'
    cookie=cookielib.MozillaCookieJar(filename)
    #httpHandler=urllib2.HTTPHandler(debuglevel=1)
    opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    request=urllib2.Request(loginUrl,postdata,Headers)
    Page=opener.open(request).read()
    cookie.save()

    getinfoUrl=getinfoUrl+Id
    #print getinfoUrl
    myrequest=urllib2.Request(getinfoUrl)
    loginPage=opener.open(myrequest).read()
    lpage=unicode(loginPage, 'gb2312','ignore').encode("utf-8") 
    #print lpage
    try:
            name=getName(lpage)
    except IndexError, e:
        print "username or password error, try again!"
        main()
        exit()
    else:
        pass

    getdata=urllib.urlencode({
            'xh':Id,
            'xm':name,
            'gnmkdm':'N121605'
        })
    head={  'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, sdch',   
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Host':'222.24.62.120',
            'Referer':'http://222.24.62.120/xs_main.aspx?xh='+Id,
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36'
            
            }
    getGradePage=urllib2.Request('http://222.24.62.120/xscjcx.aspx?'+getdata,None,head)
    getpage=unicode(opener.open(getGradePage).read(),'gb2312','ignore').encode("utf-8")
    data=urllib.urlencode({
        "__VIEWSTATE":getVIEW(getpage),
        "btn_zcj":"历年成绩"
        })
    request=urllib2.Request('http://222.24.62.120/xscjcx.aspx?'+getdata,data,head)
    html=opener.open(request)
    result=unicode(html.read(),'gb2312','ignore').encode("utf-8")
    #print result
    Print(result)
if __name__ =='__main__':
    main()




