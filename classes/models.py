from django.db import models 
from django.urls import reverse
from django.contrib.auth.models import User


class Classroom(models.Model):
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    year = models.IntegerField()
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="x")

    def get_absolute_url(self):
        return reverse('classroom-detail', kwargs={'classroom_id':self.id})

class Student(models.Model):
    name = models.CharField(max_length=120)
    date_of_birth = models.DateField(auto_now= False, auto_now_add=False)
    MALE = 'M'
    FEMALE = 'F'
    NOTAPPLICABLE = 'NA'
    GENDER = [
        (MALE, 'male'),
        (FEMALE, 'female'),
        (NOTAPPLICABLE, 'na'),
    ]
    gender = models.CharField(
        max_length=2,
        choices= GENDER,
        default="NA",)

    exame_grade = models.CharField(max_length=2)
    clasroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)