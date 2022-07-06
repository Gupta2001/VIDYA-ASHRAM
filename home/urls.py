from django.contrib import admin
from django.urls import path, include

from home import views




admin.site.site_header="Login to Vidya Ashram Admin Page"
admin.site.site_title="Welcome to Vidya Ashram Dashboard"
admin.site.index_title= "Welcome to Vidya Ashram Admin Portal"

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('blogpost/<str:slug>', views.blogpost, name='blogpost'),
    path('login/', views.login, name='login'),
    path('signin/', views.handlelogin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('verify/<auth_token>' ,views.verify , name="verify"),
    path('forget', views.forgetpass, name='forget'),
    path('reset', views.reset, name='reset'),
    path('changepass/<auth_token>', views.changepass, name='change'),
    path('register/', views.register, name='register')
]


 