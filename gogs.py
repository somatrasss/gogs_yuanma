# -*- coding: utf-8 -*-
#Author: somatra
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

worksheet = xlrd.open_workbook(u'D:\\wwwork\\wwwwork\\gogs-yuanma\\w.xls')
sheet_names = worksheet.sheet_names()
for sheet_name in sheet_names:
	sheet1 = worksheet.sheet_by_name(sheet_name)
	cols0 = sheet1.col_values(0)
    
workbook = xlwt.Workbook(encoding='utf-8')
sheet2 = workbook.add_sheet("Sheet1")
sheet2.write(0,0,"仓库URL")
sheet2.write(0,1,"仓库项目URL")
sheet2.write(0,2,"仓库项目名称")
m=n=z=1

for x in range(len(cols0)):
    
    guanjianzi = '/explore/repos'
    url=url0=cols0[x]
    if '://' not in cols0[x]:
        url = 'http://' + cols0[x]
    url = url + guanjianzi
    try:
        r = requests.get(url,verify=False,timeout=5)
    except:
        print('目标无法访问')
    names = re.findall('<a class="name" href=".*">(.*)</a>',r.text)
    print('##################################################')
    print (url,'仓库项目数量：'+str(len(names)))
    sheet2.write(n,0,url)
    n = n+len(names)
    if len(names)==0:
        sheet2.write(m,1,'空')
        m=m+1
        n=n+1
        z=z+1
    else:
        for name in names:
            if '://' not in url0:
                url0 = 'http://' + url0
            url2 = url0 +'/'+ name.replace(" ", "")
            print (url2)
            sheet2.write(m,1,url2)
            
            m=m+1
            try:
                r2 = requests.get(url2,verify=False,timeout=5)
                emoji = re.findall('<span class="description has-emoji">(.*)</span>',r2.text)
                #print (z,name,emoji)
                sheet2.write(z,2,emoji)
                z=z+1
            except:
                    print('目标访问超时，可手动打开查看')
                    sheet2.write(z,2,'目标访问超时，可手动打开查看')
                    z=z+1
    
    #print (len(names))

workbook.save(r'test.xls')
