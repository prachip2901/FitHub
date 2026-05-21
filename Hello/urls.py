from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Online Fitness Admin"
admin.site.site_title = "Online Fitness Admin Portal"
admin.site.index_title = "Welcome to Online Fitness"

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('Home.urls')),


]

