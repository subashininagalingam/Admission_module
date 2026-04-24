from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from .forms import StudentForm, EnrollmentForm
from .models import *
from django.contrib import messages
from openpyxl import Workbook
from reportlab.platypus import SimpleDocTemplate, Table
from .filters import StudentFilter
from datetime import date


# Create your views here.

def home(request):
    return render(request, 'admissions/home.html')

def student(request):
    form = StudentForm()

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')

    return render(request, 'admissions/register.html', {'form': form})

def enroll(request, id):
    student = Student.objects.get(id=id)

    # ✅ Prevent multiple enrollments
    if student.enrollments.exists():
        messages.warning(request, "Student already enrolled!")
        return redirect('student_list')

    form = EnrollmentForm(initial={'student': student})

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)

        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.student = student

            if enrollment.start_date <= date.today():
                messages.error(request, "Only future dates are allowed (tomorrow onwards)!")
                return render(request, 'admissions/enroll.html', {
                'form': form,
                'student': student
            })

            enrollment.save()
            messages.success(request, "Enrollment successful!")
            return redirect('student_list')

    return render(request, 'admissions/enroll.html', {
        'form': form,
        'student': student
    })


def success(request):
    return render(request,"admissions/success.html")
   
def student_list(request):
    students = Student.objects.prefetch_related('enrollments__course').all()

    student_filter = StudentFilter(request.GET, queryset=students)
    filtered_students = student_filter.qs.distinct()

    paginator = Paginator(filtered_students, 5)  # 5 per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    format = request.GET.get('format')

    # ================= EXCEL =================
    if format == 'excel':
        wb = Workbook()
        ws = wb.active
        ws.append(["Student", "Course", "Batch", "Phone", "Payment Status", "Joined"])

        for s in filtered_students:
            for e in s.enrollments.all():
                ws.append([
                    f"{s.First_name} {s.Last_name}",
                    str(e.course),
                    e.batch,
                    s.phone_no,
                    e.payment_status,
                    str(e.start_date)
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
            for e in s.enrollments.all():
                data.append([
                    f"{s.First_name} {s.Last_name}",
                    str(e.course),
                    e.batch,
                    s.phone_no,
                    e.payment_status,
                    str(e.start_date)
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
    student=Student.objects.get(id=id)
    if (request.method=='POST'):
        student.name=request.POST.get('name')
        student.mobile_no=request.POST.get('mobile_no')
        student.email=request.POST.get('email') 
        student.dob=request.POST.get('dob')
        student.address=request.POST.get('address')
        student.save()
        return redirect('student_list')
    return render(request, "admissions/edit_student.html", {'student': student})

        

def delete_student(request, id):
    student=Student.objects.get(id=id)
    student.delete()
    messages.success(request, "✅Student deleted successfully")
    return redirect('student_list')

def search_students(request):
    student_filter = StudentFilter(request.GET, queryset=Student.objects.all())
    return render(request, "admissions/search_students.html", {'filter': student_filter})

def view_student(request, id):
    student = Student.objects.get(id=id)
    return render(request, "admissions/view_student.html", {'student': student})