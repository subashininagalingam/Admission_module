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
    address = models.TextField()

    guardian_name = models.CharField(max_length=100, blank=True, null=True)
    guardian_phone_no = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.First_name} {self.Last_name}"


class Course(models.Model):
    course = models.CharField(max_length=50)

    duration = models.CharField(max_length=20)
    course_fee = models.IntegerField()

    def __str__(self):
        return self.course


class Admission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='admissions')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    STATUS = [
        ('enquiry', 'Enquiry'),
        ('confirmed', 'Confirmed'),
        ('enrolled', 'Enrolled'),
        ('dropped', 'Dropped'),
    ]

    status = models.CharField(max_length=20, choices=STATUS, default='enquiry')

    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course}"


class Enrollment(models.Model):
    admission = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='enrollment')

    batch = models.CharField(max_length=10, choices=[
        ('Batch A','Batch A'),
        ('Batch B','Batch B'),
        ('Batch C','Batch C')
    ])

    start_date = models.DateField()

    payment_status = models.CharField(max_length=20, choices=[
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
        ('Partial','Partial')
    ])

    def __str__(self):
        return str(self.admission)