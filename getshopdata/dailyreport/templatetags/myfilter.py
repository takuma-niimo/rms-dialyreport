from django import template

register = template.Library()

@register.filter(name='div')
def div(v, a):
  try:
    v = int(v)
    a = int(a)
    if a:
      return v / a
  except: pass
  return ''

@register.filter(name='mlt')
def mlt(v, a):
  try:
    v = int(v)
    a = int(a)
    return v * a
  except: pass
  return ''

@register.filter(name='percenet')
def percenet(v, a):
  try:
    if a:
      return v/a*100
  except: pass
  return ''
