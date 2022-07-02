from distutils.command.config import config
from urllib import request
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
import codecs
from unicodedata import name
import cryptography
from django.http import JsonResponse,QueryDict
from django.shortcuts import render
import pyrebase
from cryptography.fernet import Fernet
from django.core.exceptions import *
import rsa
from rsa.key import PrivateKey,PublicKey

Key = Fernet.generate_key()
fernet = Fernet(Key)

# PublicKey,PrivateKey = rsa.newKeys(512)
# print(PublicKey,PrivteKey)
config = {
  "apiKey": "AIzaSyAzGbRx3ge4KzClzNnGGhYTUOGgVSfBmok",
  "authDomain": "mobile-healthcare-7e096.firebaseapp.com",
  "databaseURL": "https://mobile-healthcare-7e096-default-rtdb.firebaseio.com",
  "projectId": "mobile-healthcare-7e096",
  "storageBucket": "mobile-healthcare-7e096.appspot.com",
  "messagingSenderId": "14621432131",
  "appId": "1:14621432131:web:625153965eac81761677f6",
  "measurementId": "G-651CLKR5K4"
};
firebase=pyrebase.initialize_app(config)
authe=firebase.auth()
database=firebase.database()
def adddata(request):
    name=request.POST.get('name')
    age=request.POST.get('age')
    place=request.POST.get('place')
    url=request.POST.get('url')
    
    
    database.child('Data').push({
        "name":fernet.encrypt(str(name).encode()).decode(),
        "age":fernet.encrypt(str(age).encode()).decode(),
        "place":fernet.encrypt(str(place).encode()).decode(),
        "image":fernet.encrypt(str(url).encode()).decode(),
    })
    return render(request,'adddata.html')



# def viewdata(request):
#     try:
#         data = database.child('Data').shallow().get().val()
#         uidlist = []
#         requid = 'null'
#         for i in data:
#             uidlist.append(i)
#             for i in uidlist:
#                 val = database.child('Data').child(i).child('name').get().val()
#                 val=val.lower()
#                 if(val):
#                     requid = i
#             if requid == 'null':
#                 return render(request,"viewData.html")
#             print(requid)
#         name=bytes(database.child('Data').child(requid).child('name').get().val(),'ascii') 
#         age=bytes(database.child('Data').child(requid).child('age').get().val(),'ascii')
#         place=bytes(database.child('Data').child(requid).child('place').get().val(),'ascii')
#         image=bytes(database.child('Data').child(requid).child('image').get().val(),'ascii')
#         decname = fernet.decrypt(name).decode('ascii')
#         decage = fernet.decrypt(age).decode('ascii')
#         decplace = fernet.decrypt(place).decode('ascii')
#         decimage = fernet.decrypt(image).decode('ascii')
        
#         print(decname)
        
#         return render(request,'viewData.html',{
#             "username":decname,
#             "age":decage,
#             "place":decplace,
#             "image":decimage
#         })                  
#     except cryptography.fernet.InvalidToken:
#         return render(request,'viewData.html',)                         
                   

def view(request):
    return render(request,"viewdata.html")


# # Create your views here.




def show(request):
    return render(request,'index.html')



def reg(request):
    form = CreateUserForm()
    if request.method == 'POST':
       form = CreateUserForm(request.POST)
    if form.is_valid():
        form.save()
        user = form.cleaned_data.get('username')
        messages.success(request,'Account was created for'+ user)
        
        return redirect('lo')
    context = {'form':form}
    return render(request,'regis.html',context)


def lo(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('use')
        else:
            messages.info(request,'username OR password is  incorrect')
    context = {}
    return render(request,'login.html',context)
def use(request):
    return render(request,'user.html')

# def signIn(request):
#     return render(request,"firebaselogin.html")
# def home(request):
#     return render(request,"user.html")
def postsignIn(request):
    email=request.POST.get('email')
    passw=request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid credentials!!Please check your Data"
        return render (request,"firebaselogin.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"user.html",{"email".email})
def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"index.html")
def signUp(request):
    return render(request,"Registration.html")
def postsignUp(request):
    email = request.POST.get('email')
    passs = request.POST.get('pass')
    name = request.POST.get('name')
    try:
        # creating a user with the given email and password
        user=authe.create_user_with_email_and_password(email,passs)
        uid = user['localId']
        # // storing data in session
        idtoken = request.session['uid']
        # ////////////
        print("uid=>",uid)
    except:
        return render(request,"Registration.html")
    return render(request,"Login.html")