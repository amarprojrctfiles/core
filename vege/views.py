from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator
# Create your views here.
def receipes(request):
    if request.method == "POST":
        data = request.POST
        recepie_image = request.FILES.get('recepie_image')
        recepie_name = data.get('recepie_name')
        receipe_description = data.get('receipe_description')

        Receipe.objects.create(
            recepie_image=recepie_image,
            recepie_name = recepie_name,
            receipe_description = receipe_description,
            )
        
        return redirect('/receipes/')
    
    queryset = Receipe.objects.all()
    contaxt = {'receipes' : queryset}
        
    return render(request,'receipes.html', contaxt)

def update_receipe(request, id):
    queryset = Receipe.objects.get(id = id)

    if request.method == "POST":
        data = request.POST
        recepie_image = request.FILES.get('recepie_image')
        recepie_name = data.get('recepie_name')
        receipe_description = data.get('receipe_description')

        queryset.recepie_name = recepie_name
        queryset.receipe_description = receipe_description

        if recepie_image:
            queryset.recepie_image =recepie_image
        
        queryset.save()
        return redirect('/receipes/')
    
    contaxt = {'receipe' : queryset}
    return render(request,'update_receipes.html', contaxt)

def delete_receipe(request,id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipes/')

def login_page(request):
    if request.method=="POST":
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user is None:
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/receipes/')
    
    return render(request,'login.html')

def register(request):
    if request.method=="POST":
        first_name= request.POST.get('first_name')
        last_name= request.POST.get('last_name')
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            )
        user.set_password(password)
        user.save()
        
    return render(request,'register.html')


from django.db.models import Q,Sum


def get_students(request):
    queryset = Student.objects.all()
    if request.GET.get('search'):
        search = request.GET.get('search')
        queryset = queryset.filter(
            
            Q(student_name__icontains =search)|
            Q(department__department__icontains =search)|
            Q(student_id__student_id__icontains =search)
        )

    paginator = Paginator(queryset, 3)  # Show 25 contacts per page.

    page_number = request.GET.get("page",1)
    page_obj = paginator.get_page(page_number)

    return render(request,'report/students.html',{'queryset': page_obj})

from .seed import generate_report_card

def see_marks(request,student_id):
    # generate_report_card()
    queryset = SubjectMarks.objects.filter(student__student_id__student_id=student_id)
    total_marks=queryset.aggregate(total_marks = Sum('marks'))

    return render(request,'report/see_marks.html',{'queryset': queryset,'total_marks':total_marks})
