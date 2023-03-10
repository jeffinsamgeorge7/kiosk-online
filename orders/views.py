from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import Category,  Sub,UserOrder, SavedCarts, Drinks, Snacks;
'''RegularPizza, SicilianPizza, Toppings, Pasta, DinnerPlatters, '''
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import logout, authenticate, login
import json
from django.views.decorators.csrf import csrf_exempt
from . import forms
from math import sin, cos, tan
"""
import matplotlib.pyplot as plt
from django.shortcuts import render
from .models import models
"""
from .utils import get_plot
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4


def generate_pdf (request):
    response = HttpResponse(content_type='application/pdf')
    #d = datetime.today().strftime ('%Y-%m-%d')
    #response [ 'Content-Disposition'] = f'inline; filename="{d}.pdf"'
    buffer= BytesIO()
    p = canvas.Canvas (buffer, pagesize=A4)
    # Data to print
    
    
    
    if request.user.is_superuser:
        #make a request for all the orders in the database
        rows = UserOrder.objects.all().order_by('-time_of_order')
        #orders.append(row.order[1:-1].split(","))

    for row in rows:
        data= {
            "Order details":[{"Ordered By":row.username, "order-id:":row.id, "ordered-item:":row.order,"order-time":row.time_of_order}],
        }
        # Start writing the PDF here
        
        p. setFont("Helvetica", 15, leading=None)
        p. setFillColorRGB (0.29296875, 0.453125,0.609375)
        p.drawString(260,800, "My Website")
        p. line (0,780, 1000,780)
        p.line (8,778,1000,778)
        xl = 20
        yl = 750
        #Render data
        for k,v in data.items():
            p.setFont("Helvetica", 15, leading=None)
            p.drawString(xl,yl-12,f"{k}")
            
            for value in v:
                for key,val in value.items():
                    p. setFont("Helvetica", 10, leading=None)
                    p.drawString(xl, yl-20, f"{key}-{val}")
                    yl = yl-60
    #p.setTitle(f'Report on {d}')
    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        #we are passing in the data from the category model
        return render(request, "orders/home.html", {"categories":Category.objects.all})
    else:
        return redirect("orders:login")

