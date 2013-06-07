from yujisite.file_uploader.models import Upload
from django.http import HttpResponse,HttpResponse
from django.template import Context,loader
from django.shortcuts import render_to_response,get_object_or_404
from django.forms import *
from django.utils import timezone 
import os

def index(request):
	msg=''
	if request.method == 'POST':
		form = UploadFileForm(request.POST,request.FILES)
		if form.is_valid():
			updir = r'/root/gitbreak/Django-file-upload/yujisite/yujisite/upload_dir/'+ form.cleaned_data['name']
			destination = open(updir, 'wb+')
			upfile = request.FILES['file']
			for chunk in upfile.chunks():
				destination.write(chunk)
			destination.close()
			
			#database#
			u = Upload(file_name=form.cleaned_data['name'],upload_date=timezone.now())
			u.save()
			msg = 'Uploaded!'
			
			#Hadoop#
			cmd = "ssh hadoop ./hadoop.sh >> aaa"
			os.system(cmd)
	else:
		form = UploadFileForm()
	
	latest_upload_list = Upload.objects.all().order_by('-upload_date')[:2]
	t = loader.get_template('file_uploader/index.html')
	c = Context({'latest':latest_upload_list,})
	c['form'] = form
	c['msg'] = msg
	return HttpResponse(t.render(c))

class UploadFileForm(Form):
	name = CharField(max_length = 50)
	file = FileField()

