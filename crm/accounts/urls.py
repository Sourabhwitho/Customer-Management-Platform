from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
    path('add_prod/', views.AddProd, name="add_product"),  
    path('create_customer/', views.CreateCustomer, name="create_customer"),
    path('update_customer/<str:pk>', views.updateCustomer, name="update_customer"),
	path('logout/', views.logoutUser, name="logout"),
    path('', views.home,name="home"),
    path('user/', views.userPage, name="user-page"),
    path('products/',views.products,name="products"),
    path('customer/<str:pk>',views.customer,name="customer"),
    path('account/', views.accountSettings, name="account"),
    path('create_order/<str:pk>', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('place_order/<str:pk>', views.placeOrder, name="place_order"),
    path('delete_item/<str:pk>', views.deleteProd, name="delete_item"),
]