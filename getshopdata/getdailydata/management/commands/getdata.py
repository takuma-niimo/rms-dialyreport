from django.core.management.base import BaseCommand
from dailyreport.models import NiiMoDailyReport

import sys
import re
import datetime
import json
import numpy as np
from dateutil.relativedelta import relativedelta
from prettyprinter import cpprint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

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
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(1)>div>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>span:nth-child(1)').text)
  rsales = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(1)>div>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>strong').text)
  shopdata['mratio_monthlysales'] = sign * rsales

  # Get the number of PV user
  pvuser = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-heading.heading-dotted.pa-tb-10>p>strong:nth-child(1)').text.replace(',', ''))
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>span:nth-child(1)').text)
  rpvuser = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>strong').text)
  shopdata['pvuser_monthly'] = pvuser
  shopdata['yratio_pvuser'] = sign * rpvuser
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>span:nth-child(1)').text)
  rpvuser = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(1)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>strong').text)
  shopdata['mratio_pvuser'] = sign * rpvuser

  # Get conversion ratio
  cvr = float(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-heading.heading-dotted.pa-tb-10>p>strong:nth-child(1)').text)
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>span:nth-child(1)').text)
  rcvr = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>strong').text)
  shopdata['cvr_monthly'] = cvr
  shopdata['yratio_cvr'] = sign * rcvr
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>span:nth-child(1)').text)
  rcvr = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(3)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>strong').text)
  shopdata['mratio_cvr'] = sign * rcvr

  # Get 客単価
  acc = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-heading.heading-dotted.pa-tb-10>p>strong:nth-child(1)').text.replace(',', ''))
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>span:nth-child(1)').text)
  racc = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-body.pa-tb-10>p:nth-child(2)>strong').text)
  shopdata['acc_monthly'] = acc
  shopdata['yratio_acc'] = sign * racc
  sign = rsign(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>span:nth-child(1)').text)
  racc = int(d.find_element_by_css_selector('#rmsTop-dashboard>div>section:nth-child(5)>div>div>div.rms-panel-body>div>div:nth-child(3)>div>div:nth-child(5)>div>div.rms-panel-body.pa-tb-10>p:nth-child(1)>strong').text)
  shopdata['mratio_acc'] = sign * racc

  return shopdata

def get_salesdata(d, s):
  # Get 先月売上: sales_lastmonth
  try:
    d.get('https://rdatatool.rms.rakuten.co.jp/rdreport/?app=sales_data')
    print('OK: https://rdatatool.rms.rakuten.co.jp/rdreport/?app=sales_data')
  except:
    print('NG: https://rdatatool.rms.rakuten.co.jp/rdreport/?app=sales_data')
  dt_lastmonth = s['date'] - relativedelta(months = 1)
  inputtxt = dt_lastmonth.strftime('%Y/%m')
  d.find_element_by_id('main-ym').clear()
  d.find_element_by_id('main-ym').send_keys(inputtxt)
  try:
    d.find_element_by_css_selector('body>table:nth-child(18)>tbody>tr>td>table>tbody>tr>td>input[type=submit]:nth-child(4)').click()
    print('OK: lastmonth submit')
  except:
    print('NG: lastmonth submit')
  s['sales_lastmonth'] = int(d.find_element_by_css_selector('body>table:nth-child(20)>tbody>tr>td>table>tbody>tr:last-child>td:nth-child(14)>font').text.replace(',', ''))
  # Get 前年売上(月): sales_lastyear
  dt_lastyear = s['date'] - relativedelta(years = 1)
  inputtxt = dt_lastyear.strftime('%Y/%m')
  d.find_element_by_id('main-ym').clear()
  d.find_element_by_id('main-ym').send_keys(inputtxt)
  try:
    d.find_element_by_css_selector('body>table:nth-child(18)>tbody>tr>td>table>tbody>tr>td>input[type=submit]:nth-child(4)').click()
    print('OK: lastyear submit')
  except:
    print('NG: lastyear submit')
  s['sales_lastyear'] = int(d.find_element_by_css_selector('body>table:nth-child(20)>tbody>tr>td>table>tbody>tr:last-child>td:nth-child(14)>font').text.replace(',', ''))

  return True

def get_pvuser_detail(d, s):
  try:
    d.get('https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=uu')
    print('OK: https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=uu')
  except:
    print('NG: https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=uu')
  data_tbody = d.find_elements_by_css_selector('tbody.js-report-data>tr')
  global strymd
  strymd = '{0:%Y/%m/%d}'.format(s['date'])
  global marray_pvuser
  marray_pvuser = np.zeros((31,2), dtype=int)
  for (tr, e) in zip(data_tbody, marray_pvuser):
    array = tr.text.split(' ')
    e[0] = int(array[3].replace(',', ''))
    e[1] = int(array[5].replace(',', ''))
    if strymd in tr.text:
      s['pvuser_daily'] = int(array[2].replace(',', ''))
      s['pvuser_daily_pc'] = int(array[3].replace(',', ''))
      s['pvuser_daily_sp'] = int(array[5].replace(',', ''))
      break
  # s['pvuser_monthly'] = np.sum(marray_pvuser)
  s['pvuser_monthly_pc'] = np.sum(marray_pvuser, axis=0)[0]
  s['pvuser_monthly_sp'] = np.sum(marray_pvuser, axis=0)[1]
  return True

def get_cvr_detail(d, s):
  try:
    d.get('https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=cvr')
    print('OK: https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=cvr')
  except:
    print('NG: https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=cvr')
  data_tbody = d.find_elements_by_css_selector('tbody.js-report-data>tr')
  marray_cvr = np.zeros((31,2), dtype=float)
  for (tr, e) in zip(data_tbody, marray_cvr):
    array = tr.text.split(' ')
    e[0] = float(array[3])
    e[1] = float(array[5])
    if strymd in tr.text:
      s['cvr_daily'] = float(array[2])
      s['cvr_daily_pc'] = float(array[3])
      s['cvr_daily_sp'] = float(array[5])
      break
  global buy_user
  buy_user = np.round(marray_cvr * marray_pvuser / 100).astype(int)
  # s['cvr_monthly'] = float(np.sum(buy_user) / s['pvuser_mtotal_total'] * 100)
  s['cvr_monthly_pc'] = float(np.sum(buy_user, axis=0)[0] / s['pvuser_monthly_pc'] * 100)
  s['cvr_monthly_sp'] = float(np.sum(buy_user, axis=0)[1] / s['pvuser_monthly_sp'] * 100)
  return True

def get_sales_detail(d, s):
  try:
    d.get('https://rdatatool.rms.rakuten.co.jp/datatool/?evt=sales')
    print('OK: https://rdatatool.rms.rakuten.co.jp/datatool/?evt=sales')
  except:
    print('NG: https://rdatatool.rms.rakuten.co.jp/datatool/?evt=sales')
  data_tbody = d.find_elements_by_css_selector('tbody.js-report-data>tr')
  marray_sales = np.zeros((31,2), dtype=int)
  for (tr, e) in zip(data_tbody, marray_sales):
    array = tr.text.split(' ')
    e[0] = int(array[3].replace(',', ''))
    e[1] = int(array[5].replace(',', ''))
    if strymd in tr.text:
      # s['dailysales'] = int(array[2].replace(',', ''))
      s['dailysales_pc'] = int(array[3].replace(',', ''))
      s['dailysales_sp'] = int(array[5].replace(',', ''))
      break
  # s['monthlysales'] = np.sum(marray_sales)
  s['monthlysales_pc'] = np.sum(marray_sales, axis=0)[0]
  s['monthlysales_sp'] = np.sum(marray_sales, axis=0)[1]
  return True

def get_acc_detail(d, s):
  try:
    d.get('https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=acc')
    print('OK: https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=acc')
  except:
    print('NG: https://rdatatool.rms.rakuten.co.jp/datatool/?evt=formula&act=acc')
  data_tbody = d.find_elements_by_css_selector('tbody.js-report-data>tr')
  marray_acc = np.zeros((31,2), dtype=int)
  for (tr, e) in zip(data_tbody, marray_acc):
    array = tr.text.split(' ')
    e[0] = int(array[3].replace(',', ''))
    e[1] = int(array[5].replace(',', ''))
    if strymd in tr.text:
      s['acc_daily'] = int(array[2].replace(',', ''))
      s['acc_daily_pc'] = int(array[3].replace(',', ''))
      s['acc_daily_sp'] = int(array[5].replace(',', ''))
      break
  # s['acc'] = int(round(s['monthlysales'] / np.sum(buy_user)))
  s['acc_monthly_pc'] = int(round(s['monthlysales_pc'] / np.sum(buy_user, axis=0)[0]))
  s['acc_monthly_sp'] = int(round(s['monthlysales_sp'] / np.sum(buy_user, axis=0)[1]))
  return True

def get_detail(d, s):
  get_pvuser_detail(d, s)
  get_cvr_detail(d, s)
  get_sales_detail(d, s)
  get_acc_detail(d, s)
  return True

def get_rms_detail(d, shopdata):
  get_salesdata(d, shopdata)
  get_detail(d, shopdata)
  return True

def login(d):
  d.implicitly_wait(3)
  d.set_page_load_timeout(10)

  for i in range(10):
    try:
      d.get('https://glogin.rms.rakuten.co.jp/?sp_id=1')
      print('OK: https://glogin.rms.rakuten.co.jp/?sp_id=1')
    except:
      print('NG: https://glogin.rms.rakuten.co.jp/?sp_id=1')

    d.find_element_by_tag_name('body').send_keys(Keys.F12)

    # Enter id1
    d.find_element_by_name('login_id').send_keys('horebore')
    _keys = 'horebore0' + str(i)
    d.find_element_by_name('passwd').send_keys(_keys)
    d.find_element_by_name('submit').click()

    try:
      # Enter id2
      d.find_element_by_name('user_id').send_keys('takuma.sato.niimo@gmail.com')
      d.find_element_by_name('user_passwd').send_keys('SBaq7TT7')
      print('{0}: success'.format(_keys))

    except:
      print('{0}: failed'.format(_keys))
      continue

    # Click 'notice' button
    d.find_element_by_name('submit').click()

    # Click RMS role
    d.find_element_by_name('submit').click()
    d.find_element_by_id('confirm').click()

    return d

  return False

def login(d):
  d.implicitly_wait(3)
  d.set_page_load_timeout(10)

  for i in range(10):
    try:
      d.get('https://glogin.rms.rakuten.co.jp/?sp_id=1')
    except:
      print('NG: https://glogin.rms.rakuten.co.jp/?sp_id=1')

    d.find_element_by_tag_name('body').send_keys(Keys.F12)

    # Enter id1
    d.find_element_by_name('login_id').send_keys('horebore')
    _keys = 'horebore0' + str(i)
    d.find_element_by_name('passwd').send_keys(_keys)
    d.find_element_by_name('submit').click()

    try:
      # Enter id2
      d.find_element_by_name('user_id').send_keys('takuma.sato.niimo@gmail.com')
      d.find_element_by_name('user_passwd').send_keys('SBaq7TT7')
      print('{0}: success'.format(_keys))

    except:
      print('{0}: failed'.format(_keys))
      continue

    # Click 'notice' button
    d.find_element_by_name('submit').click()

    # Click RMS role
    d.find_element_by_name('submit').click()
    d.find_element_by_id('confirm').click()

    return d

  return False

def printdata(d):
  print(d['date'])
  print('●店舗名: 新潟モノづくり NiiMo')
  print('●店舗URL: https://www.rakuten.co.jp/ep-naire/')
  print('●ニックネーム: たくま')
  print('●昨日売上: {0:,d}円\n　PC={1:,d}円\n　SP={2:,d}円'.format(d['dailysales'], d['dailysales_pc'], d['dailysales_sp']))
  print('●アクセス人数(月): {0:,d}人 ({1:+d}%)'.format(d['pvuser_monthly'], d['yratio_pvuser']))
  print('　PC: {0:,d}人\n　SP: {1:,d}人'.format(d['pvuser_monthly_pc'], d['pvuser_monthly_sp']))
  print('●アクセス人数(日): {0:,d}人'.format(d['pvuser_daily']))
  print('　PC: {0:,d}人\n　SP: {1:,d}人'.format(d['pvuser_daily_pc'], d['pvuser_daily_sp']))
  print('●転換率(月): {0:.2f}% ({1:+d}%)'.format(d['cvr_monthly'], d['yratio_cvr']))
  print('　PC: {0:.2f}%\n　SP: {1:.2f}%'.format(d['cvr_monthly_pc'], d['cvr_monthly_sp']))
  print('●転換率(日): {0:.2f}%'.format(d['cvr_daily']))
  print('　PC: {0:.2f}%\n　SP: {1:.2f}%'.format(d['cvr_daily_pc'], d['cvr_daily_sp']))
  print('●客単価(月): {0:,d}円 ({1:+d}%)'.format(d['acc_monthly'], d['yratio_acc']))
  print('　PC: {0:,d}円\n　SP: {1:,d}円'.format(d['acc_monthly_pc'], d['acc_monthly_sp']))
  print('●客単価(日): {0:,d}円'.format(d['acc_daily']))
  print('　PC: {0:,d}円\n　SP: {1:,d}円'.format(d['acc_daily_pc'], d['acc_daily_sp']))
  print('●今月累計売上: {0:,d}円 ({1:+d}%)'.format(d['monthlysales'], d['yratio_monthlysales']))
  print('●目標金額(昨年2倍): 6,000,000円'.format(d['monthlysales']))
  print('●目標達成率: {0:.1f}%'.format(d['monthlysales']/6000000*100))
  print('【楽天市場運営時間】(受注・発送作業のぞく):')
  print('【昨日やったこと】')
  print('【今日やること、やったこと】')
  print('【コメント】')

def adddata(d):
  if NiiMoDailyReport.objects.all().filter(date=d['date']):
    return False
  else:
    report = NiiMoDailyReport.objects.create(
        date = d['date'],
        dailysales = d['dailysales'],
        dailysales_pc = d['dailysales_pc'],
        dailysales_sp = d['dailysales_sp'],
        monthlysales = d['monthlysales'],
        monthlysales_pc = d['monthlysales_pc'],
        monthlysales_sp = d['monthlysales_sp'],
        mratio_monthlysales = d['mratio_monthlysales'],
        yratio_monthlysales = d['yratio_monthlysales'],
        sales_lastmonth = d['sales_lastmonth'],
        sales_lastyear = d['sales_lastyear'],
        pvuser_monthly = d['pvuser_monthly'],
        pvuser_monthly_pc = d['pvuser_monthly_pc'],
        pvuser_monthly_sp = d['pvuser_monthly_sp'],
        mratio_pvuser = d['mratio_pvuser'],
        yratio_pvuser = d['yratio_pvuser'],
        pvuser_daily = d['pvuser_daily'],
        pvuser_daily_pc = d['pvuser_daily_pc'],
        pvuser_daily_sp = d['pvuser_daily_sp'],
        cvr_monthly = d['cvr_monthly'],
        cvr_monthly_pc = d['cvr_monthly_pc'],
        cvr_monthly_sp = d['cvr_monthly_sp'],
        mratio_cvr = d['mratio_cvr'],
        yratio_cvr = d['yratio_cvr'],
        cvr_daily = d['cvr_daily'],
        cvr_daily_pc = d['cvr_daily_pc'],
        cvr_daily_sp = d['cvr_daily_sp'],
        acc_monthly = d['acc_monthly'],
        acc_monthly_pc = d['acc_monthly_pc'],
        acc_monthly_sp = d['acc_monthly_sp'],
        mratio_acc = d['mratio_acc'],
        yratio_acc = d['yratio_acc'],
        acc_daily = d['acc_daily'],
        acc_daily_pc = d['acc_daily_pc'],
        acc_daily_sp = d['acc_daily_sp']
    )

class Command(BaseCommand):
  def handle(self, *args, **options):
    # Headless Chrome
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=options)
    try:
      browser = login(browser)
      if browser == False:
        print('Error: failed to login to RMS')
        browser.quit()
        sys.exit(1)
      data = get_rmstop(browser)
      get_rms_detail(browser, data)
      printdata(data)
      cpprint(data)
      if adddata(data) == False:
        print('data {0} is already exists.'.format(data['date']))
        sys.exit(1)
      browser.quit()
    except:
      browser.quit()
      import traceback
      print('error.')
      traceback.print_exc()
      sys.exit(1)
