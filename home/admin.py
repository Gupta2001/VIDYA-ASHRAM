from django.contrib import admin
from home.models import Contact
from .models import *
# Register your models here.


class Blogadmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("css/main.css",)
        }

        js = ("js/blog.js",)



class profileadmin(admin.ModelAdmin):   
        list_display = ('user','Name','fathers_Name','Classes','Email_id','Dues','is_verified')
        exclude = ('auth_token','is_verified')


class contactadmin(admin.ModelAdmin):   
        list_display = ('name','email','phone','time')
       

admin.site.register(Contact,contactadmin)
admin.site.register(Profile, profileadmin)
admin.site.register(Blog,Blogadmin)