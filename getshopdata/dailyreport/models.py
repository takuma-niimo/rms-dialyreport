from django.db import models
import datetime

class testdata(models.Model):
  class Meta:
    verbose_name = 'test-data'

  data = models.IntegerField(
    verbose_name = 'test',
    blank = True, null = True, default = 0)

class NiiMoDailyReport(models.Model):
  class Meta:
    verbose_name = 'NiiMo Daily Report'

  date = models.DateField(
    primary_key = True,
    verbose_name = '日付',
    default = datetime.date.today,
    blank = False, null = False)

  dailysales = models.IntegerField(
    verbose_name = '売上',
    blank = True, null = True, default = 0)

  dailysales_pc = models.IntegerField(
    verbose_name = 'PC売上',
    blank = True, null = True, default = 0)

  dailysales_sp = models.IntegerField(
    verbose_name = 'SP売上',
    blank = True, null = True, default = 0)

  monthlysales = models.IntegerField(
    verbose_name = '月累計売上',
    blank = True, null = True, default = 0)

  monthlysales_pc = models.IntegerField(
    verbose_name = 'PC月累計売上',
    blank = True, null = True, default = 0)

  monthlysales_sp = models.IntegerField(
    verbose_name = 'SP月累計売上',
    blank = True, null = True, default = 0)

  mratio_monthlysales = models.FloatField(
    verbose_name = '月累計売上前月比',
    blank = True, null = True, default = 0)

  yratio_monthlysales = models.FloatField(
    verbose_name = '月累計売上前年比',
    blank = True, null = True, default = 0)

  sales_lastmonth = models.IntegerField(
    verbose_name = '前月売上',
    blank = True, null = True, default = 0)

  sales_lastyear = models.IntegerField(
    verbose_name = '前年売上(月)',
    blank = True, null = True, default = 0)

  pvuser_monthly = models.IntegerField(
    verbose_name = 'アクセス人数(月)',
    blank = True, null = True, default = 0)

  pvuser_monthly_pc = models.IntegerField(
    verbose_name = 'PCアクセス人数(月)',
    blank = True, null = True, default = 0)

  pvuser_monthly_sp = models.IntegerField(
    verbose_name = 'SPアクセス人数(月)',
    blank = True, null = True, default = 0)

  mratio_pvuser = models.FloatField(
    verbose_name = 'アクセス人数前月比',
    blank = True, null = True, default = 0)

  yratio_pvuser = models.FloatField(
    verbose_name = 'アクセス人数前年比',
    blank = True, null = True, default = 0)

  pvuser_daily = models.IntegerField(
    verbose_name = 'アクセス人数(日)',
    blank = True, null = True, default = 0)

  pvuser_daily_pc = models.IntegerField(
    verbose_name = 'PCアクセス人数(日)',
    blank = True, null = True, default = 0)

  pvuser_daily_sp = models.IntegerField(
    verbose_name = 'SPアクセス人数(日)',
    blank = True, null = True, default = 0)

  cvr_monthly = models.FloatField(
    verbose_name = '転換率(月)',
    blank = True, null = True, default = 0)

  cvr_monthly_pc = models.FloatField(
    verbose_name = 'PC転換率(月)',
    blank = True, null = True, default = 0)

  cvr_monthly_sp = models.FloatField(
    verbose_name = 'SP転換率(月)',
    blank = True, null = True, default = 0)

  mratio_cvr = models.FloatField(
    verbose_name = '転換率前月比',
    blank = True, null = True, default = 0)

  yratio_cvr = models.FloatField(
    verbose_name = '転換率前年比',
    blank = True, null = True, default = 0)

  cvr_daily = models.FloatField(
    verbose_name = '転換率(日)',
    blank = True, null = True, default = 0)

  cvr_daily_pc = models.FloatField(
    verbose_name = 'PC転換率(日)',
    blank = True, null = True, default = 0)

  cvr_daily_sp = models.FloatField(
    verbose_name = 'SP転換率(日)',
    blank = True, null = True, default = 0)

  acc_monthly = models.IntegerField(
    verbose_name = '客単価(月)',
    blank = True, null = True, default = 0)

  acc_monthly_pc = models.IntegerField(
    verbose_name = 'PC客単価(月)',
    blank = True, null = True, default = 0)

  acc_monthly_sp = models.IntegerField(
    verbose_name = 'SP客単価(月)',
    blank = True, null = True, default = 0)

  mratio_acc = models.FloatField(
    verbose_name = '客単価前月比',
    blank = True, null = True, default = 0)

  yratio_acc = models.FloatField(
    verbose_name = '客単価前年比',
    blank = True, null = True, default = 0)

  acc_daily = models.IntegerField(
    verbose_name = '客単価(日)',
    blank = True, null = True, default = 0)

  acc_daily_pc = models.IntegerField(
    verbose_name = 'PC客単価(日)',
    blank = True, null = True, default = 0)

  acc_daily_sp = models.IntegerField(
    verbose_name = 'SP客単価(日)',
    blank = True, null = True, default = 0)
