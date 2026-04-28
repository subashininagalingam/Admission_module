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


# Create your views here.

def home(request):
    return render(request, 'admissions/home.html')


def student(request):
    student_form = StudentForm()
    admission_form = AdmissionForm()

    if request.method == "POST":
        student_form = StudentForm(request.POST)
        admission_form = AdmissionForm(request.POST)

        if student_form.is_valid() and admission_form.is_valid():
            student = student_form.save()
            course = admission_form.cleaned_data['course']

            Admission.objects.create(
                student=student,
                course=course,
                status='confirmed'
            )

            return redirect('enroll',id=student.id)

    return render(request, 'admissions/register.html', {
        'student_form': student_form,
        'admission_form': admission_form
    })

def enroll(request, id):
    student = Student.objects.get(id=id)

    admission = Admission.objects.filter(student=student).first()

    if hasattr(admission, 'enrollment'):
        messages.warning(request, "Already enrolled!")
        return redirect('student_list')

    form = EnrollmentForm()

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.admission = admission
            enrollment.save()

            admission.status = 'enrolled'
            admission.save()

            return redirect('student_list')

    return render(request, 'admissions/enroll.html', {
        'form': form,
        'student': student
    })

   
def student_list(request):

    students = Student.objects.prefetch_related(
        'admissions__enrollment',
        'admissions__course',
    ).all()

    #  FILTER
    student_filter = StudentFilter(request.GET, queryset=students)
    filtered_students = student_filter.qs.distinct()

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
    students = Student.objects.prefetch_related(
        'admissions__course',
        'admissions__enrollment'
    )
    student = students.get(id=id)
    return render(request, "admissions/view_student.html", {'student': student})