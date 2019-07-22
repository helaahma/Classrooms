from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import ClassroomForm, SigninForm, SignupForm, StudentForm
from .models import Classroom, Student


def classroom_list(request):
    return render(request, 'classroom_list.html')


def classroom_detail(request, classroom_id):
    clas= Classroom.objects.get(id= classroom_id)
    clas.students.all()
    students= Student.objects.filter(classroom=clas).order_by('name', 'exam_grade')
    
    context= {
    "classroom":clas,
    "students": students
    }
    
    return render(request, 'classroom_detail.html', context)


def classroom_create(request):
    if request.user.is_authenticated:
        form = ClassroomForm()
        if request.method == "POST":
            form = ClassroomForm(request.POST, request.FILES or None)
            if form.is_valid():
                classr = form.save(commit = False)
                classr.teacher = request.user
                classr.save()
                messages.success(request, "Successfully Created!")
                return redirect('signin')
            print (form.errors)
        context = {
        "form": form,
        }
        return render(request, 'create_classroom.html', context)
    return redirect('signin')


def classroom_update(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    form = ClassroomForm(instance=classroom)
    if request.method == "POST":
        form = ClassroomForm(request.POST, (request.FILES or None), instance=classroom)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully Edited!")
            return redirect('classroom-list')
        print (form.errors)
    context = {
    "form": form,
    "classroom": classroom,
    }
    return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
    Classroom.objects.get(id=classroom_id).delete()
    messages.success(request, "Successfully Deleted!")
    return redirect('classroom-list')

def sign_in(request):
    form = SigninForm()
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('classroom-list')
    context = {
        "form":form,
    }
    return render(request,'signin.html', context)

def classroom_signup(request):
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(user.password)
            user.save()

            login(request, user)
            return redirect("classroom-list")
    context = {
        "form":form,
    }
    return render(request, 'signup.html', context)


def classroom_signout(request):
    logout(request)
    return redirect('signin')



def add_student(request, classroom_id):
    classroom= Classroom.objects.get(id=classroom_id)
    form = StudentForm()
  
    if request.method == "POST":

        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            return redirect('classroom-detail', classroom_id)
    context = {
        "form":form,
        "classroom": classroom ,
        }
    return render (request, "student_add.html", context)



