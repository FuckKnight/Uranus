from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
    path('',views.Enter,name='Enter'),
    path('MainPage/',views.MainPage,name='MainPage'),
    path('MobileMain',views.MobileMain,name='MobileMain'),
#################################################################################
    path('Login/',views.Login,name='Login'),
    path('E_Login',views.E_Login,name='E_Login'),
    path('Logout',views.Logout,name='Logout'),
#################################################################################
    path('Register/',views.Register,name='Register'),
    path('E_Register',views.E_Register,name='E_Register'),
#################################################################################
    path('Email/',views.Email,name='Email'),
    url(r'^E_Email/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)$',views.E_Email,name='E_Email'),
#################################################################################
    path('R_FuncPage/',views.R_FuncPage,name='R_FuncPage'),
    path('List',views.List,name='List'),
#################################################################################
    path('Forget/',views.Forget,name='Forget'),
    path('E_Forget',views.E_Forget,name='E_Forget'),
#################################################################################
    path('GameSpeeder',views.GameSpeeder,name='GameSpeeder'),
    path('MobileGameSpeeder',views.MobileGameSpeeder,name='MobileGameSpeeder'),
    path('Wait',views.Wait,name='Wait'),
    path('Ssr',views.Ssr,name='Ssr'),
    path('MobileSsr',views.MobileSsr,name='MobileSsr'),
]