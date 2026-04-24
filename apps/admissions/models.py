from django.db import models

class Student(models.Model):
    First_name = models.CharField(max_length=20, blank=True, null=True)
    Last_name = models.CharField(max_length=20, blank=True, null=True)
    dob = models.DateField()
    phone_no = models.CharField(max_length=10, blank=True, null=True)

    gender_choice = [
        ('M','Male'),
        ('F','Female'),
        ('O','Others')
    ]
    gender = models.CharField(max_length=3, choices=gender_choice)

    email = models.EmailField()
    address = models.TextField(max_length=1000)

    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone_no = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.First_name} {self.Last_name}"


class Course(models.Model):
    course_choice = [
        ('Python Fullstack','Python Fullstack'),
        ('Java Fullstack','Java Fullstack'),
        ('Python','Python'),
        ('Java','Java'),
        ('AWS','AWS')
    ]
    course = models.CharField(max_length=20, choices=course_choice)
    duration_choice=[
        ('3 Months','3 Months'),
        ('6 Months','6 Months'),
        ('1 Year','1 Year')
    ]
    duration=models.CharField(max_length=10,choices=duration_choice)
    course_fee=models.IntegerField()
    status_choice = [
        ('enquiry', 'Enquiry'),
        ('confirmed', 'Confirmed'),
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
    ]
    status = models.CharField(max_length=20, choices=status_choice)

    def __str__(self):
        return self.course


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    batch_choice=[
        ('Batch - A','Batch - A'),
        ('Batch - B','Batch - B'),
        ('Batch - C','Batch - C')
    ]
    batch=models.CharField(max_length=10,choices=batch_choice)    
    start_date = models.DateField()

    payment_status = models.CharField(max_length=20, choices=[
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Partial','Partial')
    ])

    def __str__(self):
        return f"{self.student} - {self.course}"