from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
     peoples =[
          {"name":"amar","age": 26},
          {"name":"Sachin","age": 21},
          {"name":"Kartik","age": 28},
          {"name":"Saurabh","age": 26},
          {"name":"SAraswati","age": 30}

     ]
     return render(request,'index.html',context={'peoples':peoples})

def about(request):
     return render(request,'about.html')

def contect(request):
     return render(request,'contect.html')