def login_request(request):
    if request.method == 'POST':
        form = forms.Login(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                

                return redirect('/')
        else:
            return render(request = request,
                    template_name = "orders/login.html",
                    context={"form":form,"error":"Incorrect Username or Password"})
    form = forms.Login()
    return render(request = request,
                    template_name = "orders/login.html",
                    context={"form":form})

def logout_request(request):
    logout(request)
    return redirect("orders:login")

def register(request):
    if request.method == "POST":
        form = forms.Registration(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            return redirect("orders:index")

        return render(request = request,
                          template_name = "orders/register.html",
                          context={"form":form})
    form = forms.Registration()
    return render(request = request,
                  template_name = "orders/register.html",
                  context={"form":form})

def pizza(request):
    if request.user.is_authenticated:
        return render(request, "orders/pizza.html", context = {"regular_pizza":RegularPizza.objects.all, "sicillian_pizza":SicilianPizza.objects.all , "toppings":Toppings.objects.all, "number_of_toppings":3})
    else:
        return redirect("orders:login")

def pasta(request):
    if request.user.is_authenticated:
        return render(request, "orders/pasta.html", context = {"dishes":Pasta.objects.all})
    else:
        return redirect("orders:login")

def drink(request):
    if request.user.is_authenticated:
        return render(request, "orders/drink.html", context = {"dishes":Drinks.objects.all})
    else:
        return redirect("orders:login")


def payment(request):
    if request.user.is_authenticated:
        return render(request, "orders/payment.html")
    else:
        return redirect("orders:login")

def snack(request):
    if request.user.is_authenticated:
        return render(request, "orders/snack.html", context = {"dishes":Snacks.objects.all})
    else:
        return redirect("orders:login")


def subs(request):
    if request.user.is_authenticated:
        return render(request, "orders/sub.html", context = {"dishes":Sub.objects.all})
    else:
        return redirect("orders:login")


def dinner_platters(request):
    if request.user.is_authenticated:
        return render(request, "orders/dinner_platters.html", context = {"dishes":DinnerPlatters.objects.all})
    else:
        return redirect("orders:login")

def directions(request):
    if request.user.is_authenticated:
        return render(request, "orders/directions.html")
    else:
        return redirect("orders:login")

def hours(request):
    if request.user.is_authenticated:
        return render(request, "orders/hours.html")
    else:
        return redirect("orders:login")

def contact(request):
    if request.user.is_authenticated:
        return render(request, "orders/contact.html")
    else:
        return redirect("orders:login")

def cart(request):
    if request.user.is_authenticated:
        return render(request, "orders/cart.html")
    else:
        return redirect("orders:login")

def checkout(request):
    if request.method == 'POST':
        cart = json.loads(request.POST.get('cart'))
        price = request.POST.get('price_of_cart')
        username = request.user.username
        response_data = {}
        list_of_items = [item["item_description"] for item in cart]

        order = UserOrder(username=username, order=list_of_items, price=float(price), delivered=False) #create the row entry
        order.save() #save row entry in database

        response_data['result'] = 'Order Recieved!'

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
        
        

def view_orders(request):
    if request.user.is_superuser:
        #make a request for all the orders in the database
        rows = UserOrder.objects.all().order_by('-time_of_order')
        #orders.append(row.order[1:-1].split(","))

        return render(request, "orders/orders.html", context = {"rows":rows})
    else:
        rows = UserOrder.objects.all().filter(username = request.user.username).order_by('-time_of_order')
        return render(request, "orders/orders.html", context = {"rows":rows})

def mark_order_as_delivered(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        UserOrder.objects.filter(pk=id).update(delivered=True)
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def save_cart(request):
    if request.method == 'POST':
        cart = request.POST.get('cart')
        saved_cart = SavedCarts(username=request.user.username, cart=cart) #create the row entry
        saved_cart.save() #save row entry in database
        return HttpResponse(
            json.dumps({"good":"boy"}),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def retrieve_saved_cart(request):
    try:
        saved_cart = SavedCarts.objects.get(username = request.user.username)
        return HttpResponse(saved_cart.cart)
    except:
        return HttpResponse('')

def check_superuser(request):
    print(f"User super??? {request.user.is_superuser}")
    return HttpResponse(request.user.is_superuser)



def graph1_views(request):
    
    
    qs = UserOrder.objects.all()
    x=[x.order for x in qs]
    y=[y.price for y in qs]
    chart = get_plot(x,y)
    """
    ms = Snacks.objects.all()
    k=[k.dish_name for k in ms]
    j=[j.small_price for j in ms]
    chart1 = get_plot(k,j)
    
    js = Drinks.objects.all()
    m=[m.drink_name for m in js]
    o=[o.bottle_price for o in js]
    chart2 = get_plot(m,o)
    """
    return render (request, 'orders/subwaypgraph.html',{'chart':chart,})
"""
def graph2_views(request):
    ms = Snacks.objects.all()
    k=[k.dish_name for k in ms]
    j=[j.small_price for j in ms]
    chart1 = get_plot(k,j)
    return render (request, 'orders/snacksgraphs.html',{'chart1':chart1,})

def total_graphs(request):
    if request.user.is_superuser:
        return render (request, 'orders/total_graph.html')


def my_view(request):
    # Query the database for the data to use in the graph
    data = models.objects.all()

    # Extract the x and y data for the graph
    names = [d.subs for d in data]
    amounts = [d.price for d in data]

    # Create the bar chart using Matplotlib
    plt.bar(names, amounts)
    plt.xlabel('Name')
    plt.ylabel('Amount')

    # Save the plot to a file
    plt.savefig('/media/my_plot.png')

    # Open the file and read the contents
    with open('/media/my_plot.png', 'rb') as f:
        plot_data = f.read()

    # Return the plot in the HttpResponse object
    return HttpResponse(plot_data, content_type='image/png')
"""