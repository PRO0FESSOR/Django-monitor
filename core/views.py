from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import  LoginForm
from django.db import connection
from .query import getSelectedDate , updateSelectedDate , getFromToDT , getSwitchStatus , toggleSwitchStatus,glanceShortcut ,alltables,onlyglanceShortcut ,gettodate
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



#description 

def description(request,user):


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
                print(toggle_value)
            else:
                print(toggle_value)
            
            toggleSwitchStatus(toggle_value) 

            #handeling datetime

            if From_datee:
                if To_datee:
                    print(To_datee)
                    updateSelectedDate(From_datee,To_datee)
                else:
                    updateSelectedDate(From_datee,From_datee)

                print(From_datee)
                

            
            #handeling search 

            if emp_value!="Open this select menu":
                print(emp_value)
                return HttpResponseRedirect(f'/description/{emp_value}/') 




    user_data = onlyglanceShortcut(user)

    data = alltables(user)
    print(data)

    rdp_data = []
    browsing_data = []
    process_data = []

    for entry in data:
        if entry[2] == 'RDP':
            rdp_data.append(entry)
            process_data.append(entry)
        elif entry[2] == 'BROWSING':
            browsing_data.append(entry)
            process_data.append(entry)
        else:
            process_data.append(entry)

    # print(rdp_data)
    # print(browsing_data)
    # print(process_data) 
                
    
    context = {
        'user':user,
        'user_data': user_data,
        'rdpdata':rdp_data,
        'brdata':browsing_data,
        'prdata':process_data,
        "data3":getSwitchStatus(),
        "fromdate":getSelectedDate(),
        "todate":gettodate()
    }
    return render(request,'core/description.html',context)



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
                print(toggle_value)
            else:
                print(toggle_value)
            
            toggleSwitchStatus(toggle_value) 

            #handeling datetime

            if From_datee:
                if To_datee:
                    print(To_datee)
                    updateSelectedDate(From_datee,To_datee)
                else:
                    updateSelectedDate(From_datee,From_datee)

                print(From_datee)
                

            
            #handeling search 

            if emp_value!="Open this select menu":
                print(emp_value)
                return HttpResponseRedirect(f'/description/{emp_value}/') 
                 
   
        return render(request,'core/home.html',{"data2":getFromToDT(),"fromdate":getSelectedDate(),"data3":getSwitchStatus(),"data5":glanceShortcut(),"data6":emp_value,"todate":gettodate()})
        
    else:
        return HttpResponseRedirect('/login/')



