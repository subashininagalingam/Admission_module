from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    TrainerViewSet,
    BatchViewSet,
    AttendanceViewSet,
    batches_page,
    mark_attendance_page,
    bulk_attendance,
    today_attendance_summary,
)

router = DefaultRouter()

router.register(r'trainers', TrainerViewSet)

router.register(r'batches', BatchViewSet)

router.register(r'attendance', AttendanceViewSet)

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
        '',
        include(router.urls)
    ),

]