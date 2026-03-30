import base64

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from datetime import datetime
# Create your views here.
from myapp.models import *


def login(request):
    return render(request,'login index.html')

def login_post(request):
    username=request.POST['textfield']
    password=request.POST['textfield2']
    log=Login.objects.filter(username=username,password=password)
    if log.exists():
        log1 = Login.objects.get(username=username, password=password)
        request.session['lid'] = log1.id
        if log1.type=="admin":
            return HttpResponse('''<script>alert('Login Successfully');window.location="/myapp/Admin_home/"</script>''')
        elif log1.type=="fuelstation":
            return HttpResponse('''<script>alert('Login Successfully');window.location="/myapp/Fuelstation_home/"</script>''')
        elif log1.type=="evstation":
            return HttpResponse('''<script>alert('Login Successfully');window.location="/myapp/EVstation_home/"</script>''')
        else:
            return HttpResponse('''<script>alert('User not found');window.location="/myapp/login/"</script>''')
    else:
        return HttpResponse('''<script>alert('User not Exist');window.location="/myapp/login/"</script>''')



def home_admin(request):
    return render(request,'Admin/homeindex.html')

def password_change(request):
    return render(request,'Admin/change password.html')

def password_post(request):
    oldpassword=request.POST['textfield']
    newpassword=request.POST['textfield2']
    confirmpassword=request.POST['textfield3']

    id=request.session['lid']
    chp=Login.objects.get(id=id)
    if chp.password==oldpassword:
        if newpassword==confirmpassword:
            Login.objects.filter(id=id).update(password=newpassword)
            return HttpResponse('''<script>alert('password changed successfully');window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse('''<script>alert('User not found');window.location="/myapp/Admin_password_change/"</script>''')
    else:
        return HttpResponse('''<script>alert('you must login first');window.location="/myapp/login/"</script>''')



def view_fuel(request):
    a=FuelStation.objects.filter(status="pending")
    return render(request,'admin/view fuel station.html',{'data':a})

def view_fuel_post(request):
    search=request.POST['textfield']
    a=FuelStation.objects.filter(name__icontains=search)
    return render(request,'admin/view fuel station.html',{'data':a})

def approve_fuel(request):
    a=FuelStation.objects.filter(status='approved')
    return render(request,'admin/view accepted fuel station.html',{'data':a})


def approve_post(request,id):
    if request.session['lid']!='':

        lobj = Login.objects.get(id=id)
        lobj.type = 'fuelstation'
        lobj.save()

        fobj = FuelStation.objects.get(LOGIN=id)
        fobj.LOGIN = lobj
        fobj.status = 'approved'
        fobj.save()

        return HttpResponse('''<script>alert('approved successfully');window.location="/myapp/Admin_approve_fuel/"</script>''')
    else:
        return HttpResponse('''<script>alert('approved successfully');window.location="/myapp/login/"</script>''')




def reject_fuel(request):
    a=FuelStation.objects.filter(status='rejected')
    return render(request,'admin/view rejected fuel station.html',{'data':a})

def reject_post(request, id):
        if request.session['lid'] != '':

            lobj = Login.objects.get(id=id)
            lobj.type = 'rejected'
            lobj.save()

            fobj = FuelStation.objects.get(LOGIN=id)
            fobj.LOGIN = lobj
            fobj.status = 'rejected'
            fobj.save()

            return HttpResponse('''<script>alert('you are rejected');window.location="/myapp/Admin_reject_fuel/"</script>''')
        else:
            return HttpResponse('''<script>alert('you are rejected');window.location="/myapp/login/"</script>''')


def view_EV(request):
    b=evstation.objects.filter(status="pending")
    return render(request,'admin/view EV  station.html',{'data':b})


def view_EV_post(request):
    search=request.POST['textfield']
    b=evstation.objects.filter(name__icontains=search)
    return render(request,'admin/view EV  station.html',{'data':b})

def approve_EV(request):
    b = evstation.objects.filter(status='approved')
    return render(request,'admin/view accepted EV station.html',{'data':b})

def approve_EV_post(request,id):
    if request.session['lid']!='':

        lobj = Login.objects.get(id=id)
        lobj.type = 'evstation'
        lobj.save()

        fobj = evstation.objects.get(LOGIN=id)
        fobj.LOGIN = lobj
        fobj.status = 'approved'
        fobj.save()

        return HttpResponse(
        '''<script>alert('approved successfully');window.location="/myapp/Admin_approve_fuel/"</script>''')
    else:
        return HttpResponse('''<script>alert('approved successfully');window.location="/myapp/login/"</script>''')

def approve_worker_post(request,id):
    if request.session['lid']!='':

        lobj = Login.objects.get(id=id)
        lobj.type = 'worker'
        lobj.save()

        fobj = Worker.objects.get(LOGIN=id)
        fobj.status = 'approved'
        fobj.save()

        return HttpResponse(
        '''<script>alert('approved successfully');window.location="/myapp/Admin_approve_worker/"</script>''')
    else:
        return HttpResponse('''<script>alert('approved successfully');window.location="/myapp/login/"</script>''')

def reject_worker_post(request,id):
    if request.session['lid']!='':

        lobj = Login.objects.get(id=id)
        lobj.type = 'reject'
        lobj.save()

        fobj = Worker.objects.get(LOGIN=id)
        fobj.status = 'rejected'
        fobj.save()

        return HttpResponse(
        '''<script>alert('approved successfully');window.location="/myapp/approve_worker_post/"</script>''')
    else:
        return HttpResponse('''<script>alert('approved successfully');window.location="/myapp/login/"</script>''')

def wrkr_send_req(request):
        lid = request.POST['lid']
        print(lid)
        serviceid = request.POST['sid']

        s = Servicerequest()
        s.SERVICE_id = serviceid
        s.USER = User.objects.get(LOGIN_id=lid)
        s.status = "pending"
        s.date = datetime.now().date()
        s.save()
        return JsonResponse({"status": "ok"})


def reject_EV(request):
    b = evstation.objects.filter(status='rejected')
    return render(request,'admin/view rejecteted EV station.html',{'data':b})


def reject_EV_post(request, id):
    if request.session['lid'] != '':

        lobj = Login.objects.get(id=id)
        lobj.type = 'rejected'
        lobj.save()

        fobj = evstation.objects.get(LOGIN=id)
        fobj.LOGIN = lobj
        fobj.status = 'rejected'
        fobj.save()

        return HttpResponse(
            '''<script>alert('you are rejected');window.location="/myapp/Admin_reject_fuel/"</script>''')
    else:
        return HttpResponse('''<script>alert('you are rejected');window.location="/myapp/login/"</script>''')


def view_worker(request):
    c=Worker.objects.filter(status="pending")
    return render(request,'admin/view WORKER.html',{'data':c})


def approve_worker(request):
    c=Worker.objects.filter(status="approved")
    return render(request,'admin/view accepted worker.html',{'data':c})

def reject_worker(request):
    c = Worker.objects.filter(status="rejected")
    return render(request,'admin/view rejected worker.html',{'data':c})



def complaint(request):
    c=Complaint.objects.all()
    return render(request,'admin/View complaint.html',{'data':c})

def complaint_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    a= Complaint.objects.filter(date__range=[fromdate, todate])
    return render(request,'admin/View complaint.html',{'data':a})


def reply(request,id):
    # c=Complaint.objects.get(id=id)
    return render(request,'admin/Send reply.html',{"id":id})

def reply_post(request):
    id = request.POST['id']
    reply=request.POST['textarea']

    a=Complaint.objects.filter(id=id).update(reply=reply,status='replied')

    return HttpResponse(
        '''<script>alert('sending');window.location="/myapp/Admin_complaint/"</script>''')


def review_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    b = Review.objects.filter(date__range=[fromdate, todate])
    return render(request, 'admin/View review.html', {"data": b})


def review(request):
    b=Review.objects.all()
    return render(request,'admin/View review.html',{"data":b})

def home_fuelstation(request):
    return render(request,'Fuel station/homeindex.html')

def signup_fuel(request):
    return render(request,'fuelsignupindex.html')

def signupfuel_post(request):
    name=request.POST['textfield']
    photo=request.FILES['textfield2']
    email=request.POST['textfield3']
    phone=request.POST['textfield4']
    place=request.POST['textfield5']
    longtitude=request.POST['textfield6']
    latitude=request.POST['textfield7']
    state=request.POST['textfield8']
    city= request.POST['textfield9']
    pin=request.POST['textfield10']
    password=request.POST['textfield13']
    confirmpassword=request.POST['textfield14']

    fs=FileSystemStorage()
    date=datetime.now().strftime('%Y%m%d%H%M%S')+'jpg'
    fs.save(date,photo)
    path=fs.url(date)

    lobj=Login()
    lobj.username=email
    lobj.password=confirmpassword
    lobj.type='pending'
    lobj.save()

    fobj=FuelStation()
    fobj.name=name
    fobj.photo=path
    fobj.email=email
    fobj.phone=phone
    fobj.place=place
    fobj.longtitude=longtitude
    fobj.latitude=latitude
    fobj.state=state
    fobj.city=city
    fobj.pin=pin
    fobj.password=password
    fobj.confirmpassword=confirmpassword
    fobj.LOGIN=lobj
    fobj.status='pending'
    fobj.save()

    return HttpResponse('''<script>alert('you are signed in');window.location="/myapp/login/"</script>''')


def passwordfuel_change(request):
    return render(request,'Fuel station/change passwordfuel.html')

def passwordfuel_post(request):
    oldpassword=request.POST['textfield']
    newpassword=request.POST['textfield2']
    confirmpassword=request.POST['textfield3']
    id = request.session['lid']
    chp = Login.objects.get(id=id)
    if chp.password == oldpassword:
        if newpassword == confirmpassword:
            Login.objects.filter(id=id).update(password=newpassword)
            return HttpResponse(
                '''<script>alert('password changed successfully');window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse(
                '''<script>alert('User not found');window.location="/myapp/Fuelstation_passwordfuel_change/"</script>''')
    else:
        return HttpResponse('''<script>alert('you must login first');window.location="/myapp/login/"</script>''')



def view_profile(request):
    a = FuelStation.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Fuel station/View profile FS.html',{'i':a})

def edit_profile(request):
    a = FuelStation.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'Fuel station/Edit profile.html',{"data":a})

