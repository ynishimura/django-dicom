from django.db import models

# Create your models here.

class Upload (models.Model):
	file_name = models.CharField(max_length = 100)
	upload_date = models.DateTimeField('date upload')
	def __unicode__(self):
	        return self.file_name
