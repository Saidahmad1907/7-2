from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Course, Student
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Course
from django.core.paginator import Paginator



def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def course_detail(request, pk):
    course = Course.objects.get(id=pk)
    students = course.students.all()
    return render(request, 'courses/course_detail.html', {'course': course, 'students': students})
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render





def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('course_list')
    else:
        form = UserCreationForm()
    return render(request, 'courses/register.html', {'form': form})





def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('course_list')
    else:
        form = AuthenticationForm()
    return render(request, 'courses/login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('course_list')


def send_course_email(request, course_id):
    course = Course.objects.get(id=course_id)
    send_mail(
        subject=f"New Course Available: {course.title}",
        message=f"Dear user,\n\nWe are excited to announce a new course: {course.title}.\n\nDescription:\n{course.description}",
        from_email='your_email@gmail.com',
        recipient_list=['recipient_email@gmail.com'],  # Qabul qiluvchi email
        fail_silently=False,
    )
    return redirect('course_list')  # Course ro'yxatiga qaytarish




def course_list(request):
    courses = Course.objects.all()
    paginator = Paginator(courses, 5)  # Har bir sahifada 5 ta kurs bo'ladi
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'courses/course_list.html', {'page_obj': page_obj})