def edit_profile_post(request):

        name = request.POST['textfield']
        email = request.POST['textfield10']
        phone = request.POST['textfield9']
        place = request.POST['textfield8']
        longtitude = request.POST['textfield3']
        latitude = request.POST['textfield7']
        state = request.POST['textfield6']
        city = request.POST['textfield5']
        pin = request.POST['textfield4']
        # id = request.POST['id']
        fobj = FuelStation.objects.get(LOGIN_id=request.session['lid'])

        if 'fileField' in request.FILES:
            photo = request.FILES['fileField']
            fs = FileSystemStorage()
            date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
            fs.save(date, photo)
            path = fs.url(date)
            fobj.photo = path
            fobj.save()

        # lobj = Login()
        # lobj.username = email
        # lobj.save()


        fobj.name = name
        fobj.email = email
        fobj.phone = phone
        fobj.place = place
        fobj.longtitude = longtitude
        fobj.latitude = latitude
        fobj.state = state
        fobj.city = city
        fobj.pin = pin
        # fobj.LOGIN = request.session['lid']
        fobj.save()
        return HttpResponse('''<script>alert('Edited Successfully');window.location="/myapp/Fuelstation_view_profile/"</script>''')

def add_staff(request):
    return render(request,'Fuel station/add staff FS.html')

def addstaff_post(request):
    name = request.POST['textfield11']
    photo = request.FILES['fileField']
    email = request.POST['textfield10']
    phone = request.POST['textfield9']
    place = request.POST['textfield8']
    longtitude = request.POST['textfield3']
    latitude = request.POST['textfield7']
    state = request.POST['textfield6']
    city = request.POST['textfield5']
    pin = request.POST['textfield4']

    fs = FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
    fs.save(date, photo)
    path = fs.url(date)

    obj=Staff()
    obj.name=name
    obj.photo=path
    obj.email=email
    obj.phone=phone
    obj.place=place
    obj.longtitude=longtitude
    obj.latitude=latitude
    obj.state=state
    obj.city=city
    obj.pin=pin
    obj.FUELSTATION=FuelStation.objects.get(LOGIN_id=request.session['lid'])
    obj.save()

    return HttpResponse('''<script>alert('staff added successfully');window.location="/myapp/Fuelstation_home/"</script>''')


def edit_staff(request,id):

    s=Staff.objects.get(id=id)
    return render(request,'Fuel station/Edit staff.html',{'data':s})

def editstaff_post(request):
    name = request.POST['textfield11']
    photo = request.POST['fileField']
    email = request.POST['textfield10']
    phone = request.POST['textfield9']
    place = request.POST['textfield8']
    longtitude = request.POST['textfield3']
    latitude = request.POST['textfield7']
    state = request.POST['textfield6']
    city = request.POST['textfield5']
    pin = request.POST['textfield4']
    return HttpResponse('''<script>alert('staff edited successfully');window.location="/myapp/Fuelstation_home/"</script>''')




