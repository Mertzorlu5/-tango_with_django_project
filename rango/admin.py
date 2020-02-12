from django.contrib import admin
from rango.models import UserProfile
# Register your models here.
from django.contrib import admin
from rango.models import Category, Page
class PageAdmin(admin.ModelAdmin): #chp 5 admin.ModelAdmin is the way to inherit from a clas.
    list_display = ('title', 'category', 'url') #chp5
class CategoryAdmin(admin.ModelAdmin): #chp6
    prepopulated_fields = {'slug':('name',)} #chp6


admin.site.register(Category,CategoryAdmin) #chp6
admin.site.register(Page, PageAdmin)#chp5
admin.site.register(UserProfile)