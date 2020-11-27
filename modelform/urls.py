"""modelform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.LoginView.as_view(), name='login'),
    url(r'^login_out/', views.LoginOutView.as_view(), name='login_out'),
    url(r'^register/', views.RegisterView.as_view(), name='register'),
    url(r'^home/', views.HomeView.as_view(), name='home'),
    url(r'^customer/', views.CustomerView.as_view(), name='customer'),
    url(r'^my_customer/', views.CustomerView.as_view(), name='my_customer'),
    # url(r'^add_customer/', views.AddCustomerView.as_view(), name='add_customer'),
    url(r'^add_customer/', views.AddEditCustomer.as_view(), name='add_customer'),
    url(r'^edit_customer/(\d+)/', views.AddEditCustomer.as_view(), name='edit_customer'),
]
