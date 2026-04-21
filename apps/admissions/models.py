from django.db import models

# Create your models here.

class Student(models.Model):
    name=models.CharField(max_length=20,blank=False)
    mobile_no=models.CharField(max_length=10)
    email=models.EmailField()
    dob=models.DateField()
    gender_choice=[
        ('M','Male'),
        ('F','Female'),
        ('O','Others')
    ]
    gender=models.CharField(max_length=3,choices=gender_choice)
    address=models.TextField(max_length=1000)
    photo=models.ImageField(upload_to='photos/')
    documents=models.FileField(upload_to='documents/')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
