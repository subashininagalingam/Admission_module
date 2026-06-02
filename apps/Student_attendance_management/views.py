from itertools import count
from multiprocessing import context
from urllib import request
from apps.Student_attendance_management.forms import BatchForm

from rest_framework import viewsets
from django.shortcuts import render
from apps.admissions.models import Course, Enrollment
from django.utils import timezone
from rest_framework import generics
from rest_framework import status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import localdate

from .models import (
    Trainer,
    Batch,
    Attendance
)

from .serializers import (
    TrainerSerializer,
    BatchSerializer,
    AttendanceSerializer
)


class TrainerViewSet(viewsets.ModelViewSet):

    queryset = Trainer.objects.all()

    serializer_class = TrainerSerializer


class BatchViewSet(viewsets.ModelViewSet):

    queryset = Batch.objects.all()

    serializer_class = BatchSerializer

class AttendanceViewSet(viewsets.ModelViewSet):

    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def create(self, request, *args, **kwargs):

        enrollment = request.data.get('enrollment')
        batch = request.data.get('batch')
        attendance_status = request.data.get('status')

        attendance_date = timezone.now().date()

        batch_obj = Batch.objects.get(id=batch)

        attendance, created = Attendance.objects.update_or_create(

            enrollment_id=enrollment,
            batch_id=batch,
            attendance_date=attendance_date,

            defaults={
                'status': attendance_status,
                'trainer': batch_obj.trainer
            }
        )

        serializer = self.get_serializer(attendance)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


def batches_page(request):

    form = BatchForm()

    context = {
        'form': form
    }

    return render(
        request,
        'attendance/batches.html',
        context
    )


def mark_attendance_page(request, batch_id):

    batch = Batch.objects.get(
        id=batch_id
    )

    enrollments = Enrollment.objects.filter(
        admission__course=batch.course
    )

    attendance_records = Attendance.objects.filter(
        batch=batch,
        attendance_date=timezone.now().date()
    )

    attendance_map = {
        att.enrollment_id: att.status
        for att in attendance_records
    }

    context = {
        'batch': batch,
        'enrollments': enrollments,
        'attendance_map': attendance_map
    }

    return render(
        request,
        'attendance/mark_attendance.html',
        context
    )


@api_view(['GET'])
def today_attendance_summary(request, batch_id):

    today = timezone.now().date()

    qs = Attendance.objects.filter(
        batch_id=int(batch_id),  
        attendance_date=today
    )

    data = {
        "present": qs.filter(status="Present").count(),
        "absent": qs.filter(status="Absent").count(),
        "late": qs.filter(status="Late").count(),
        "total": qs.count()
    }

    return Response(data)


@api_view(['POST'])
def bulk_attendance(request):

    enrollment = request.data.get('enrollment')
    batch = request.data.get('batch')
    attendance_status = request.data.get('status')
    remarks = request.data.get('remarks', '')

    attendance_date = timezone.now().date()

    batch_obj = Batch.objects.get(id=batch)

    Attendance.objects.update_or_create(

        enrollment_id=enrollment,
        batch_id=batch,
        attendance_date=attendance_date,

        defaults={
            'status': attendance_status,
            'trainer': batch_obj.trainer,
            'remarks': remarks
        }
    )

    return Response({
        'message': 'Attendance saved'
    })