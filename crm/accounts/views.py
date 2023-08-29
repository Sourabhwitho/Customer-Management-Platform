from django.shortcuts import render, redirect 
from django.http import HttpResponse, HttpRequest
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import *
from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users, admin_only

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	return render(request, 'accounts/dashboard.html', context)

def userPage(request):
	orders = request.user.customer.order_set.all()

	total_orders = orders.count()
	delivered = orders.filter(status='Delivered').count()
	pending = orders.filter(status='Pending').count()
	context = {'orders':orders, 'total_orders':total_orders,
	'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)



@login_required(login_url='login')
def products(request):
	products = Product.objects.all()
	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
	customer = Customer.objects.get(id=pk)

	orders = customer.order_set.all()
	order_count = orders.count()

	myFilter = OrderFilter(request.GET, queryset=orders)
	orders = myFilter.qs 

	context = {'customer':customer, 'orders':orders, 'order_count':order_count,
	'myFilter':myFilter}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=1)
	customer = Customer.objects.get(name=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	print(formset)
	if request.method == 'POST':
		OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			# formset.status='Pending'
			formset.save()
			return redirect('/')

	context = {'field':formset}
	return render(request, 'accounts/forms.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
	print(pk)
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/forms.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order,'action':"order"}
	return render(request, 'accounts/delete.html', context)

@login_required(login_url='login')
@admin_only
def AddProd(request):
	formset = ProductForm()
	if request.method == 'POST':
		formset = ProductForm(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/products')
	
	context = {'form':formset}
	return render(request, 'accounts/addproduct.html', context)

@login_required(login_url='login')
@admin_only
def CreateCustomer(request):
	formset = CustomerForm()
	if request.method == 'POST':
		formset = CustomerForm(request.POST)
		if formset.is_valid():
			formset.save()
			return redirect('/')
	
	context = {'form':formset}
	return render(request, 'accounts/forms.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
	print(pk)
	# userr= User.objects.get(id=pk)
	# print(userr.username)
	customer = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')
	
	context = {'form':form }
	return render(request, 'accounts/forms.html', context)

@login_required(login_url='login')
def placeOrder(request,pk):
	product=Product.objects.get(name=pk)
	customer=request.user.customer
	if request.method == "POST":
		Order.objects.create(product=product, customer=customer, status="Pending")
		return redirect('/')
	context = {'item':product}
	return render(request, 'accounts/place_order.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteProd(request, pk):
	product=Product.objects.get(name=pk)
	if request.method == "POST":
		product.delete()
		return redirect('/products')

	context = {'item':product, 'action': "prod" }
	return render(request, 'accounts/delete.html', context)