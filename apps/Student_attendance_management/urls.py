from django.urls import path, include

from . import views 
from rest_framework.routers import DefaultRouter

from .views import (
    AttendanceSubmitAPIView,
    SyllabusLogViewSet,
    TrainerViewSet,
    BatchViewSet,
    AttendanceViewSet,
    attendance_export,
    attendance_report_page,
    batches_page,
    mark_attendance_page,
    bulk_attendance,
    today_attendance_summary,
)

router = DefaultRouter()

router.register(r'trainers', TrainerViewSet)

router.register(r'batches', BatchViewSet)

router.register(r'attendance', AttendanceViewSet)

router.register(r'syllabus-logs',SyllabusLogViewSet)

urlpatterns = [

    path(
        'batches-page/',
        batches_page,
        name='batches_page'
    ),

    path(
    'mark-attendance/<int:batch_id>/',
    mark_attendance_page,
    name='mark_attendance_page'
    ),

    path('today-attendance/<int:batch_id>/', today_attendance_summary),

    path(
    'attendance/bulk/',
    bulk_attendance,
    name='bulk_attendance'
    ),

    path(
        "attendance/submit/",
        AttendanceSubmitAPIView.as_view(),
        name="attendance-submit"
    ),

    path(
    'attendance-report/',
    attendance_report_page,
    name='attendance_report'
),
path('attendance-export/', views.attendance_export, name='attendance_export'),

path(
        "student-attendance-summary/<int:student_id>/",
        views.student_attendance_summary,
        name="student_attendance_summary"
    ),
    path('get-batches/', views.get_batches_by_course, name='get-batches'),


    path(
        '',
        include(router.urls)
    ),

]