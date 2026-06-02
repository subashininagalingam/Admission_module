from django.contrib import admin

from .models import (
    Trainer,
    Batch,
    Attendance
)


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):

    list_display = (
        'trainer_name',
        'specialization',
        'phone_no',
        'email'
    )


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):

    list_display = (
        'batch_name',
        'course',
        'trainer',
        'student_count'
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'enrollment',
        'batch',
        'status',
        'timestamp'
    )

    list_filter = (
        'batch',
        'status'
    )

    search_fields = (
        'enrollment__admission__student__student_name',
    )