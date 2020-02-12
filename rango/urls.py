from django.urls import path
from rango import views
app_name = 'rango'
urlpatterns = [path('about/', views.about, name='about'), #rango/about/ yapınca buraya gidilir.
               path('', views.index, name='index'), #index degil bos birak homepagedir burası rango/ yapınca buraya
               path('category/<slug:category_name_slug>/', views.show_category, name='show_category'), #chp6
                path('add_category/', views.add_category, name='add_category'),
                path('category/<slug:category_name_slug>/add_page/',views.add_page,name='add_page') ,#chp7
                path('register/', views.register, name='register'), #chp9
                path('login/', views.user_login, name='login'),
                path('restricted/', views.restricted, name='restricted'),
                path('logout/', views.user_logout, name='logout'),
                ]
