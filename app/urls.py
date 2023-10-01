from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('create',views.create),
    path('update/<int:id>',views.update,name='update'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('file',views.FileUploadView.as_view(),name='file'),
    path('images',views.ProfileView.as_view(),name='images'),
    path('register',views.register_page,name='register'),
    path('login',views.login_page,name='login'),
    path('logout',views.logout_page,name='logout')

]
