from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

# from apps.admissions.models import (
#     Course,
#     Enrollment
# )

from django.db import models
from django.utils import timezone


class Trainer(models.Model):

    trainer_name = models.CharField(max_length=100)

    specialization = models.CharField(max_length=100)

    phone_no = models.CharField(
        max_length=10,
        unique=True
    )

    email = models.EmailField(unique=True)

    joined_date = models.DateField(
        default=timezone.now
    )

    def __str__(self):
        return self.trainer_name


class Batch(models.Model):

    batch_choices = [
        ('Batch A', 'Batch A'),
        ('Batch B', 'Batch B'),
        ('Batch C', 'Batch C')
    ]

    timing_choices = [
        ('Morning', 'Morning'),
        ('Afternoon', 'Afternoon'),
        ('Evening', 'Evening')
    ]

    batch_name = models.CharField(
        max_length=50,choices=batch_choices
    )

    timing = models.CharField(
        max_length=100,
        choices=timing_choices
    )

    start_time = models.TimeField(
    null=True,
    blank=True
    )

    end_time = models.TimeField(
    null=True,
    blank=True
    )

    course = models.ForeignKey(
        'admissions.Course',
        on_delete=models.CASCADE,
        related_name='batches'
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='batches'
    )

    student_count = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.batch_name
    
class Attendance(models.Model):

    class AttendanceStatus(models.TextChoices):

        PRESENT = 'Present', 'Present'
        ABSENT = 'Absent', 'Absent'
        LATE = 'Late', 'Late'

    enrollment = models.ForeignKey(
        'admissions.Enrollment',
        on_delete=models.CASCADE
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE
    )

    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )


    status = models.CharField(
        max_length=10,
        choices=AttendanceStatus.choices
    )

    attendance_date = models.DateField(default=timezone.now) 

    timestamp = models.DateTimeField(
        auto_now_add=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['enrollment', 'batch', 'attendance_date'],
                name='unique_attendance'
            )
        ]

    def __str__(self):

        return (
            f"{self.enrollment.student}"
            f"- {self.attendance_date}"
            f" - {self.status}"
        )
    


class SyllabusLog(models.Model):

    batch = models.ForeignKey(
        'Batch',
        on_delete=models.CASCADE,
        related_name='syllabus_logs'
    )

    trainer = models.ForeignKey(
        'Trainer',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='syllabus_logs'
    )

    date = models.DateField(
        default=timezone.now
    )

    topic_covered = models.CharField(max_length=255)

    duration = models.PositiveIntegerField(
        help_text="Duration in minutes"
    )

    next_topic = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    trainer_notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date', '-created_at']

    def clean(self):
        if self.duration <= 0:
            raise ValidationError("Duration must be greater than 0")

    def save(self, *args, **kwargs):
        # auto-assign trainer from batch if not given
        if not self.trainer and self.batch and self.batch.trainer:
            self.trainer = self.batch.trainer

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.batch.batch_name} | {self.topic_covered} | {self.date}"