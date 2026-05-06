from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .forms import StudentForm, AdmissionForm, EnrollmentForm 
from .models import *
from django.contrib import messages
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table
from .filters import StudentFilter
from datetime import date
from django.db import transaction


# Create your views here.

def home(request):
    return render(request, 'admissions/home.html')


def student(request):
    student_form = StudentForm()
    admission_form = AdmissionForm()
    enrollment_form = EnrollmentForm()

    courses = Course.objects.all()

    if request.method == "POST":
        student_form = StudentForm(request.POST, request.FILES)
        admission_form = AdmissionForm(request.POST)
        enrollment_form = EnrollmentForm(request.POST, request.FILES)

        if (student_form.is_valid() and 
            admission_form.is_valid() and 
            enrollment_form.is_valid()):

            with transaction.atomic():
                student = student_form.save()

                admission = Admission.objects.create(
                    student=student,
                    course=admission_form.cleaned_data['course'],
                    status=admission_form.cleaned_data['status']
                )

                enrollment = enrollment_form.save(commit=False)
                enrollment.admission = admission
                enrollment.save()

            messages.success(request, "Student enrolled successfully!")
            return redirect('student_list')
        
        else:
            messages.error(request, "Form has errors. Please check!")

    return render(request, 'admissions/register.html', {
        'student_form': student_form,
        'admission_form': admission_form,
        'enrollment_form': enrollment_form,
        'courses': courses,
    })

def student_list(request):

    students = Student.objects.prefetch_related(
        'admissions__enrollment',
        'admissions__course',
    ).all()

    #  FILTER
    student_filter = StudentFilter(request.GET, queryset=students)
    filtered_students = student_filter.qs.distinct().order_by('-id')

    #  PAGINATION
    paginator = Paginator(filtered_students, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    format = request.GET.get('format')

    # ================= EXCEL =================
    if format == 'excel':
        wb = Workbook()
        ws = wb.active
        ws.append(["Student", "Course", "Batch", "Phone", "Payment Status", "Joined"])

        for s in filtered_students:
            for admission in s.admissions.all():
                enrollment = getattr(admission, 'enrollment', None)

                ws.append([
                    f"{s.First_name} {s.Last_name}",
                    str(admission.course),
                    enrollment.batch if enrollment else "-",
                    s.phone_no,
                    enrollment.payment_status if enrollment else "-",
                    str(enrollment.start_date) if enrollment else "-"
                ])

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=students.xlsx'
        wb.save(response)
        return response

    # ================= PDF =================
    if format == 'pdf':
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="students.pdf"'

        data = [["Student", "Course", "Batch", "Phone", "Payment Status", "Joined"]]

        for s in filtered_students:
            for admission in s.admissions.all():
                enrollment = getattr(admission, 'enrollment', None)

                data.append([
                    f"{s.First_name} {s.Last_name}",
                    str(admission.course),
                    enrollment.batch if enrollment else "-",
                    s.phone_no,
                    enrollment.payment_status if enrollment else "-",
                    str(enrollment.start_date) if enrollment else "-"
                ])

        doc = SimpleDocTemplate(response)
        table = Table(data)
        doc.build([table])

        return response

    return render(request, 'admissions/student_list.html', {
        'page_obj': page_obj,
        'filter': student_filter,
        'courses': Course.objects.all(),
        'total_students': filtered_students.count()
    })

def edit_student(request, id):
    student = Student.objects.get(id=id)

    if request.method == 'POST':
        student.First_name = request.POST.get('First_name')
        student.Last_name = request.POST.get('Last_name')
        student.phone_no = request.POST.get('phone_no')
        student.email = request.POST.get('email')
        student.dob = request.POST.get('dob')
        student.address = request.POST.get('address')

        student.save()
        return redirect('student_list')

    return render(request, "admissions/edit_student.html", {'student': student})

        

def delete_student(request, id):
    student=Student.objects.get(id=id)
    student.delete()
    messages.success(request, "✅Student deleted successfully")
    return redirect('student_list')

def search_students(request):

    students = Student.objects.prefetch_related(
        'admissions__course',
        'admissions__enrollment'
    )

    student_filter = StudentFilter(request.GET, queryset=students)
    filtered_students = student_filter.qs.distinct()

    paginator = Paginator(filtered_students, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "admissions/search_students.html", {
        'filter': student_filter,
        'page_obj': page_obj,
        'courses': Course.objects.all()
    })

    
def view_student(request, id):
    student = Student.objects.prefetch_related(
        'admissions__course',
        'admissions__enrollment'
    ).get(id=id)

    admission = student.admissions.first()   # get latest/first admission
    enrollment = admission.enrollment if admission else None

    return render(request, "admissions/view_student.html", {
        'student': student,
        'admission': admission,
        'enrollment': enrollment
    })