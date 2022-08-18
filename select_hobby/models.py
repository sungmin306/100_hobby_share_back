from django.db import models

# Create your models here.
class your_hobby(models.Model):
    your_MBTI = models.CharField(max_length=4,default='')
    hobby_category = models.CharField(max_length=100,default='')
    first_point = models.IntegerField(default='')
    second_point = models.IntegerField(default='')
    third_point = models.IntegerField(default='')
    return_hobby = models.CharField(max_length=20,default='')

    def __str__(self):
        return self.return_hobby