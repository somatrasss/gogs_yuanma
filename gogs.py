# -*- coding: utf-8 -*-
#Author: somatra
#usage:python3 gogs.py
import urllib3
import argparse
import requests
import sys
import xlrd
import io
import re
import xlwt  # 用于写入xls
requests.packages.urllib3.disable_warnings()
#requests.get(url,verify=False)

worksheet = xlrd.open_workbook(u'C:\\Users\\Administrator\\Desktop\\12311\\11.xls') #文件xls必须是另存为xls文件
sheet_names = worksheet.sheet_names()
for sheet_name in sheet_names:
	sheet1 = worksheet.sheet_by_name(sheet_name)
	cols0 = sheet1.col_values(0)
    
workbook = xlwt.Workbook(encoding='utf-8')
sheet2 = workbook.add_sheet("Sheet1")
sheet2.write(0,0,"URL")
sheet2.write(0,1,"仓库项目URL")
sheet2.write(0,2,"仓库项目名称")
m=n=1

for x in range(len(cols0)):
    
    guanjianzi = '/explore/repos'
    url=url0=cols0[x]
    if '://' not in cols0[x]:
        url = 'http://' + cols0[x]
    url = url + guanjianzi
    print('##################################################')
    print (url)
    sheet2.write(n,0,url)
    try:
        r = requests.get(url,verify=False,timeout=5)
        names = re.findall('<a class="name" href=".*">(.*)</a>',r.text)
        n = n+len(names)
        print (len(names))
        if len(names)==0:
            m=m+1
            n=n+1
        else:
            for name in names:
                if '://' not in url0:
                    url0 = 'http://' + url0
                url2 = url0 +'/'+ name.replace(" ", "")
                r2 = requests.get(url2,verify=False,timeout=5)
                sheet2.write(m,1,url2)
                emoji = re.findall('<span class="description has-emoji">(.*)</span>',r2.text)
                print (name,emoji)
                sheet2.write(m,2,emoji)
                m=m+1
    except:
        print('无法访问')
        m=m+1
        n=n+1
    #print (len(names))

workbook.save(r'test.xls')
