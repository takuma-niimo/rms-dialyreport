from django.core.management.base import BaseCommand

import sys
import re
import datetime
import json
from prettyprinter import cpprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
# import pdb; pdb.set_trace()

def rsign(s):
  if re.match(r'[＋+]', s):
    return 1
  else:
    return -1

def get_rmstop(d):
  shopdata = {}

  # Get date
  year = datetime.date.today().year
  date = d.find_element_by_css_selector('#mm_gg005_more001 h2').text.split('日')[0]
  date_md = list(map(int, date.split('月')))
  if date_md[0] == 1 and date_md[1] == 1:
    year -= 1
  shopdata['date'] = datetime.date(year, date_md[0], date_md[1])

  # Get daily sales
  sales_d = int(d.find_element_by_css_selector('#mm_gg005_more001 strong.txt-size-42').text.replace(',', ''))
  shopdata['dailysales'] = sales_d

  # Get monthly sales
  sales_m = int(d.find_element_by_css_selector('#mm_gg006_more strong.txt-size-42').text.replace(',', ''))
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(1)>div>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>span:nth-child(1)').text)
  rsales = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(1)>div>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>strong').text)
  shopdata['monthlysales'] = sales_m
  shopdata['yratio_monthlysales'] = sign * rsales
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(1)>div>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>span.txt-size-20').text)
  rsales = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(1)>div>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>strong').text)
  shopdata['mratio_montylysales'] = sign * rsales

  # Get the number of PV user
  pvuser = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-heading.heading-dotted.pa-tb-10>p>strong:nth-child(1)').text.replace(',', ''))
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>span.txt-size-20').text)
  rpvuser = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>strong').text)
  shopdata['pvuser'] = pvuser
  shopdata['yratio_pvuser'] = sign * rpvuser
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>span.txt-size-20.maintxt-1').text)
  rpvuser = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>strong').text)
  shopdata['mratio_pvuser'] = sign * rpvuser

  # Get conversion ratio
  cvr = float(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-heading.heading-dotted.pa-tb-10>p>strong:nth-child(1)').text)
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>span.txt-size-20').text)
  rcvr = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>strong').text)
  shopdata['cvr'] = cvr
  shopdata['yratio_cvr'] = sign * rcvr
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>span.txt-size-20').text)
  rcvr = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>strong').text)
  shopdata['mratio_cvr'] = sign * rcvr

  # Get 客単価
  adt = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-heading.heading-dotted.pa-tb-10>p>strong:nth-child(1)').text.replace(',', ''))
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>span.txt-size-20').text)
  radt = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>strong').text)
  shopdata['adt'] = adt
  shopdata['yratio_adt'] = sign * radt
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>span.txt-size-20').text)
  radt = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>strong').text)
  shopdata['mratio_adt'] = sign * radt

  return shopdata

def login(d):
  d.implicitly_wait(0.5)

  for i in range(10):
    print('i=', i)
    d.get('https://glogin.rms.rakuten.co.jp/?sp_id=1')
    d.find_element_by_tag_name('body').send_keys(Keys.F12)

    # Enter id1
    d.find_element_by_name('login_id').send_keys('horebore')
    _keys = 'horebore0' + str(i)
    d.find_element_by_name('passwd').send_keys(_keys)
    d.find_element_by_name('submit').click()
    print('trying: pass={0}'.format(_keys))

    try:
      # Enter id2
      d.find_element_by_name('user_id').send_keys('takuma.sato.niimo@gmail.com')
      d.find_element_by_name('user_passwd').send_keys('SBaq7TT7')
      print('  success.')

    except:
      print('  failed.')
      continue

    # Click 'notice' button
    d.find_element_by_name('submit').click()

    # Click RMS role
    d.find_element_by_name('submit').click()
    d.find_element_by_id('confirm').click()

    return d

  return False

def printdata(d):
  print('・店舗名: 新潟モノづくり NiiMo')
  print('・店舗URL: https://www.rakuten.co.jp/ep-naire/')
  print('・ニックネーム: たくま')
  print('・昨日売上: {0:,d}'.format(d['dailysales']))
  print('・アクセス人数: {0:,d}人 ({1:+d}%)'.format(d['pvuser'], d['yratio_pvuser']))
  print('・転換率: {0:.1f}% ({1:+d}%)'.format(d['cvr'], d['yratio_cvr']))
  print('・客単価: {0:,d}円 ({1:+d}%)'.format(d['adt'], d['yratio_adt']))
  print('・今月累計売上: {0:,d}円 ({1:+d}%)'.format(d['monthlysales'], d['yratio_monthlysales']))
  print('・目標金額(昨年2倍): 6,000,000円'.format(d['monthlysales']))
  print('・目標達成率: {0:.1f}%'.format(d['monthlysales']/6000000*100))
  print('【楽天市場運営時間】(受注・発送作業のぞく):')
  print('【昨日やったこと】')
  print('【今日やること、やったこと】')
  print('【コメント】')

# Headless Chrome
options = Options()
options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=options)
browser = login(browser)
if browser == False:
  print('Error: failed to login to RMS')
  sys.exit(1)
data = get_rmstop(browser)
cpprint(data)


