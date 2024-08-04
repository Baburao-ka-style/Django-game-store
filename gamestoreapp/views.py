from django.shortcuts import render, HttpResponse, redirect
from gamestoreapp.models import Product, Cart, Orders, Review
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import get_connection, EmailMessage
from django.conf import settings
import random

# Create your views here.


def index(request):
    
    return render(request, 'home.html')


def createproduct(request):
    
    if request.method == "GET":
        
        return render(request, 'createproduct.html')
    
    else:
        
        name = request.POST['name']
        description = request.POST['description']
        manufacturer = request.POST['manufacturer']
        category = request.POST['category']
        price = request.POST['price']
        image = request.FILES['image']
        
        p = Product.objects.create(name = name, Description = description, manufacturer = manufacturer, category = category, price = price, image = image)
        
        p.save()
        
        return redirect('/')
    
    
def read_products(request):
    
    if request.method == "GET":

        p = Product.objects.all()
        
        context = {}
        
        context['data'] = p
        
        return render(request, 'readproducts.html', context)

    else:
        
        name =request.POST['search']

        prod = Product.objects.get(name = name)
        
        return redirect(f'/readproductdetails/{prod.id}')

def update_products(request, rid):

    if request.method == "GET":
    
        p = Product.objects.filter(id = rid)
        
        context = {}
        
        context['data'] = p

        return render(request, 'updateproducts.html', context)    

    else:
        
        name = request.POST['name']
        description = request.POST['description']
        manufacturer = request.POST['manufacturer']
        category = request.POST['category']
        price = request.POST['price']

        p = Product.objects.filter(id = rid)

        p.update(name = name, Description = description, manufacturer = manufacturer, category = category, price = price)
        
        return redirect('/read_products')
    
def delete(requesst, rid):
    
    e = Product.objects.filter(id = rid)
    
    e.delete()
    
    return redirect('/read_products')

def register_user(request):
    
    if request.method == "GET":
        
        return render(request, 'registeruser.html')
    
    else:
        
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            
            u = User.objects.create(first_name = first_name, last_name = last_name, username = username, email =email)
            
            u.set_password(password)
            
            u.save()

            return redirect('/')
        
        else:
            
            return HttpResponse("Password and Confirm password does not match")
        
def user_login(request):
    
    if request.method == "GET":
        
        return render(request, 'login.html')
    
    else:
        
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        
        if user is not None:
            
            login(request, user)
            
            return redirect('/')
        
        else:
            
            context = {}
            
            context['error'] = 'Password and Username are incorrect'
            
            return render(request, 'login.html', context)
        
def user_logout(request):
    
    logout(request)

    return redirect('/')

@login_required(login_url= 'login')
def create_cart(request, rid):
    
    prod = Product.objects.get(id = rid)
    
    isPresent = Cart.objects.filter(user = request.user, Product = prod).exists()
    
    if isPresent:
        return redirect('/read_cart')
    
    else:
        
        user = User.objects.get(username = request.user)

        total_price = prod.price
        
        c = Cart.objects.create(Product = prod, user = user, quantity = 1, total_price = total_price)
        
        c.save()
        
        return redirect('/read_cart')


@login_required(login_url= 'login')
def read_cart(request):
    
    cart = Cart.objects.filter(user = request.user)
    
    context = {}
    
    context['prod'] = cart
    
    return render(request, 'readcart.html', context)

def delete_cart(request, rid):
    
    cart = Cart.objects.filter(id = rid)
    
    cart.delete()
    
    return redirect('/read_cart')

def update_cart(request, cid, q):
    
    cart = Cart.objects.filter(id = cid)
    
    cart2 = Cart.objects.get(id = cid)

    total_price = cart2.Product.price * int(q)
    
    cart.update(quantity = q, total_price = total_price)
    
    return redirect('/read_cart')

def create_orders(request, rid):
    
    cart = Cart.objects.get(id = rid)

    orders = Orders.objects.create(Product = cart.Product, user = request.user, quantity = cart.quantity, total_price = cart.total_price)

    orders.save()
    
    cart.delete()
    
    return redirect('/read_cart')

def read_orders(request):
    
    orders = Orders.objects.filter(user = request.user)

    context = {}

    context['data'] = orders
    
    return render(request, 'readorders.html', context)

def create_review(request, rid):
    
    if request.method == 'GET':
            
        return render(request, 'createreview.html')

    else:
        
        order = Orders.objects.get(id = rid)

        title = request.POST['title']
        content = request.POST['content']
        rating = request.POST['rate']
        image = request.FILES['image']

        review = Review.objects.create(title = title, content = content, rating = rating, image = image, product = order.Product, user = request.user)
        
        review.save()
        
        return HttpResponse('review saved')
    
def productdetail(request, rid):
    
    p = Product.objects.filter(id = rid)
    
    prod = Product.objects.get(id = rid)

    review = Review.objects.filter( product = prod)
    
    try:
        sum = 0
        n = 0
    
        for x in review:
            sum += x.rating
            n += 1
        
        avg = sum/n
    
        avg1 = int(sum/n)
    except:
        print('Error')
    
    context = {}
    
    context['data'] = p
    
    if n == 0:

        context['avg'] = 'No Review'

    else:
        
        context['avg'] = avg
    
        context['rating'] = avg1
    
    return render(request, 'productdetail.html', context)


def forgotPassword(request):
    
    if request.method == 'GET':
    
        return render(request, 'forgotpassword.html')

    else:
        
        otp = random.randint(1000, 9999)
        
        request.session['otp'] = otp
                
        email = request.POST['email']
        
        request.session['email'] = email
        
        user = User.objects.filter(email = email).exists()
        
        if user:
        
            with get_connection(
                
                host = settings.EMAIL_HOST,
                port = settings.EMAIL_PORT,
                username = settings.EMAIL_HOST_USER,
                password = settings.EMAIL_HOST_PASSWORD,
                use_tls = settings.EMAIL_USE_TLS
                
            ) as connection:
                
                subject = "OTP verification"
                email_from = settings.EMAIL_HOST_USER
                reciption_list =[ email ]
                message = f"Your opt is {otp}"
                
                EmailMessage(subject, message, email_from, reciption_list, connection = connection).send()

            return redirect('/opt_verification')

        else:
            
            context = {}
            
            context['error'] = 'user does not exist'
            
            return render(request, 'forgotpassword.html', context)
            
    
def opt_verification(request):
    
    if request.method == 'GET':
    
        return render(request, 'optverification.html')
    
    else:
        
        otp = int(request.POST['otp'])
        
        otp_email = int(request.session['otp'])
        
        if otp == otp_email:
            
            return redirect('/reset_password')
        
        else:
            
            context = {}

            context['error'] = 'OPT does not match'
            
            return render(request, 'optverification.html', context)
        
def reset_password(request):
    
    if request.method == 'GET':
    
        return render(request, 'resetpassword.html')

    else:
        
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            
            email = request.session['email']

            user = User.objects.get(email = email)
            
            user.set_password(password)

            user.save()
            
            return redirect('/login')