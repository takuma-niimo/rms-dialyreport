from django.core.management.base import BaseCommand
from dailyreport.models import testdata

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

def adddata():
  testdata.objects.create(
    data = 1
  )

class Command(BaseCommand):
  def handle(self, *args, **options):
    adddata()
    print('done.')