def view_staff(request):
    a=Staff.objects.filter(FUELSTATION__LOGIN_id=request.session['lid'])
    return render(request,'Fuel station/view staff.html',{'data':a})

def view_staff_post(request):
    search=request.POST['textfield']
    a=FuelStation.objects.filter(name__icontains=search)
    return render(request,'Fuel station/view staff.html',{'data':a})

def add_stock(request):
    return render(request,'Fuel station/add stock.html')

def addstock_post(request):
    Fuel=request.POST['textfield']
    Stocks=request.POST['textfield2']
    date=datetime.now()

    s=Stock()
    s.date=date
    s.stock=Stocks
    s.fuel=Fuel
    s.FUELSTATION= FuelStation.objects.get(LOGIN_id=request.session['lid'])
    s.save()





    return HttpResponse('''<script>alert('Stock added successfully');window.location="/myapp/Fuelstation_home/"</script>''')

def edit_stock(request,id):

    s=Stock.objects.get(id=id)
    return render(request,'Fuel station/EDIT STOCK.html',{'data':s})

def editstock_post(request):
    Fuel = request.POST['textfield']
    Stocks = request.POST['textfield2']
    id = request.POST['id']

    s=Stock.objects.get(id=id)
    s.fuel=Fuel
    s.stock=Stocks
    s.save()


    return HttpResponse('''<script>alert('Stock Edited successfully');window.location="/myapp/Fuelstation_view_stock/"</script>''')


def view_stock(request):
    a=Stock.objects.filter(FUELSTATION__LOGIN_id= request.session['lid'])
    return render(request,'Fuel station/View stock.html',{'data':a})

def view_stock_post(request):
    fromdate=request.POST['textfield']
    todate=request.POST['textfield2']
    a=Stock.objects.filter(date__range=[fromdate,todate])
    return render(request,'Fuel station/View stock.html',{'data':a})

def delete_stock(request,id):
    Stock.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Stock Deleted successfully');window.location="/myapp/Fuelstation_view_stock/"</script>''')

