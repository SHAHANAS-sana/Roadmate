from django.db import models

# Create your models here.

class Login(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=40)
    type=models.CharField(max_length=30)

class User(models.Model):
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    latitude = models.CharField(max_length=60)
    longtitude = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

class FuelStation(models.Model):
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    latitude = models.CharField(max_length=60)
    longtitude = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    status=models.CharField(max_length=100)
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class evstation(models.Model):
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    latitude = models.CharField(max_length=60)
    longtitude = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    status = models.CharField(max_length=10,default="pending")
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)

class Slot(models.Model):
    amount=models.BigIntegerField()
    slotno=models.CharField(max_length=100)
    EVSTATION = models.ForeignKey(evstation,on_delete=models.CASCADE)

class Complaint(models.Model):
    date=models.DateField()
    complaint=models.CharField(max_length=400)
    reply=models.CharField(max_length=400)
    status = models.CharField(max_length=10,default="pending")
    USER=models.ForeignKey(User,on_delete=models.CASCADE)

class Review(models.Model):
    date=models.DateField()
    review=models.CharField(max_length=500)
    rating=models.CharField(max_length=50,default='')
    USER=models.ForeignKey(User,on_delete=models.CASCADE)

class Staff(models.Model):
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    latitude = models.CharField(max_length=60)
    longtitude = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    FUELSTATION=models.ForeignKey(FuelStation,on_delete=models.CASCADE)

class Stock(models.Model):
    date = models.DateField()
    stock=models.FloatField()
    fuel=models.CharField(max_length=400)
    FUELSTATION=models.ForeignKey(FuelStation,on_delete=models.CASCADE)

class Worker(models.Model):
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=300)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    place = models.CharField(max_length=100)
    latitude = models.CharField(max_length=60)
    longtitude = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    status = models.CharField(max_length=25)
    LOGIN = models.ForeignKey(Login, on_delete=models.CASCADE)

class Workwrservice(models.Model):
    servicename=models.CharField(max_length=100)
    serviceamount=models.CharField(max_length=500)
    description=models.CharField(max_length=500)
    WORKER=models.ForeignKey(Worker,on_delete=models.CASCADE)

class Servicerequest(models.Model):
    date=models.DateField()
    status=models.CharField(max_length=400)
    USER=models.ForeignKey(User,on_delete=models.CASCADE)
    SERVICE=models.ForeignKey(Workwrservice,on_delete=models.CASCADE)

class Fuelrequest(models.Model):
    date=models.DateField()
    status=models.CharField(max_length=10,default="pending")
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    STOCK=models.ForeignKey(Stock,on_delete=models.CASCADE)


class Allocate(models.Model):
    date=models.DateField()
    STAFF=models.ForeignKey(Staff,on_delete=models.CASCADE)
    FUELREQUEST=models.ForeignKey(Fuelrequest,on_delete=models.CASCADE)

class Booking(models.Model):
    date=models.DateField()
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    SLOT=models.ForeignKey(Slot,on_delete=models.CASCADE)

class evrequest(models.Model):
    date=models.DateField()
    USER = models.ForeignKey(User, on_delete=models.CASCADE)
    BOOKING=models.ForeignKey(Booking,on_delete=models.CASCADE,default='')
    evstation=models.ForeignKey(evstation,on_delete=models.CASCADE)

class evpayment(models.Model):
    date=models.DateField(max_length=50)
    payment=models.BigIntegerField()
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    BOOKING=models.ForeignKey(Booking,on_delete=models.CASCADE)


class Chargingstation(models.Model):
    name = models.CharField(max_length=50)
    photo = models.CharField(max_length=300)
    place = models.CharField(max_length=100)
    latitude = models.CharField(max_length=60)
    longtitude = models.CharField(max_length=60)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin = models.CharField(max_length=10)
    EVSTATION=models.ForeignKey(evstation,on_delete=models.CASCADE)

class Workerpayment(models.Model):
    date=models.DateField()
    payment = models.BigIntegerField()
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    SERVICEREQUEST=models.ForeignKey(Servicerequest,on_delete=models.CASCADE)

class Reminder(models.Model):
    date=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    USER = models.ForeignKey(User,on_delete=models.CASCADE)

class Fuelpayment(models.Model):
    date=models.DateField()
    payment=models.BigIntegerField()
    USER = models.ForeignKey(User,on_delete=models.CASCADE)
    STOCK=models.ForeignKey(Stock,on_delete=models.CASCADE)











