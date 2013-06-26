from yujisite.file_uploader.models import Upload
from django.http import HttpResponse,HttpResponse,HttpResponseRedirect
from django.template import Context,loader
from django.shortcuts import render_to_response,get_object_or_404
from django.forms import *
from django.utils import timezone 
import os
import os.path
from django.shortcuts import get_object_or_404, render_to_response


def index(request):
	msg=''
	FILENAME=''
	name=''
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
			FILENAME = form.cleaned_data['name']
			name , ext = os.path.splitext(FILENAME)
	else:
		form = UploadFileForm()

	####dcm_convert######	
	#cmd1 = "dcmdjpeg /root/gitbreak/Django-file-upload/yujisite/yujisite/upload_dir/" + name + ".dcm /root/gitbreak/Django-file-upload/yujisite/yujisite/upload_dir/" + name + ".dcm"
	#os.system(cmd1)

	#cmd2 = "dcm2pnm --write-png /root/gitbreak/Django-file-upload/yujisite/yujisite/upload_dir/" + name + ".dcm /root/gitbreak/Django-file-upload/yujisite/yujisite/upload_dir/" + name + ".png"
	#cmd = "source /root/gitbreak/Django-file-upload/yujisite/convert.sh  " + name
	#os.system(cmd2)

	#cmd3 = "scp /root/gitbreak/Django-file-upload/yujisite/yujisite/upload_dir/" + name + ".dcm /root/gitbreak/Django-file-upload/yujisite/yujisite/upload_dir/" + name + ".png root@172.22.55.121:/var/www/files/"
	#os.system(cmd3)
	
	######################

	latest_upload_list = Upload.objects.all().order_by('-upload_date')[:5]
	t = loader.get_template('file_uploader/index.html')
	c = Context({'latest':latest_upload_list,})
	c['form'] = form
	c['msg'] = msg
	return HttpResponse(t.render(c))

class UploadFileForm(Form):
	name = CharField(max_length = 50)
	file = FileField()
def hadoop(request):
	msg=''
	if request.method == 'POST':
		#Hadoop_link#
		cmd = "ssh 172.22.55.135 ./hadoop.sh >> outputs"
		#cmd = "ssh 192.168.24.62 ./hadoop.sh >> outputs"
		os.system(cmd)

		#jumpurl = '172.22.55.135:50030'
		msg = 'finished!'
	t = loader.get_template('file_uploader/hadoop.html')
	return render_to_response('file_uploader/hadoop.html', {'msg':msg},)
			#return HttpResponseRedirect('/uploader/')
	#return HttpResponse(t.render(RequestContext(request,{'msg':msg})))
