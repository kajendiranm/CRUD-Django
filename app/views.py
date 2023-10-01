from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import UserDetails,UserImage
from .forms import FileForm,RegisterForm
from django.views import View
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
# Create your views here.

@unauthenticated_user
def register_page(request):
    form = RegisterForm()

    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Customer')
            user.groups.add(group)
            name = form.cleaned_data['username']
            messages.success(request,'Account was created for ' + name)
            return redirect('login')
    return render(request,'register.html',{'form':form})

@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            messages.info(request,'Username or Password Incorrect!')

    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('login')

class FileUploadView(CreateView):
    template_name = 'file.html'
    model = UserImage
    fields = '__all__'
    success_url = 'file'


class ProfileView(ListView):
    template_name = 'profiles.html'
    model = UserImage
    context_object_name = 'images'

# class FileUploadView(View):
#     def get(self,request):
#         form = FileForm()
#         return render(request,'file.html',{'form':form})
#     def post(self,request):
#         form = FileForm(request.POST,request.FILES)
#         if form.is_valid():
#             UserImage.objects.create(image=request.FILES['image'])
#             return HttpResponseRedirect('file')
#         return render(request,'file.html',{'form':form})
        

@login_required(login_url='login')
@admin_only
def index(request):
    print(request.user.groups.all()[0].name)
    users = UserDetails.objects.all().order_by('-id')
    return render(request,'index.html',{'users':users})

def create(request):
    if request.method == 'POST':
        UserDetails.objects.create(name=request.POST['name'], email=request.POST['email'] ,place=request.POST['place'] )
        with open('temp/image.jpg','wb+') as dest:
            for chunk in request.FILES['file'].chunks():
                dest.write(chunk)
        return redirect('index')

def delete(request,id):
    user = UserDetails.objects.get(id=id)
    user.delete()
    return redirect('index')

def update(request,id):
    user = UserDetails.objects.get(id=id)
    if request.method == 'POST':
        user.name = request.POST['name']
        user.email = request.POST['email']
        user.place = request.POST['place']
        user.save()
        return redirect('index')
    return render(request,'update.html',{'user':user})

