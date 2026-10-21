from datetime import datetime

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from myapp.models import Login, User, Contact, Complaint



def signup(request):
    return render(request,'signup.html')

def signup_post(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    gender = request.POST['gender']
    photo = request.FILES['photo']
    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
    fs.save(date, photo)
    path = fs.url(date)
    password = request.POST['password']
    cpassword = request.POST['cpassword']
    if password==cpassword:

        lobj = Login()
        lobj.username = email
        lobj.password = password
        lobj.type = 'user'
        lobj.save()

        obj =User()
        obj.name = name
        obj.email = email
        obj.phone = phone
        obj.gender = gender
        obj.photo = path
        obj.LOGIN = lobj
        obj.save()
    else:
        return HttpResponse('''<script>alert("Password & Confirm Password Doesn't Match");window.location='/myapp/signup/'</script>''')

    return HttpResponse('''<script>alert("Sign up Succesful");window.location='/myapp/login/'</script>''')


def login(request):
    return render(request,'login.html')

def login_post(request):
    username=request.POST['username']
    password=request.POST['password']
    l = Login.objects.filter(username=username, password=password)

    if l.exists():
        log1 = Login.objects.get(username=username, password=password)
        request.session['lid'] = log1.id

        if log1.type == 'user':
            return HttpResponse('''<script>alert("Logged in succesfull");window.location='/myapp/userhome/'</script>''')

        elif log1.type == 'admin':
            return HttpResponse('''<script>alert("Logged in as Admin");window.location='/myapp/adminhome/'</script>''')

    return HttpResponse('''<script>alert("Invalid");window.location='/myapp/login/'</script>''')




def userhome(request):
    profile = User.objects.filter(LOGIN_id=request.session["lid"]).first()
    return render(request, "userhome.html", {"profile": profile})


def adminhome(request):
    return render(request,'adminhome.html')


def viewprofile(request):
    login_id = request.session.get("lid")
    data = User.objects.filter(LOGIN_id=login_id)
    return render(request, "viewprofile.html", {"i": data})



def addcontact(request):
    profile = User.objects.filter(LOGIN_id=request.session["lid"]).first()
    return render(request, "addcontact.html", {"profile": profile})

def addcontact_post(request):
    if request.method != "POST":
        return render("/myapp/addcontact/")

    photo = request.FILES.get("photo")
    if not photo:
        return rednder("/myapp/addcontact/")

    owner = User.objects.get(LOGIN_id=request.session["lid"])

    fs = FileSystemStorage()
    saved_name = fs.save(photo.name, photo)

    contact = Contact()
    contact.name = request.POST.get("name", "")
    contact.email = request.POST.get("email", "")
    contact.phone = request.POST.get("phone", "")
    contact.gender = request.POST.get("gender", "")
    contact.photo = fs.url(saved_name)
    contact.USER = owner
    contact.save()

    return HttpResponse('''<script>alert("Contact Added");window.location='/myapp/userhome/'</script>''')




def viewcontact(request):
    login_id = request.session["lid"]
    profile = User.objects.filter(LOGIN_id=login_id).first()
    data = Contact.objects.filter(USER__LOGIN_id=login_id)

    return render(request, "viewcontact.html", {"i": data,"profile": profile,})

def viewcontact_post(request):
    login_id = request.session["lid"]
    profile = User.objects.filter(LOGIN_id=login_id).first()
    search = request.POST.get("search", "")
    data = Contact.objects.filter(USER__LOGIN_id=login_id,name__icontains=search,)

    return render(request, "viewcontact.html", {"i": data,"profile": profile,})




def changepassword(request):
    profile = User.objects.filter(LOGIN_id=request.session["lid"]).first()
    return render(request, "changepassword.html", {"profile": profile})
def changepassword_post(request):
    oldpassword=request.POST['oldpassword']
    newpassword=request.POST['newpassword']
    cpassword=request.POST['cpassword']
    l = Login.objects.get(id=request.session['lid'])
    if l.password == oldpassword:
        if newpassword==cpassword and l.password!=newpassword:
            l.password=newpassword
            l.save()
            return HttpResponse('''<script>alert("Password Changed");window.location='/myapp/login/'</script>''')
        else:
            return HttpResponse('''<script>alert("New password & confirm password does'n match");window.location='/myapp/changepassword/'</script>''')
    else:
        return HttpResponse('''<script>alert("Invalid");window.location='/myapp/changepassword/'</script>''')


def viewuser(request):
    data=User.objects.all()
    return render(request,'viewuser.html',{'i':data})



def sendcomplaint(request):
    profile = User.objects.filter(LOGIN_id=request.session["lid"]).first()
    return render(request, "sendcomplaint.html", {"profile": profile})

def sendcomplaint_post(request):
    complaint=request.POST['complaint']

    obj=Complaint()
    from datetime import datetime
    obj.date=datetime.now().today()
    obj.USER=User.objects.get(LOGIN_id=request.session['lid'])
    obj.complaint=complaint
    obj.reply='Pending'
    obj.Status='Pending'
    obj.save()

    return  HttpResponse('''<script>alert("Complaint Send");window.location='/myapp/userhome/'</script>''')



def viewcomplaint(request):
    data=Complaint.objects.all()
    return render(request,'viewcomplaint.html',{'i':data})

def viewcomplaint_post(request):
    data = Complaint.objects.all()

    fromdate = request.POST.get("fromdate", "")
    todate = request.POST.get("todate", "")

    if fromdate and todate:
        data = data.filter(date__range=[fromdate, todate])
    elif fromdate:
        data = data.filter(date__gte=fromdate)
    elif todate:
        data = data.filter(date__lte=todate)

    return render(request, "viewcomplaint.html", {"i": data})


def sendreply(request,id):
    return render(request,'sendreply.html',{'id':id})

def sendreply_post(request):
    sendreply=request.POST['sendreply']
    id=request.POST['id']

    obj = Complaint.objects.get(id=id)
    obj.reply = sendreply
    obj.Status = 'Replied'
    obj.save()

    return HttpResponse('''<script>alert("Reply Send");window.location='/myapp/viewcomplaint/'</script>''')

def viewreply(request):
    login_id = request.session["lid"]
    profile = User.objects.filter(LOGIN_id=login_id).first()
    data = Complaint.objects.filter(USER__LOGIN_id=login_id)

    return render(request, "viewreply.html", {"i": data,"profile": profile,})


def viewreply_post(request):
    login_id = request.session["lid"]
    profile = User.objects.filter(LOGIN_id=login_id).first()

    data = Complaint.objects.filter(USER__LOGIN_id=login_id)

    fromdate = request.POST.get("fromdate", "")
    todate = request.POST.get("todate", "")

    if fromdate and todate:
        data = data.filter(date__range=[fromdate, todate])
    elif fromdate:
        data = data.filter(date__gte=fromdate)
    elif todate:
        data = data.filter(date__lte=todate)

    return render(request, "viewreply.html", {
        "i": data,
        "profile": profile,
    })


def editprofile(request):
    data = User.objects.get(LOGIN_id=request.session['lid'])
    return render(request, 'editprofile.html', {'i':data})

def editprofile_post(request):
    name = request.POST['name']
    email = request.POST['email']
    phone = request.POST['phone']
    gender = request.POST['gender']


    obj = User.objects.get(LOGIN_id=request.session['lid'])
    if 'photo' in request.FILES:
        photo = request.FILES['photo']
        if photo!='':
            fs = FileSystemStorage()
            date = datetime.now().strftime('%Y%m%d-%H%M%S') + ".jpg"
            fs.save(date, photo)
            path = fs.url(date)
            obj.photo = path

    obj.name = name
    obj.email = email
    obj.phone = phone
    obj.gender = gender
    obj.save()

    return HttpResponse('''<script>alert("Profile Edited");window.location='/myapp/viewprofile/'</script>''')



def editcontact(request, id):
    login_id = request.session["lid"]
    profile = User.objects.filter(LOGIN_id=login_id).first()
    data = Contact.objects.get(id=id, USER__LOGIN_id=login_id)
    return render(request, "editcontact.html", {"i": data,"profile": profile,})

def editcontact_post(request):
    obj = Contact.objects.get(id=request.POST["id"])

    obj.name = request.POST["name"]
    obj.email = request.POST["email"]
    obj.phone = request.POST["phone"]
    obj.gender = request.POST["gender"]

    photo = request.FILES.get("photo")
    if photo:
        fs = FileSystemStorage()
        saved_name = fs.save(photo.name, photo)
        obj.photo = fs.url(saved_name)

    obj.save()
    return HttpResponse('''<script>alert("Contact Edited");window.location='/myapp/viewcontact/'</script>''')


def deletecontact(request,id):
    data=Contact.objects.filter(id=id).delete()
    return HttpResponse('''<script>alert("Contact Deleted");window.location='/myapp/viewcontact/'</script>''')


