from apps.admissions.models import Enrollment
from rest_framework import serializers
from django.utils import timezone
from .models import (
    SyllabusLog,
    Trainer,
    Batch,
    Attendance
)


class TrainerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Trainer
        fields = '__all__'


class BatchSerializer(serializers.ModelSerializer):

    trainer_name = serializers.SerializerMethodField()
    is_marked = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    course_name = serializers.CharField(
        source='course.course_name',
        read_only=True
    )

    class Meta:
        model = Batch
        fields = [
            'id',
            'batch_name',
            'course',
            'course_name',
            'timing',
            'start_time',
            'end_time',
            'student_count',
            'trainer',
            'trainer_name',
            'is_marked',
            'start_date',
            'end_date',
        ]

    def validate(self, data):
        trainer = data.get('trainer')
        timing = data.get('timing')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        today = timezone.now().date()

        if start_date <= today:
            raise serializers.ValidationError({
            "start_date": "Start date must be a future date."
        })

        if end_date <= today:
            raise serializers.ValidationError({
            "end_date": "End date must be a future date."
        })

        if end_date < start_date:
            raise serializers.ValidationError({
            "end_date": "End date cannot be before start date."
        })

        # Trainer overlap validation
        if trainer and start_date and end_date:
            overlapping_batches = Batch.objects.filter(
            trainer=trainer,
            timing=timing,
            start_date__lte=end_date,
            end_date__gte=start_date
        )

        # Update time exclude current batch
            if self.instance:
                overlapping_batches = overlapping_batches.exclude(
                pk=self.instance.pk
            )

            if overlapping_batches.exists():
                raise serializers.ValidationError({
                "trainer": [
                    "Trainer already assigned to another batch during this period."
                ]
            })

        return data

    def get_student_count(self, obj):

        return obj.student_count

    def get_trainer_name(self, obj):

        return obj.trainer.trainer_name if obj.trainer else None

    def get_is_marked(self, obj):

        return Attendance.objects.filter(
            batch=obj,
            attendance_date=timezone.now().date()
        ).exists()
    



class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = '__all__'

class SyllabusLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = SyllabusLog
        fields = "__all__"