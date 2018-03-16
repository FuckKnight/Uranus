from django.db import models
from django.contrib.auth.models import User
import django.utils.timezone as timezone
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    code = models.CharField(max_length=16)
    port = models.TextField(blank = True)
    domain = models.TextField(blank = True)
    predic = models.DateField(default=timezone.now,editable=True)
    #nickName = models.CharField(max_length=20)


class Comment(models.Model):
    content = models.TextField(max_length=None)
    launchTime = models.DateField(auto_now=True)
    thumbUp = models.IntegerField(default=0)

    writer = models.ForeignKey(User,related_name='writer',on_delete = models.CASCADE)
    sub_comment = models.ForeignKey("self",on_delete = models.CASCADE)
    
    def __str__(self):
        return self.writer.name +" "+ str(self.launchTime)