def delete_staff(request,id):
    Staff.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('Stock Delelted successfully');window.location="/myapp/Fuelstation_view_staff/"</script>''')

def fuel_send_req(request):
    lid=request.POST['lid']
    sid=request.POST['sid']

    s=Fuelrequest()
    s.USER=User.objects.get(LOGIN_id=lid)
    s.STOCK_id=sid
    s.status="pending"
    s.date=datetime.now()
    s.save()
    return JsonResponse({"status": "ok"})

def user_view_fuel_Req_status(request):
    lid=request.POST['lid']
    print(lid)
    s=Fuelrequest.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in s:
        l.append({"id": i.id,
                  "date": i.date,
                  "rstatus": i.status,
                  "fuelname": i.STOCK.fuel,
                  "fuelstationame": i.STOCK.FUELSTATION.name,
                  })
    print(l)
    return JsonResponse({"status": "ok","data": l})




def view_request_to_staff(request):

    a=Fuelrequest.objects.all()

    return render(request,'Fuel station/View req user to staff.html',{'data':a})

def allocation(request,id):
    s=Staff.objects.filter(FUELSTATION__LOGIN_id= request.session['lid'])
    return render(request,'Fuel station/Allocarion.html',{'data':s,'id':id})

def allocation_post(request):
    Staff=request.POST['textfield']
    id=request.POST['id']

    a=Allocate()
    a.STAFF_id=Staff
    a.FUELREQUEST_id=id
    a.date=datetime.now()
    a.save()

    return HttpResponse('''<script>alert('Allocated successfully');window.location="/myapp/Fuelstation_home/"</script>''')

def view_allocation(request):
    a=Allocate.objects.filter(FUELREQUEST__STOCK__FUELSTATION__LOGIN_id= request.session['lid'])
    return render(request,'Fuel station/view allocated.html',{'data':a})

def view_allocation_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']


    a = Allocate.objects.filter(FUELREQUEST__FuelStation__LOGIN_id=request.session['lid'],date__range=[fromdate,todate])
    return render(request, 'Fuel station/view allocated.html', {'data': a})
def payment(request):
    return render(request,'Fuel station/view payment FS.html')

def home_EV(request):
    return render(request,'EV station/homeindex.html')

#========================EV====
def signup_EV(request):
    return render(request,'evsignupindex.html')

def signupEV_post(request):
    name = request.POST['textfield']
    photo = request.FILES['textfield2']
    email = request.POST['textfield3']
    phone = request.POST['textfield4']
    place = request.POST['textfield5']
    longtitude = request.POST['textfield6']
    latitude = request.POST['textfield7']
    state = request.POST['textfield8']
    city = request.POST['textfield9']
    pin = request.POST['textfield10']
    password = request.POST['textfield13']
    confirmpassword = request.POST['textfield14']

    ev= FileSystemStorage()
    date = datetime.now().strftime('%Y%m%d%H%M%S') + 'jpg'
    ev.save(date, photo)
    path = ev.url(date)

    lobj = Login()
    lobj.username = email
    lobj.password = confirmpassword
    lobj.type = 'pending'
    lobj.save()

    fobj = evstation()
    fobj.name = name
    fobj.photo = path
    fobj.email = email
    fobj.phone = phone
    fobj.place = place
    fobj.longtitude = longtitude
    fobj.latitude = latitude
    fobj.state = state
    fobj.city = city
    fobj.pin = pin
    fobj.password = password
    fobj.confirmpassword = confirmpassword
    fobj.LOGIN = lobj
    fobj.status = 'pending'
    fobj.save()

    return HttpResponse('''<script>alert('You are signed ');window.location="/myapp/login/"</script>''')

def edit_EV(request):
    a = evstation.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'EV station/Edit profile.html',{"data":a})

def editEV_post(request):
    name = request.POST['textfield11']
    photo = request.POST['fileField']
    email = request.POST['textfield10']
    phone = request.POST['textfield9']
    place = request.POST['textfield8']
    longtitude = request.POST['textfield3']
    latitude = request.POST['textfield7']
    state = request.POST['textfield6']
    city = request.POST['textfield5']
    pin = request.POST['textfield4']
    fobj = evstation.objects.get(LOGIN_id=request.session['lid'])

    if 'fileField' in request.FILES:
        photo = request.FILES['fileField']
        fs = FileSystemStorage()
        date = datetime.now().strftime('%Y%m%d%H%M%S') + '.jpg'
        fs.save(date, photo)
        path = fs.url(date)
        fobj.photo = path
        fobj.save()
    fobj.name = name
    fobj.email = email
    fobj.phone = phone
    fobj.place = place
    fobj.longtitude = longtitude
    fobj.latitude = latitude
    fobj.state = state
    fobj.city = city
    fobj.pin = pin
    # fobj.LOGIN = request.session['lid']
    fobj.save()
    return HttpResponse('''<script>alert('profile changed successfully');window.location="/myapp/view_profile_EV/"</script>''')


def view_profile_EV(request):
    b = evstation.objects.get(LOGIN_id=request.session['lid'])
    return render(request,'EV station/view profile EV.html',{'i':b})

def passwordEV_change(request):
    return render(request,'EV station/change password ev.html')

def passwordEV_post(request):
    oldpassword=request.POST['textfield']
    newpassword=request.POST['textfield2']
    confirmpassword=request.POST['textfield3']
    id = request.session['lid']
    chp = Login.objects.get(id=id)
    if chp.password == oldpassword:
        if newpassword == confirmpassword:
            Login.objects.filter(id=id).update(password=newpassword)
            return HttpResponse(
                '''<script>alert('password changed successfully');window.location="/myapp/login/"</script>''')
        else:
            return HttpResponse(
                '''<script>alert('User not found');window.location="/myapp/EVstation_passwordEV_change/"</script>''')
    else:
        return HttpResponse('''<script>alert('you must login first');window.location="/myapp/login/"</script>''')


def view_payment_EV(request):
    b = evpayment.objects.filter(BOOKING__SLOT__EVSTATION__LOGIN_id=request.session['lid'])
    return render(request,'EV station/view payment EV.html',{'data':b})

def view_payment_EV_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    b = evpayment.objects.filter(BOOKING__SLOT__EVSTATION__LOGIN_id=request.session['lid'],date__range=[fromdate,todate])
    return render(request,'EV station/view payment EV.html',{'data':b})

def add_slot(request):
    return render(request,'EV station/Slot EV.html')

def addslot_post(request):
    slotno=request.POST['textfield']

    s= Slot()
    s.slotno=slotno
    s.amount='300'
    s.EVSTATION=evstation.objects.get(LOGIN_id=request.session['lid'])
    s.save()
    return HttpResponse('''<script>alert('Slot Added ');window.location="/myapp/EVstation_view_slot/"</script>''')



def edit_slot(request,id):
    a=Slot.objects.get(id=id)
    return render(request,'EV station/EDIT Slot EV.html',{'data':a})

def editslot_post(request):
    slot=request.POST['textfield']
    id = request.POST['id']

    s = Slot.objects.get(id=id)
    s.slotno = slot
    s.EVSTATION = evstation.objects.get(LOGIN_id=request.session['lid'])
    s.save()
    return HttpResponse('''<script>alert('Slot Edited ');window.location="/myapp/EVstation_view_slot/"</script>''')

def delete_slot(request,id):
    a=Slot.objects.get(id=id).delete()
    return HttpResponse('''<script>alert('slot is removed');window.location="/myapp/EVstation_view_slot/"</script>''')

def view_slot(request):
    b = Slot.objects.filter(EVSTATION__LOGIN_id=request.session['lid'])
    return render(request,'EV station/View slot EV.html',{'data':b})




def view_slot_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    b = evstation.objects.filter(date__range=[fromdate,todate])
    return render(request,'EV station/View slot EV.html',{'data':b})


def view_booking(request):
    b = Booking.objects.filter(SLOT__EVSTATION__LOGIN_id=request.session['lid'])
    return render(request, 'EV station/View booking EV.html', {'data': b})

def view_booking_post(request):
    fromdate = request.POST['textfield']
    todate = request.POST['textfield2']
    b = Booking.objects.filter(SLOT__EVSTATION__LOGIN_id=request.session['lid'],date__range=[fromdate,todate])
    return render(request, 'EV station/View booking EV.html', {'data': b})


# worker


def flut_login_post(request):
    username=request.POST['name']
    password=request.POST['password']
    print(username,password)
    log=Login.objects.filter(username=username,password=password)
    if log.exists():
        log1 = Login.objects.get(username=username, password=password)
        lid= log1.id
        if log1.type=="worker":
            return JsonResponse({"status":"ok",'lid':str(lid),"type":"worker"})
        elif log1.type=="user":
            return JsonResponse({"status": "ok",'lid':str(lid),"type":"user"})
        else:
            return JsonResponse({"status": "no",})
    else:
        return JsonResponse({"status": "no",})


def signup_worker(request):
    return render(request,'Worker station/WORKER sign up.html')

def signupwrk_post(request):
    name = request.POST['name']
    photo = request.POST['photo']
    email = request.POST['em']
    phone = request.POST['phn']
    place = request.POST['plc']
    # longtitude = request.POST['textfield6']
    # latitude = request.POST['textfield7']
    state = request.POST['state']
    city = request.POST['city']
    pin = request.POST['pin']
    password = request.POST['pwd']
    confirmpassword = request.POST['cpwd']

    if password==confirmpassword:

        lg=Login()
        lg.username=email
        lg.password=confirmpassword
        lg.type="pending"
        lg.save()

        decode=base64.b64decode(photo)
        date=datetime.now().strftime("%Y%m%d-%H%M%S")+".jpg"
        fs=open("C:\\Users\\ramseena\\PycharmProjects\\roadmate\\media\\worker\\"+date,"wb")
        path="/media/worker/"+date
        fs.write(decode)
        fs.close()

        w=Worker()
        w.name=name
        w.photo=path
        w.email=email
        w.phone=phone
        w.place=place
        w.latitude="pending"
        w.longtitude="pending"
        w.state=state
        w.city=city
        w.pin=pin
        w.status="pending"
        w.LOGIN=lg
        w.save()
    return JsonResponse({"status":"ok"})

def view_profile_wrkr(request):
    lid=request.POST['lid']
    c = Worker.objects.get(LOGIN_id=lid)
    return JsonResponse({"status":"ok",
                         "name":c.name,
                         "photo":c.photo,
                         "email":c.email,
                         "phone":c.phone,
                         "place":c.place,
                         "latitude":c.latitude,
                         "longtitude":c.longtitude,
                         "state":c.state,
                         "city":c.city,
                         "pin":c.pin,
                         "Wstatus":c.status,
                         "lid":c.LOGIN_id})

def edit_profile_wrkr(request):
    return render(request,'Worker station/worker edit.html')

def editprofilewrk_post(request):
    name = request.POST['name']
    photo = request.POST['photo']
    email = request.POST['em']
    phone = request.POST['phn']
    place = request.POST['plc']
    # longtitude = request.POST['textfield6']
    # latitude = request.POST['textfield7']
    state = request.POST['state']
    city = request.POST['city']
    pin = request.POST['pin']
    lid=request.POST['lid']
    w = Worker.objects.get(LOGIN_id=lid)
    if len(photo)>200:
        decode = base64.b64decode(photo)
        date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        fs = open("C:\\Users\\ramseena\\PycharmProjects\\roadmate\\media\\worker\\" + date, "wb")
        path = "/media/worker/" + date
        fs.write(decode)
        fs.close()
        w.photo = path
    w.name = name
    w.email = email
    w.phone = phone
    w.place = place
    w.latitude = "pending"
    w.longtitude = "pending"
    w.state = state
    w.city = city
    w.pin = pin
    w.status = "pending"
    w.save()
    return JsonResponse({"status": "ok"})



def passwordwrkr_post(request):
    oldpassword = request.POST['cp']
    newpassword = request.POST['np']
    confirmpassword = request.POST['c_p']
    id = request.POST['lid']
    chp = Login.objects.get(id=id)
    if chp.password == oldpassword:
        if newpassword == confirmpassword:
            Login.objects.filter(id=id).update(password=newpassword)
            return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"no"})
    else:
        return JsonResponse({"status": "no"})


def view_service(request):
    lid=request.POST['lid']
    c = Workwrservice.objects.filter(WORKER__LOGIN_id=lid)
    l=[]
    for i in c:
        l.append({"id":i.id,
                  "servicename":i.servicename,
                  "serviceamount":i.serviceamount,
                  "description":i.description,})
    return JsonResponse({"status":"ok","data":l})


def add_service(request):
    return render(request,'Worker station/add service wrkr.html')

def addservice_post(request):
    servicename=request.POST['sn']
    serviceamount=request.POST['sa']
    description=request.POST['d']
    lid=request.POST['lid']
    w=Workwrservice()
    w.servicename=servicename
    w.serviceamount=serviceamount
    w.description=description
    w.WORKER=Worker.objects.get(LOGIN_id=lid)
    w.save()
    return JsonResponse({"status":"ok"})

def edit_service(request):
    id = request.POST['id']
    c = Workwrservice.objects.get(id=id)
    print(c)
    return JsonResponse({"status": "ok",
                         "id": c.id,
                  "servicename": c.servicename,
                  "serviceamount": c.serviceamount,
                  "description": c.description, })

def editservice_post(request):
    servicename=request.POST['sn']
    serviceamount=request.POST['sa']
    description=request.POST['d']
    id = request.POST['id']
    w = Workwrservice.objects.get(id=id)
    w.servicename = servicename
    w.serviceamount = serviceamount
    w.description = description
    w.save()
    return JsonResponse({"status": "ok"})

def delete_service(request):
    sid=request.POST['sid']
    Workwrservice.objects.filter(id=sid).delete()
    return JsonResponse({"status": "ok"})



def worker_view_service_req(request):
    lid=request.POST['lid']
    print(lid)
    s=Servicerequest.objects.filter(SERVICE__WORKER__LOGIN_id=lid,status="pending")
    l = []
    for i in s:
        l.append({"id": i.id,
                  "date": i.date,
                  "status": i.status,
                  "name": i.USER.name,
                  "email": i.USER.email,
                  "phone": i.USER.phone,
                  "place": i.USER.place,
                  "latitude": i.USER.latitude,
                  "longtitude": i.USER.longtitude,
                  "state": i.USER.state,
                  "city": i.USER.city,
                  "pin": i.USER.pin,
                  "servicename": i.SERVICE.servicename,
                  "serviceamount": i.SERVICE.serviceamount,
                  "description": i.SERVICE.description,
                  })
    print(l)
    return JsonResponse({"status": "ok", "data": l})


def approve_service_req(request):
    sid = request.POST['sid']
    Servicerequest.objects.filter(id=sid).update(status="approved")
    return JsonResponse({"status": "ok"})

def reject_service_req(request):
    sid = request.POST['sid']
    Servicerequest.objects.filter(id=sid).update(status="rejected")
    return JsonResponse({"status": "ok"})

def wrkr_view_approved_req(request):
    lid = request.POST['lid']
    s = Servicerequest.objects.filter(SERVICE__WORKER__LOGIN_id=lid, status="approved")
    l = []
    for i in s:
        l.append({"id": i.id,
                  "date": i.date,
                  "status": i.status,
                  "name": i.USER.name,
                  "email": i.USER.email,
                  "phone": i.USER.phone,
                  "place": i.USER.place,
                  "state": i.USER.state,
                  "city": i.USER.city,
                  "pin": i.USER.pin,
                  "servicename": i.SERVICE.servicename,
                  "serviceamount": i.SERVICE.serviceamount,
                  "description": i.SERVICE.description,
                  })
    return JsonResponse({"status": "ok", "data": l})


def wrkr_view_rejected_req(request):
     lid = request.POST['lid']
     s = Servicerequest.objects.filter(SERVICE__WORKER__LOGIN_id=lid, status="rejected")
     l = []
     for i in s:
         l.append({"id": i.id,
                   "date": i.date,
                   "status": i.status,
                   "name": i.USER.name,
                   "email": i.USER.email,
                   "phone": i.USER.phone,
                   "place": i.USER.place,
                   "latitude": i.USER.latitude,
                   "longtitude": i.USER.longtitude,
                   "state": i.USER.state,
                   "city": i.USER.city,
                   "pin": i.USER.pin,
                   "servicename": i.SERVICE.servicename,
                   "serviceamount": i.SERVICE.serviceamount,
                   "description": i.SERVICE.description,
                   })
     return JsonResponse({"status": "ok", "data": l})

def user_wrkr_payment(request):
    lid = request.POST['lid']
    pay=request.POST["pay"]
    servicerequest=request.POST["sid"]

    print(lid)
    print(servicerequest)
    print(pay)
    print("riss")



    c=Workerpayment()
    c.USER=User.objects.get(LOGIN_id=lid)
    c.payment=pay
    c.SERVICEREQUEST_id=servicerequest
    c.date=datetime.now()
    c.save()

    return JsonResponse({"status": "ok", "data": 1})


def view_payment_wrkr(request):
    lid = request.POST['lid']
    c = Workerpayment.objects.filter(SERVICEREQUEST__SERVICE__WORKER__LOGIN_id=lid)
    l = []
    for i in c:
        l.append({"id": i.id,
                  "date": i.date,
                  "payment": i.payment,
                  "name": i.USER.name,
                  "email": i.USER.email,
                  "phone": i.USER.phone,
                  "place": i.USER.place,
                  "latitude": i.USER.latitude,
                  "longtitude": i.USER.longtitude,
                  "state": i.USER.state,
                  "city": i.USER.city,
                  "pin": i.USER.pin,
                  "servicename": i.SERVICEREQUEST.SERVICE.servicename,
                  "serviceamount": i.SERVICEREQUEST.SERVICE.serviceamount,
                  "description": i.SERVICEREQUEST.SERVICE.description,
                  })
    return JsonResponse({"status": "ok", "data": l})



def wrkr_view_review(request):
    lid = request.POST['lid']
    c = Review.objects.all()
    l = []
    for i in c:
        l.append({"id": i.id,
                  "date": i.date,
                  "review": i.review,
                  "rating": i.rating,
                  "name": i.USER.name,})
    return JsonResponse({"status": "ok", "data": l})


# user



def signupusr_post(request):
    name = request.POST['name']
    photo = request.POST['photo']
    email = request.POST['em']
    phone = request.POST['phn']
    place = request.POST['plc']
    longtitude = request.POST['long']
    latitude = request.POST['lat']
    state = request.POST['state']
    city = request.POST['city']
    pin = request.POST['pin']
    password = request.POST['pwd']
    confirmpassword = request.POST['cpwd']
    if password == confirmpassword:
        lg = Login()
        lg.username = email
        lg.password = confirmpassword
        lg.type = "user"
        lg.save()

        decode = base64.b64decode(photo)
        date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        fs = open("C:\\Users\\ramseena\\PycharmProjects\\roadmate\\media\\user\\" + date, "wb")
        path = "/media/user/" + date
        fs.write(decode)
        fs.close()

        w = User()
        w.name = name
        w.photo = path
        w.email = email
        w.phone = phone
        w.place = place
        w.latitude = latitude
        w.longtitude = longtitude
        w.state = state
        w.city = city
        w.pin = pin
        w.LOGIN = lg
        w.save()
    return JsonResponse({"status": "ok"})


def view_profile_usr(request):
    lid = request.POST['lid']
    c = User.objects.get(LOGIN_id=lid)
    return JsonResponse({"status": "ok",
                         "name": c.name,
                         "photo": c.photo,
                         "email": c.email,
                         "phone": c.phone,
                         "place": c.place,
                         "latitude": c.latitude,
                         "longtitude": c.longtitude,
                         "state": c.state,
                         "city": c.city,
                         "pin": c.pin,
                         "lid": c.LOGIN_id})

# def edit_profile_usr(request):
#     return render(request,'User/Edit profile.html')

def editprofileusr_post(request):
    name = request.POST['name']
    photo = request.POST['photo']
    email = request.POST['em']
    phone = request.POST['phn']
    place = request.POST['plc']
    longtitude = request.POST['longitude']
    latitude = request.POST['latitude']
    state = request.POST['state']
    city = request.POST['city']
    pin = request.POST['pin']
    lid = request.POST['lid']
    w = User.objects.get(LOGIN_id=lid)
    if len(photo)<0:
        decode = base64.b64decode(photo)
        date = datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
        fs = open("C:\\Users\\ramseena\\PycharmProjects\\roadmate\\media\\user\\" + date, "wb")
        path = "/media/user/" + date
        fs.write(decode)
        fs.close()
        w.photo = path
        w.save()
    w.name = name
    w.email = email
    w.phone = phone
    w.place = place
    w.latitude = latitude
    w.longtitude = longtitude
    w.state = state
    w.city = city
    w.pin = pin

    w.save()
    return JsonResponse({"status": "ok"})


# def passwordusr_change(request):
#     return render(request,'change password.html')

def passwordusr_post(request):
    oldpassword = request.POST['cp']
    newpassword = request.POST['np']
    confirmpassword = request.POST['c_p']
    id = request.POST["lid"]
    chp = Login.objects.get(id=id)
    if chp.password == oldpassword:
        if newpassword == confirmpassword:
            Login.objects.filter(id=id).update(password=newpassword)
            return JsonResponse({"status":"ok"})
        else:
            return JsonResponse({"status":"no"})
    else:
        return JsonResponse({"status": "no"})


def view_nearby_fuel_station(request):
    latitude=request.POST['latitude']
    longtitude=request.POST['longtitude']
    b = FuelStation.objects.all()
    l = []
    for i in b:
        l.append({"id": i.id,
                  "name": i.name,
                  "photo": i.photo,
                  "email": i.email,
                  "phone": i.phone,
                  "place": i.place,
                  "latitude": i.latitude,
                  "longtitude": i.longtitude,
                  "state": i.state,
                  "city": i.city,
                  "pin": i.pin,
                  "status": i.status,
                  })
    return JsonResponse({"status": "ok", "data": l})

def view_slot_user(request):
    eid=request.POST['sid']
    b = Slot.objects.filter(EVSTATION_id=eid)
    l = []
    for i in b:
        l.append({"id": i.id,
                  "slotno": i.slotno,
                  "name": i.EVSTATION.name,
                  # "photo": i.EVSTATION.photo,
                  # "email": i.EVSTATION.email,
                  # "phone": i.EVSTATION.phone,
                  # "place": i.EVSTATION.place,
                  # "latitude": i.EVSTATION.latitude,
                  # "longtitude": i.EVSTATION.longtitude,
                  # "state": i.EVSTATION.state,
                  # "city": i.EVSTATION.city,
                  # "pin": i.EVSTATION.pin,
                  # "status": i.EVSTATION.status,
                  })
    return JsonResponse({"status": "ok", "data": l})


# def view_slot_usr_post(request):
#     lid=request.POST['lid']
#     sid=request.POST['sid']
#
#     b=Booking()
#     b.date=datetime.now().today()
#     b.USER=User.objects.get(LOGIN_id=lid)
#     b.SLOT_id=sid
#     b.save()
#     return JsonResponse({"status":"ok"})


def stock_usr(request):
    lid = request.POST['lid']
    sid = request.POST['sid']
    fuel = request.POST['sid']

    c = Stock()
    c.USER = User.objects.get(LOGIN_id=lid)
    c.STOCK__id=sid
    c.fuel= fuel
    c.date = datetime.now()
    c.save()

    return JsonResponse({"status": "ok"})



def view_stock_usr(request):
    eid = request.POST['sid']
    print(eid,'---------------------------')
    b = Stock.objects.filter(FUELSTATION_id=eid)
    l = []
    for i in b:
        l.append({"id": i.id,
                  "stock": i.stock,
                  "fuel": i.fuel,
                  "name": i.FUELSTATION.name,
                  })
    print(l)
    return JsonResponse({"status": "ok", "data": l})


def view_EV_usr(request):
    d = User.objects.all()
    return render(request,'User/VIEW EV STATION USER.html',{'data':d})

def slot_usr(request):
    return render(request,'User/SLOT USER.html')

def booking_usr(request):
    lid = request.POST['lid']
    sid = request.POST['sid']

    c = Booking()
    c.USER = User.objects.get(LOGIN_id=lid)
    c.SLOT_id=sid
    c.date = datetime.now()
    c.save()

    return JsonResponse({"status": "ok"})

def view_book_user(request):
    lid=request.POST['lid']
    b = Booking.objects.filter(USER__LOGIN__id=lid)
    l = []
    for i in b:
        l.append({"id": i.id,
                  "date": i.date,
                  "slot": i.SLOT.slotno,
                  "Evstationname": i.SLOT.EVSTATION.name,
                  "evid": i.SLOT.EVSTATION.id,

                  # "photo": i.EVSTATION.photo,
                  # "email": i.EVSTATION.email,
                  # "phone": i.EVSTATION.phone,
                  # "place": i.EVSTATION.place,
                  # "latitude": i.EVSTATION.latitude,
                  # "longtitude": i.EVSTATION.longtitude,
                  # "state": i.EVSTATION.state,
                  # "city": i.EVSTATION.city,
                  # "pin": i.EVSTATION.pin,
                  # "status": i.EVSTATION.status,
                  })


    return JsonResponse({"status": "ok", "data": l})





def history_usr(request):
        lid = request.POST['lid']
        b = Booking.objects.filter(USER__LOGIN__id=lid)
        l = []
        for i in b:
            l.append({"id": i.id,
                      "date": i.date,
                      "slot": i.SLOT.slotno,
                      "Evstationname": i.SLOT.EVSTATION.name,
                      })
        print(l)
        return JsonResponse({"status": "ok", "data": l})


def usr_view_previous_bookings(request):
    lid = request.POST['lid']
    b = Booking.objects.filter(date__lt=datetime.now().today(),USER__LOGIN=lid)
    print(b)
    l = []
    for i in b:
        l.append({"id": i.id,
                  "date": i.date,
                  "slot": i.SLOT.slotno,
                  "Evstationname": i.SLOT.EVSTATION.name,
                  })
    print(l)
    return JsonResponse({"status": "ok", "data": l})


# def view_payment_usr(request):
#     d = payment.objects.all()
#     return render(request,'User/VIEW PAYMENT USER.html')

def user_send_complaint(request):
    lid = request.POST['lid']
    cc=request.POST["complaint"]

    c=Complaint()
    c.complaint=cc
    c.USER=User.objects.get(LOGIN_id=lid)
    c.status="pending"
    c.reply="pending"
    c.date=datetime.now()
    c.save()

    return JsonResponse({"status": "ok"})


def user_view_complaint(request):
    lid=request.POST['lid']
    print(lid)
    s=Complaint.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in s:
        l.append({"id": i.id,
                  "date": i.date,
                  "complaint": i.complaint,
                  "reply": i.reply,
                  "status": i.status,
                  })
    print(l)
    return JsonResponse({"status": "ok","data": l})




def user_send_review(request):
    lid = request.POST['lid']
    reviews= request.POST["review"]
    rating = request.POST["rating"]

    r=Review()
    r.review=reviews
    r.USER=User.objects.get(LOGIN_id=lid)
    r.date=datetime.now()

    r.rating=rating
    r.save()

    return JsonResponse({"status": "ok"})
















def user_view_worker(request):

    s=Worker.objects.all()
    l = []
    for i in s:
        l.append({"id": i.id,
                  "name": i.name,
                  "photo": i.photo,
                  "email": i.email,
                  "phone": i.phone,
                  "place": i.place,
                  "latitude": i.latitude,
                  "longtitude": i.longtitude,
                  "state": i.state,
                  "city": i.city,
                  "pin": i.pin,

                  })
    print(l)
    return JsonResponse({"status": "ok","data": l})


def user_view_fuelstation(request):
    s = FuelStation.objects.all()
    l = []
    for i in s:
        l.append({"id": i.id,
                  "name": i.name,
                  "photo": i.photo,
                  "email": i.email,
                  "phone": i.phone,
                  "place": i.place,
                  "latitude": i.latitude,
                  "longtitude": i.longtitude,
                  "state": i.state,
                  "city": i.city,
                  "pin": i.pin,

                  })
    print(l)
    return JsonResponse({"status": "ok", "data": l})


def user_view_evstation(request):
    s = evstation.objects.all()
    l = []
    for i in s:
        l.append({"id": i.id,
                  "name": i.name,
                  "photo": i.photo,
                  "email": i.email,
                  "phone": i.phone,
                  "place": i.place,
                  "latitude": i.latitude,
                  "longtitude": i.longtitude,
                  "state": i.state,
                  "city": i.city,
                  "pin": i.pin,

                  })
    print(l)
    return JsonResponse({"status": "ok", "data": l})





def user_view_stock(request):
    fid=request.POST['sid']
    c = Stock.objects.filter(FUELSTATION__id=fid)
    l=[]
    for i in c:
        l.append({"id":i.id,

                  "stock":i.stock,
                  "fuel":i.fuel,})
    return JsonResponse({"status":"ok","data":l})




def user_send_wrokreq(request):
    lid=request.POST['lid']
    serviceid=request.POST['sid']

    s=Servicerequest()
    s.SERVICE_id=serviceid
    s.USER=User.objects.get(LOGIN_id=lid)
    s.status="pending"
    s.date=datetime.now()
    s.save()
    return JsonResponse({"status": "ok"})




def user_view_service(request):
    wid=request.POST['wid']
    c = Workwrservice.objects.filter(WORKER_id=wid)
    l=[]
    for i in c:
        l.append({"id": i.id,
                  "servicename": i.servicename,
                  "serviceamount": i.serviceamount,
                  "description": i.description, })
    return JsonResponse({"status":"ok","data":l})


def user_view_Req_service(request):
    lid=request.POST['lid']
    print(lid)
    s=Servicerequest.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in s:
        l.append({"id": i.id,
                  "date": i.date,
                  "rstatus": i.status,
                  "servicename": i.SERVICE.servicename,
                  "serviceamount": i.SERVICE.serviceamount,
                  "description": i.SERVICE.description,
                  })
    print(l)
    return JsonResponse({"status": "ok","data": l})

def user_send_evreq(request):
    lid=request.POST['lid']
    eid=request.POST['eid']
    bid=request.POST['bid']

    s=evrequest()
    s.USER=User.objects.get(LOGIN_id=lid)
    s.evstation_id=eid
    s.BOOKING_id=bid
    s.date=datetime.now().today()
    s.save()
    return JsonResponse({"status": "ok"})


def user_view_Req_slot(request):
    lid=request.POST['lid']
    print(lid)
    s=evrequest.objects.filter(USER__LOGIN_id=lid)
    l = []
    for i in s:
        l.append({"id": i.BOOKING.id,
                  "date": i.date,
                  "slotno": i.BOOKING.SLOT.slotno,
                  "evstationame":i.evstation.name,
                  "evid":i.evstation.id,
                  "amount":"300",

                })
    print(l)
    return JsonResponse({"status": "ok","data": l})

# def view_payment_wrkr_history(request):
#     lid = request.POST['lid']
#     print(lid,'lllllllllll')
#     c = Workerpayment.objects.filter(USER__LOGIN_id=lid)
#     l = []
#     for i in c:
#         l.append({"id": i.id,
#                   "date": i.date,
#                   "payment": i.payment,
#                   "phone": i.SERVICEREQUEST.SERVICE.WORKER.phone,
#                   "place": i.SERVICEREQUEST.SERVICE.WORKER.place,
#                   "latitude": i.SERVICEREQUEST.SERVICE.WORKER.latitude,
#                   "longtitude": i.SERVICEREQUEST.SERVICE.WORKER.longtitude,
#                   "state": i.SERVICEREQUEST.SERVICE.WORKER.state,
#                   "city": i.SERVICEREQUEST.SERVICE.WORKER.city,
#                   "pin": i.SERVICEREQUEST.SERVICE.WORKER.pin,
#                   "servicename": i.SERVICEREQUEST.servicename,
#                   "serviceamount": i.SERVICEREQUEST.serviceamount,
#                   "description": i.SERVICEREQUEST.description,
#                   })
#         print(l,'aaaaaaaaaa')
#     return JsonResponse({"status": "ok", "data": l})


from django.http import JsonResponse
from myapp.models import Workerpayment


def view_payment_wrkr_history(request):
    lid = request.POST['lid']
    print(lid, 'lllllllllll')
    c = Workerpayment.objects.select_related(
        'SERVICEREQUEST', 'SERVICEREQUEST__SERVICE', 'SERVICEREQUEST__SERVICE__WORKER'
    ).filter(USER__LOGIN_id=lid)

    l = []
    for i in c:
        if i.SERVICEREQUEST:
            worker = i.SERVICEREQUEST.SERVICE.WORKER
            l.append({
                "id": i.id,
                "date": i.date,
                "payment": i.payment,
                "phone": worker.phone,
                "place": worker.place,
                "latitude": worker.latitude,
                "longtitude": worker.longtitude,
                "state": worker.state,
                "city": worker.city,
                "pin": worker.pin,
                "servicename": i.SERVICEREQUEST.SERVICE.servicename,
                "serviceamount": i.SERVICEREQUEST.SERVICE.serviceamount,
                "description": i.SERVICEREQUEST.SERVICE.description,
            })
        else:
            l.append({
                "id": i.id,
                "date": i.date,
                "payment": i.payment,
                "servicename": None,
                "serviceamount": None,
                "description": None,
                "phone": None,
                "place": None,
                "latitude": None,
                "longtitude": None,
                "state": None,
                "city": None,
                "pin": None,
            })
    return JsonResponse({"status": "ok", "data": l})

def view_payment_ev_history(request):
    lid = request.POST['lid']
    print(lid, 'lllllllllll')
    c = evpayment.objects.filter(USER__LOGIN_id=lid)

    l = []
    for i in c:
            l.append({
                "id": i.id,
                "date": i.date,
                "payment": i.payment,
                "slotno":i.BOOKING.SLOT.slotno,
                "amount":i.BOOKING.SLOT.amount,
                "name": i.BOOKING.SLOT.EVSTATION.name,
                "phone": i.BOOKING.SLOT.EVSTATION.phone,
                "place": i.BOOKING.SLOT.EVSTATION.place,
                "latitude":  i.BOOKING.SLOT.EVSTATION.latitude,
                "longtitude": i.BOOKING.SLOT.EVSTATION.longtitude,
                "state": i.BOOKING.SLOT.EVSTATION.state,
                "city": i.BOOKING.SLOT.EVSTATION.city,
                "pin": i.BOOKING.SLOT.EVSTATION.pin,
            })
    return JsonResponse({"status": "ok", "data": l})


def user_ev_payment(request):
    lid = request.POST['lid']
    pay=request.POST["pay"]
    bid=request.POST["bid"]

    print(lid)
    print(pay)
    print("riss")



    c=evpayment()
    c.USER=User.objects.get(LOGIN_id=lid)
    c.payment=pay
    c.BOOKING_id=bid
    c.date=datetime.now()
    c.save()

    return JsonResponse({"status": "ok", "data": 1})

def add_reminder(request):
    lid = request.POST['lid']
    date = request.POST["date"]
    reminder = request.POST["reminder"]

    c = Reminder()
    c.name= reminder
    c.USER = User.objects.get(LOGIN_id=lid)
    c.date = datetime.now()
    c.save()

    return JsonResponse({"status": "ok"})

def user_view_reminder(request):
    lid=request.POST['lid']
    c = Reminder.objects.filter(USER__LOGIN_id=lid)
    l=[]
    for i in c:
        l.append({"id": i.id,
                  "date": i.date.split(' ')[0],
                  "reminder": i.name,
                   })
        print(l)
    return JsonResponse({"status":"ok","data":l})


from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

# Replace with your actual API key
GOOGLE_API_KEY = 'AIzaSyC5d0IaxP3O4VmaibaivTKRm98DyPqos2I  '
genai.configure(api_key=GOOGLE_API_KEY)

model = None
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
        model = genai.GenerativeModel('gemini-1.5-flash')
        break

def generate_gemini_response(prompt):
    # Directly use the user's question as the prompt
    response = model.generate_content(prompt)
    return response.text


@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user_message = json.loads(request.body).get('message')
        # Generate a response based on the user message without additional context
        gemini_response = generate_gemini_response(user_message)
        return JsonResponse({'response': gemini_response})

def petrolpriceprediction(request):
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    import matplotlib.pyplot as plt

    # Step 2: Data Loading
    data = pd.read_csv(r'C:\Users\ramseena\PycharmProjects\roadmate\fuel_prices.csv')  # Replace with your file path

    data = data.values[:, 1]

    X = []
    y = []

    for i in range(3, len(data)):  # Start from index 3 so that we have enough previous data
        # Features: Prices of the previous 3 days
        X.append(data[i - 3:i])
        # Target: Next day's petrol price
        y.append(data[i])

    # Convert lists to numpy arrays for training


    # Step 4: Train-test split
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 5: Train the Random Forest Model
    model = RandomForestRegressor(n_estimators=100, random_state=42)  # 100 trees, can adjust
    model.fit(X_train, y_train)

    datas = data[len(data) - 3:]
    print(datas)

    # Step 6: Predictions
    y_pred = model.predict([datas])

    print(y_pred[0])


    return  JsonResponse(
        {
            'status':'ok',
            'data':y_pred[0]
        }
    )



