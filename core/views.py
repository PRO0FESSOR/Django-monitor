from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import  LoginForm
from django.db import connection
from .query import getSelectedDate , updateSelectedDate , getFromToDT , getSwitchStatus , toggleSwitchStatus,gettodate
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime


# Create your views here.

#loginform

def user_login(request):
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

#logout

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

#home 
  
def home(request):
    if request.user.is_authenticated : 

        toggle_value = ""
        From_datee=getSelectedDate()
        emp_value=None
        if request.method == 'POST':

            print(request.get_full_path())
            From_datee=request.POST.get('currdate')
            To_datee=request.POST.get('currdating')
            toggle_value = request.POST.get('toggler')
            emp_value = request.POST.get('employee')

            #handeling toggle

            if toggle_value==None:
                toggle_value="OFF"
                
            
            print(f"toggle --> {toggle_value}")
            
            toggleSwitchStatus(toggle_value) 

            #handeling datetime

            if From_datee:
                if To_datee:
                    print(f"to-date -->{To_datee}")
                    updateSelectedDate(From_datee,To_datee)
                else:
                    updateSelectedDate(From_datee,From_datee)

                print(f"from-date -->{From_datee}")
                

            
            #handeling search 

            if emp_value!="Open this select menu":
                print(f"selected user -->{emp_value}")
                 

            with open('data.txt', 'w') as file:
                file.write(f"Toggle Value: {toggle_value}\n")
                file.write(f"From Date: {From_datee}\n")
                file.write(f"To Date: {To_datee}\n")
                file.write(f"Employee Value: {emp_value}\n")
                
        return render(request,'core/home.html',{"data2":getFromToDT(),"fromdate":getSelectedDate(),"data3":getSwitchStatus(),"data6":emp_value,"todate":gettodate()})
        
    else:
        return HttpResponseRedirect('/login/')



