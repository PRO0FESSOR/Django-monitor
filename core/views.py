from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import  LoginForm
from django.db import connection
from .query import getSelectedDate , updateSelectedDate , getFromToDT , getSwitchStatus , toggleSwitchStatus,getGlanceValues,log_values
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Create your views here.

#loginform

def login(request):
    if request.method=="POST":
        form = LoginForm(request=request , data=request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname,password=upass)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/') 
    else:
        form = LoginForm()
    return render(request,'core/login.html',{"form":form})

#home 
    
def home(request):
    toggle_value = ""
    datecurr=getSelectedDate()
    if request.method == 'POST':
        datecurr=request.POST.get('currdate')
        toggle_value = request.POST.get('toggler')

        if toggle_value==None:
            toggle_value="OFF"
            print(toggle_value)
        else:
            print(toggle_value)

        if datecurr:
            input_format = "%m/%d/%Y"
            output_format = "%Y-%m-%d"
            date_object = datetime.strptime(datecurr, input_format)
            formatted_date = date_object.strftime(output_format)
            updateSelectedDate(formatted_date)
            print(formatted_date)
            
        toggleSwitchStatus(toggle_value)      
   
        
    
    return render(request,'core/home.html',{"data2":getFromToDT(),"data1":getSelectedDate(),"data3":getSwitchStatus(),"toggle_value":toggle_value,"data4":getGlanceValues(),"data5":log_values()})

#description 

def description(request,user):
    return render(request,'core/description.html',{"name":user})