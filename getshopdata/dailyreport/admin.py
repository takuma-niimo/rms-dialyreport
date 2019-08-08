from django.contrib import admin
from dailyreport.models import ShopDailyReport
from dailyreport.models import testdata

class testdataAdmin(admin.ModelAdmin):
  intagerdata = (
    'data',
  )

admin.site.register(testdata, testdataAdmin)

class ShopDailyReportAdmin(admin.ModelAdmin):
  # list_display = ('id','pidata1', 'pidata2', 'pidata3', 'pidata4','pidata5',)
  dailydata = (
    'date',
    'dailysales'
    'dailysales_pc',
    'dailysales_sp',
    'monthlysales',
    'monthlysales_pc',
    'monthlysales_sp',
    'mratio_monthlysales',
    'yratio_monthlysales',
    'sales_lastmonth',
    'sales_lastyear',
    'pvuser_monthly',
    'pvuser_monthly_pc',
    'pvuser_monthly_sp',
    'mratio_pvuser',
    'yratio_pvuser',
    'pvuser_daily',
    'pvuser_daily_pc',
    'pvuser_daily_sp',
    'cvr_monthly',
    'cvr_monthly_pc',
    'cvr_monthly_sp',
    'mratio_cvr',
    'yratio_cvr',
    'cvr_daily',
    'cvr_daily_pc',
    'cvr_daily_sp',
    'acc_monthly',
    'acc_monthly_pc',
    'acc_monthly_sp',
    'mratio_acc',
    'yratio_acc',
    'acc_daily',
    'acc_daily_pc',
    'acc_daily_sp',
  )

admin.site.register(ShopDailyReport, ShopDailyReportAdmin)
