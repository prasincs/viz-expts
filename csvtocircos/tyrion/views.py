# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
# Create your views here.
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from circos.models import *
from circos.csvtocircos import *
import urllib
from django.utils import simplejson as json

from django import forms
process = None
csvToCircos = None

def handle_uploaded_file(title, f):
  global process, csvToCircos
  destination = open('uploads/data.csv', 'wb+')
  for chunk in f.chunks():
    destination.write(chunk)
  destination.close()
  csvToCircos = CsvToCircos("uploads/data.csv")
  csvToCircos.writeFiles()
  process = csvToCircos.runCircos("../static/images/circos.png")

  return csvToCircos.rowNames



class UploadCSVForm(forms.Form):
  title = forms.CharField(max_length=50)
  csv_file = forms.FileField()

def home(request):
  c = {}
  c.update(csrf(request))
  if request.method == 'POST':
    form = UploadCSVForm(request.POST, request.FILES)
    if form.is_valid():
      title = request.POST['title']
      #title = urllib.urlencode(request.POST['title'])
      rowNames = handle_uploaded_file(title,request.FILES['csv_file'])
      c = {'items': rowNames}
      return render_to_response('circos.html', c)
  else:
    form = UploadCSVForm()
  c['form'] = form
  return render_to_response('index.html', c)


def showGraph(request, title):
  return render_to_response('circos.html')

def proc(request):
  global process
  if (process!=None):
    process.poll()
    #print process.returncode
    print process.communicate()
    process = None
  return HttpResponse("complete")

@csrf_exempt
def updateGraph(request):
  global process,csvToCircos
  print request.raw_post_data
  if request.is_ajax():
    print "Ajax"
    if request.method == "POST":
      json_data = json.loads(request.raw_post_data)
      rows = json_data["items"]
    if csvToCircos == None:
      csvToCircos = CsvToCircos("uploads/data.csv")
      csvToCircos.openFile()
      csvToCircos.writeKaryotypesFile()
    
    csvToCircos.writeConfigFiles(rows)
    process = csvToCircos.runCircos("../static/images/circos.png")
      
  return HttpResponse(json.dumps({"test": "test"}), mimetype="application/javascript")
