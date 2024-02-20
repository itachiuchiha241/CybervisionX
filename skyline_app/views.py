from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from skyline_app.models import product, Cart, order
from django.db.models import Q
import random
import razorpay
from django.core.mail import send_mail

# Create your views here.

#  This is About 
def about(request):
    return HttpResponse("This is About Page")



#  This is Edit 
def edit(request,rid):
    print("id to be edited: ",rid)
    return HttpResponse("id to be edited :"+rid)




#  This is  Delete
def delete(request,rid):
    print("id to be deleted: ",rid)
    return HttpResponse("id to be edited :"+rid)




#  This is SimpleVires
class SimpleViews(View):
    def get(self,request):
        return HttpResponse("Hello From Simple View")
    






#   This is  Home
def home(request):
    context={}
    p=product.objects.filter(is_active=True)
    context['products']=p
    return render(request,'index.html',context)




#   This is  Product Details
def product_details(request,pid):
    p=product.objects.filter(id=pid)          
    context={}
    context['products']=p
    return render(request,'product_details.html',context)




#   This is Register 
def register(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        ucpass=request.POST['ucpass']
        context={}
        if uname=="" or upass=="" or ucpass=="":
            context['errmsg']="Fields can not be empty"
            return render(request,'register.html',context)
        elif upass !=ucpass:
            context['errmsg']="Password and Confirm Password didn't match"
            return render(request,'register.html',context)
        else:
            try:
                u=User.objects.create(password=upass,username=uname,email=uname)
                u.set_password(upass)    # Encrypted Format
                u.save()
                context['success']="user created successfully"
                return render(request,'register.html',context)
            except Exception:
                context['errmsg']="User with same username alredy Exist"
                return render(request,'register.html',context)
    else:
        return render(request,'register.html')
    





#    Tthis is User Login
def user_login(request):
    if request.method=='POST':
        uname=request.POST['uname']
        upass=request.POST['upass']
        context={}
        if uname=="" or upass=="":
            context['errmsg']="Fields can not be empty"
            return render(request,'login.html',context)
        else:
            u=authenticate(username=uname,password=upass)
            if u is not None:
                login(request,u)       #Start the Session
                return redirect('/home')
            else:
                context['errmsg']="Invalid username & password"
                return render(request,'login.html',context)
    else:
        return render(request,'login.html')
    



    
#   User Logout
def user_logout(request):
    logout(request)
    return redirect('/home')



#   This is catfilter
def catfilter(request,cv):
    q1=Q(is_active=True)
    q2=Q(cat=cv)
    p=product.objects.filter(q1 & q2)
    context={}
    context['products']=p
    return render(request,'index.html',context)




# This is Sort
def sort(request,sv):         #sv='0'  or  '1'
    if sv == '0':
        col='price'           #ascentive
    else:
        col='-price'           #descentive
    p=product.objects.filter(is_activte=True).order_by(col)
    context={}
    context['products']=p
    return render(request,'index.html',context)



#  This is Range
def range(request):
    min=request.GET['min']
    max=request.GET['max']
    q1=Q(price__gte=min)
    q2=Q(price__lte=max)
    q3=Q(is_active=True)
    p=product.objects.filter(q1 & q2 & q3)
    context={}
    context['products']=p
    return render(request,'index.html',context)




#   This is  Add to cart
def addtocart(request,pid):
    if request.user.is_authenticated:
        userid=request.user.id
        u=User.objects.filter(id=userid)
        print(u[0])
        p=product.objects.filter(id=pid)
        print(p[0])          #project object
        q1=Q(uid=u[0])
        q2=Q(pid=p[0])
        c=Cart.objects.filter(q1 & q2)
        n=len(c)      #  [1 object]
        context={}
        context['products']=p
        if n==1:
            context['msg']="Product Alredy Exist In Cart !!"
        else:
            c=Cart.objects.create(uid=u[0],pid=p[0])
            c.save()
            context['success']="Product Added Successfully In The Cart!!"
        return render(request,'product_details.html',context)
    else:
        return redirect('/login')
    

    

#  This is Views Cart
def viewcart(request):
    if request.user.is_authenticated:
        c=Cart.objects.filter(uid=request.user.id)
        np=len(c)
        s=0
        for x in c:
            s=s+ x.pid.price * x.qty
        print(s)
        context={}
        context['products']=c
        context['total']=s
        context['n']=np
        return render(request,'cart.html',context)
    else:
        return redirect('/login')




# This is Remove
def remove(request,cid):
    c=Cart.objects.filter(id=cid)
    c.delete()
    return redirect('/viewcart')




#   This is Updateqty
def updateqty(request,qv,cid):
    c=Cart.objects.filter(id=cid)
    if qv=='1':
        t=c[0].qty + 1
        c.update(qty=t)
    else:
        if c[0].qty >1:          #1>1=>F
            t=c[0].qty-1
            c.update(qty=t)
    return redirect('/viewcart')



# This is Placehorder
def placeorder(request):
    userid=request.user.id
    c=Cart.objects.filter(uid=userid) 
    oid=random.randrange(1000,9999)
    for x in c:
        o=order.objects.create(order_id=oid,pid=x.pid,uid=x.uid,qty=x.qty)
        o.save()
        x.delete()                 #Delete Record From Cart Table
    orders=order.objects.filter(uid=request.user.id)
    context={}
    context['products']=orders
    np=len(orders)
    s=0
    for x in orders:
        s=s + x.pid.price*x.qty
    context['total']=s
    context['n']=np
    return render(request,'placeorder.html',context)




#   This is Make Payment
def makepayment(request):
    orders=order.objects.filter(uid=request.user.id)
    s=0
    for x in orders:
        s=s+ x.pid.price*x.qty
        oid=x.order_id
    client = razorpay.Client(auth=("rzp_test_RxHmicyvTCmXDC", "8Qwj1hJSId7QkFGOty1NOe1s"))
    data = { "amount": s*100, "currency": "INR", "receipt": oid }
    payment = client.order.create(data=data)
    print(payment)
    context={}
    uname=request.user.username
    context['uname']=uname
    context['data']=payment
    return render(request,'pay.html',context)





#   This is Send mail
def sendusermail(request,uname):
    send_mail(
        "Ekart - order placed successfully",
        "order details are:",
        "roshanipawar456@gmail.com",
        [],
        fail_silently=False,
    )
    return HttpResponse("Mail Send Successfully")