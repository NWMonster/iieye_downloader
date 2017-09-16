#!/usr/bin/env python
# NWMonster 16/9/2017

import urllib2
import sys, os

sk = 'kxnelimwzsb'
servers = ['http://comic.jmydm.com:8080/', 'http://zz.kucomic.com:2813/']

def decode(en_files):
    de_files = ''
    table_offset = ord(en_files[-1:]) - ord('a') + 1
    tmp = en_files[len(en_files) - table_offset - 12:len(en_files) - table_offset - 1]
    split = tmp[-1:]
    table = tmp[:-1]
    en_files = en_files[:len(en_files) - table_offset -12]
    for i in range(len(table)):
	en_files = en_files.replace(table[i], str(i))
    de_files_s = en_files.split(split)
    for i in range(len(de_files_s)):
	de_files += chr(int(de_files_s[i]))
    return de_files

def decode2(en_files, sk):
    de_files = ''
    split = sk[-1:]
    table = sk[:-1]
    for i in range(len(table)):
	en_files = en_files.replace(table[i], str(i))
    de_files_s = en_files.split(split)
    for i in range(len(de_files_s)):
	de_files += chr(int(de_files_s[i]))
    return de_files

def usage():
    print 'usage: ' + sys.argv[0] + 'download_path download_tool url'
    print 'download_tool 0: urllib2'
    print '              1: aria2'
    print '              2: wget'
    print '              3: curl'

if (len(sys.argv) != 4):
    usage()
    sys.exit(-1)

url = sys.argv[3]

page = urllib2.urlopen(url).read()
sFiles = page[page.find("var ")+12:page.find("\";var sPath")]
sPath = page[page.find("var sPath=\"")+11:page.find("\";</script>")]

if (url.find('jmydm') != -1):
    files = decode2(sFiles, sk).split('|')
    server_num = 0
elif (url.find('iibq') != -1):
    files = decode(sFiles).split('|')
    server_num = 0
elif (url.find('iieye') != -1):
    files = decode(sFiles).split('|')
    server_num = 1
else:
    print "wrong url!"
    sys.exit(-1)

comic_url = servers[server_num] + sPath
end = files[0][-4:]

download_path = sys.argv[1]
os.system('mkdir '+ download_path)
download_path = download_path + '/'

for i in range(len(files)):
    print 'progress: %02d%%' % (i*100/len(files))
    if (sys.argv[2] == '0'):
        req = urllib2.Request(comic_url + files[i])
        req.add_header('Referer', url)
        download_file = urllib2.urlopen(req).read()
        f = open(download_path + str(i) + end, "wb")
        f.write(download_file)
        continue
    if (sys.argv[2] == '1'):
        cmd_line = 'aria2c --referer=\"' + url + '\" ' + comic_url + files[i] + ' -q -o ' + download_path + str(i) + end
    elif (sys.argv[2] == '2'):
        cmd_line = 'wget --referer=\"' + url +'\" ' + comic_url + files[i] + ' -q -O ' + download_path + str(i) + end
    elif (sys.argv[2] == '3'):
        cmd_line = 'curl -e \"' + url + '\" ' + comic_url + files[i] + ' -s -o ' + download_path +str(i) + end
    os.system(cmd_line)


