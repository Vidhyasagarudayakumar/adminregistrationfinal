from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .forms import RegistrationForm,Userloginform,changepasswordform
from django.contrib.auth.models import User
from .models import registration
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse





def userregistrationform(request):
    form = RegistrationForm()
    if request.method == "POST":
        form= RegistrationForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password1']
            phonenumber = data['phonenumber']
            adminuser = User.objects.create_user(username=username,email=email,password=password)
            registration.objects.create(user=adminuser,phonenumber=phonenumber)
            request.method="GET"
            return HttpResponseRedirect(reverse('home'))


    return render(request,'adminregistration/register.html', {'form':form})









def loginform(request):
    form = Userloginform()
    if request.user.is_authenticated:
        return render(request, 'adminregistration/base.html')
    else:
        if request.method=="POST":
            form = Userloginform(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                username = data['username']
                password = data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        return render(request, 'adminregistration/base.html')
                    else:
                        return HttpResponse("Your  account is disabled.")
                else:
                    return HttpResponse("Invalid login details supplied.")


    return render(request, 'adminregistration/login.html', {'form': form})

def logoutt(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))




def home(request):
    if request.user.is_authenticated:
        return render(request, 'adminregistration/base.html')
    else:
        return HttpResponseRedirect(reverse('login'))

@login_required
def changepassword(request):
    form = changepasswordform(user=request.user,data=request.POST or None)
    if request.POST and form.is_valid():
        data = form.cleaned_data
        password = data['password1']
        pass1 = data['password']
        user = request.user
        u = user.check_password(pass1)
        if u:
            current_user = User.objects.get(username=user)
            current_user.set_password(password)
            current_user.save()
            present = authenticate(username =user, password = password)
            login(request, present)
            return redirect('login')
        else:
            form.errors['password']=['INVALID CURRENT PASSWORD']


    return render(request,'adminregistration/changepassword.html',{'form':form})
