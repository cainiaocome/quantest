from urllib import request
from urllib import parse
from http import cookiejar
import ssl

#声明一个CookieJar对象实例来保存cookie
cookie = cookiejar.CookieJar()
#利用urllib库中的request的HTTPCookieProcessor对象来创建cookie处理器
handler=request.HTTPCookieProcessor(cookie)
#通过handler来构建opener
ssl._create_default_https_context = ssl._create_unverified_context
opener = request.build_opener(handler)
#此处的open方法同urllib的urlopen方法，也可以传入request
response = opener.open('http://www.qichacha.com')
cookieStr = ''
for item in cookie:
    cookieStr = cookieStr + item.name + '=' + item.value + ';'
    print (cookieStr)