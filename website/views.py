from django.shortcuts import render
import time,traceback
import datetime
from .Token import Token
from random import randint
import Uranus.settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import LoginMassage,RegisterForm
from django.contrib.auth.models import User
from .models import Comment,UserProfile

token_confirm = Token(Uranus.settings.SECRET_KEY)

def Enter(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('R_FuncPage')
    else:
        return HttpResponseRedirect('MainPage')
########################################################################################
#主页面
def MainPage(request):
    return render(request,'website/MainPage.html')

def MobileMain(request):
    return render(request,'website/Mobile-Main.html')
########################################################################################
#登陆界面
def Login(request):
    return render(request,'website/Login.html')

#登陆处理
def E_Login(request):
    errors = []
    try:
        if request.method == 'POST':
            form = LoginMassage(request.POST)
            if form.is_valid():
                usrName = form.cleaned_data['usrName']
                usrPassword = form.cleaned_data['usrPassword']
                user = authenticate(username = usrName,password = usrPassword)
                if user == None:
                    errors.append('用户名/密码错误')
                    return render(request,'website/Login.html',{'errors':errors})
                else:
                    login(request,user)
                    return HttpResponseRedirect('R_FuncPage')
        else:
            form = LoginMassage()
    except Exception as e:
        errors.append(str(e))
    return render(request,'website/Login.html',{'errors':errors})

#登出
def Logout(request):
    logout(request)
    return HttpResponseRedirect('MainPage')

########################################################################################
#注册界面
def Register(request):
    return render(request,'website/Register.html')

#注册处理
def E_Register(request):
    curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
    try:
        if request.method=='POST':
            #nickName = request.POST.get('nickName','')
            usrName = request.POST.get('usrName','')
            usrPassword = request.POST.get('usrPassword','')
            subPassword = request.POST.get('subPassword','')
            email = request.POST.get('email','')
            errors=[]
#对表单进行验证
            registerForm = RegisterForm(request.POST)
            if not registerForm.is_valid():
                errors.extend(registerForm.errors.values())
                return render(request,'website/Register.html',
            context=({'curtime':curtime,'usrName':usrName,'email':email,'errors':errors}))
            if len(usrPassword)<6 and not usrPassword.isdigit():
                errors.append('密码强度不够，至少六位密码，且不能全为数字')
            if usrPassword != subPassword:
                errors.append('两次输入的密码不一致！')
                return render(request,'website/Register.html',
            context=({'curtime':curtime,'usrName':usrName,'email':email,'errors':errors}))
            for sb in User.objects.all():
                try:
                    if sb.is_active == False:
                        last = sb.date_joined
                        now = datetime.datetime.now()
                        during = (now-last).seconds
                        if during > 3600:
                            sb.delete()
                except Exception as e:
                    print(str(e))
            filterResult = User.objects.filter(username=usrName)
            if len(filterResult)>0:
                errors.append('用户名已存在！')
                return render(request,'website/Register.html',
            context=({'curtime':curtime,'usrName':usrName,'email':email,'errors':errors}))

            user = User.objects.create_user(username=usrName,password=usrPassword,email=email,is_active=False)
            user.set_password(usrPassword)
            user.save()
            profile = UserProfile()
            profile.user_id = user.id
            chars = 'AaBbCcDdEeFf1234567890'
            string = ''
            i=1
            while (i<9):
                i = i + 1
                string += chars[randint(0,21)]
            profile.code = string
            #profile.nickName = nickName
            profile.save()
            
            Email(user.id)
            return HttpResponse(u'请登陆注册邮箱中验证账户，有效期1小时')
#对异常的处理
    except Exception as e:
        errors.append(str(e))
        return render(request,'website/Register.html',
    context=({'curtime':curtime,'usrName':usrName,'email':email,'errors':errors}))
    return render(request,'website/Register.html')

def Email(id):
    email = User.objects.get(id = id).email
    username = User.objects.get(id = id).username
    token = token_confirm.generate_validate_token(username)
    message = "\n".join([u'{0},Oh shit, to avoid the checking of QQ'.format(username),
    u', i choose this way to inform you to click this link and finish register! Understand?',
    '/'.join([Uranus.settings.DOMAIN,'E_Email',token])
    ])
    send_mail(u'This letter is from uranus',message,Uranus.settings.EAMIL_FROM,[email])

def E_Email(request,token):
    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        return HttpResponse(u'对不起，验证链接已过期')
    try:
        user = User.objects.get(username = username)
    except ObjectDoesNotExist:
        return HttpResponse(u'对不起，您所验证的用户不存在，请重新注册')
    user.is_active = True
    user.save()
    errors = u'验证成功，请进行登陆操作'
    return render(request,'website/Login.html',{'errors':errors})
########################################################################################
def Forget(request):
    return render(request,'website/Forget.html')

def E_Forget(request):
    try:
        if request.method == 'POST':
            new_password = request.POST.get('new_password','')
            re_new_password = request.POST.get('re_new_password','')
            email = request.POST.get('email','')
            usrName = request.POST.get('usrName','')
            errors = []
            length = User.objects.filter(username = usrName)
            if(new_password != re_new_password):
                errors.append('两次输入的密码不一致！')
                return render(request,'website/Forget.html',{'errors':errors})
            if length == 0:
                errors.append('用户名不存在')
                return render(request,'website/Forget.html',{'errors':errors})
            else:
                user = User.objects.get(username = usrName)
                if not user.email == email:
                    errors.append('用户名与邮箱不匹配')
                    return render(request,'website/Forget.html',{'errors':errors})
                else:
                    user.is_active = False
                    user.set_password(new_password)
                    user.save()
                    token = token_confirm.generate_validate_token(usrName)
                    message = "\n".join([u'{0}, your password is changed'.format(usrName),
                    u', i choose this way to inform you to click this link and finish changing password! Understand?',
                    '/'.join([Uranus.settings.DOMAIN,'E_Email',token])
                    ])
                    send_mail('An identification',message,Uranus.settings.EAMIL_FROM,[email])
                    return HttpResponse('密码已成功修改，查看邮件重新登陆，有效时间1小时')
    except Exception as e:
        errors.append(str(e))
        return render(request,'website/Forget.html',{'errors':errors})
########################################################################################
#登录功能页面（限制权限）
def R_FuncPage(request):
    if request.user.is_authenticated:
        pk = request.user.id
        userpro = UserProfile.objects.get(user_id=pk)
        port = userpro.port
        domain = userpro.domain
        userpro.begin=datetime.datetime.now
        userpro.save()
        if userpro.begin>userpro.end :
            userpro.end=userpro.begin
        time = str((userpro.begin-userpro.end))
        userpro.save()
        contacts=[port,time,domain]
        return render(request,'website/R_FuncPage.html',{'contacts':contacts})
    else:
        return HttpResponseRedirect('Login')

#评论区（限权）
def List(request):
    contact_list = Comment.objects.all()
    paginator = Paginator(contact_list,7)

    page = request.GET.get('page')
    contacts = paginator.get_page(page)
    return render(request,'List.html',{'contacts':contacts})

########################################################################################
def GameSpeeder(request):
    return render(request,'website/GameSpeeder.html')

def MobileGameSpeeder(request):
    return render(request,'website/MobileGameSpeeder.html')

def Ssr(request):
    return render(request,'website/Ssr.html')

def Wait(request):
    return render(request,'website/Wait.html')

def MobileSsr(request):
    return render(request,'website/MobileSsr.html')
