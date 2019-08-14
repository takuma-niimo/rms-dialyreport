from django.shortcuts import render
from dailyreport.models import ShopDailyReport

def apptop(request):
  shopdata = ShopDailyReport.objects.all()
  return render(
    request,
    'dailyreport/ShopDailyReport.html',
    {'shopdata': shopdata}
  )

def report(request):
  year =  int(request.GET.get('y'))
  month = int(request.GET.get('m'))
  day =   int(request.GET.get('d'))
  one_day = '{0}-{1:02d}-{2}'.format(year,month,day)
  data_one_day = ShopDailyReport.objects.get(pk=one_day)
  return render(
      request,
      'dailyreport/report.html',
      {'d': data_one_day}
  )
