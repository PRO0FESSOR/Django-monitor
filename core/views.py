from django.shortcuts import render , redirect
from django.http import HttpResponseRedirect , HttpResponse
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import  LoginForm
from django.db import connection
from .query import getSelectedDate , updateSelectedDate , getFromToDT , getSwitchStatus , toggleSwitchStatus,getGlanceValues,log_values,rdpSessions,browsingSessions,processSessions
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
                # input_format = "%m/%d/%Y"
                # output_format = "%Y-%m-%d"
                # date_object = datetime.strptime(datecurr, input_format)
                # formatted_date = date_object.strftime(output_format)
                # updateSelectedDate(formatted_date)
                # print(formatted_date)
                if To_datee:
                    print(To_datee)
                    updateSelectedDate(From_datee,To_datee)
                else:
                    updateSelectedDate(From_datee,From_datee)

                print(From_datee)
                

            
            #handeling search 

            if emp_value!="Open this select menu":
                print(emp_value)
                return HttpResponseRedirect(f'/user_data/{emp_value}/')               
                
                 
   
        return render(request,'core/home.html',{"data2":getFromToDT(),"data1":getSelectedDate(),"data3":getSwitchStatus(),"data4":getGlanceValues(),"data5":log_values(),"data6":emp_value})
        
    else:
        return HttpResponseRedirect('/login/')

#description 

def description(request,user):
    glance_data = getGlanceValues()
    user_data = glance_data.get(user, None)
    rdp_data = rdpSessions(user)
    browsing_data = browsingSessions(user)
    process_data = processSessions(user)    
                
    
    context = {
        'user_data': user_data,
        'rdpdata':rdp_data,
        'brdata':browsing_data,
        'prdata':process_data
    }
    return render(request,'core/description.html',context)


#search

def user_data(request, emp_value):
    glance_data = getGlanceValues()
    user_data = glance_data.get(emp_value, None)
    if user_data:
        return render(request, 'core/user_data.html', {'user_data': user_data})
    else:
        # Handle the case where user_data is None
        return HttpResponse('User data not found')