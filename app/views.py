from django.shortcuts import render, HttpResponse, redirect
from app.models import *
from django.core.paginator import Paginator
import re
import datetime



def mainpage(request):
    is_login = request.COOKIES.get('user')
    LOGIN = False
    if is_login:
        LOGIN = True
        YOU = Users.objects.filter(user=is_login).first()
    else:
        YOU = None
    ALL = Bloks.objects.all()
    alls = []
    for i in ALL:
        alls.append(i)
    return render(request,"mainpage.html",{'LOGIN':LOGIN,"YOU":YOU,'alls':alls})

def loginpage(request):
    is_login = request.COOKIES.get('user')
    if is_login:
        return redirect('/')
    return render(request,"login.html")

def signpage(request):
    is_login = request.COOKIES.get('user')
    if is_login:
        return redirect('/')
    return render(request,"sign.html")

def detailpage(request, bk_id ='0'):
    is_login = request.COOKIES.get('user')
    LOGIN = False
    if is_login:
        LOGIN = True
        YOU = Users.objects.filter(user=is_login).first()
    else:
        YOU = None
    try:
        bk_id = int(bk_id)
    except:
        return redirect('/')
    BK = Bloks.objects.filter(nid=bk_id).first()
    TK = Talk.objects.filter(tk_bk=bk_id)
    TKS = []
    for i in TK:
        TKS.append(i)
    if not BK:
        return redirect('/')
    return render(request,"detail.html",{'LOGIN':LOGIN,"YOU":YOU,'BK':BK,'TK':TKS })

def submitpage(request):
    is_login = request.COOKIES.get('user')
    LOGIN = False
    if is_login:
        LOGIN = True
        YOU = Users.objects.filter(user=is_login).first()
    else:
        return redirect('/')
    return render(request,"submit.html",{'LOGIN':LOGIN,"YOU":YOU,'Error':False})

def submitS(request):
    is_login = request.COOKIES.get('user')
    YOU = Users.objects.filter(user=is_login).first()
    if request.method == "POST":
        title = request.POST.get("title")
        describe = request.POST.get("describe")
        text = request.POST.get("text")
        #text = re.sub('\n','&#10;',text)
        author = Users.objects.filter(user=request.COOKIES.get('user')).first().name
        curr_time = datetime.datetime.now()
        tm = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
        love = 0
        try:
            data = Bloks(bk_title=title,bk_describe=describe,bk_text=text,bk_author=author,bk_love=love,bk_time=tm)
            data.save()
        except:
            return render(request,"submit.html",{'LOGIN':True,"YOU":YOU,'Error':True})
        Blok = Bloks.objects.filter(bk_time=tm).first()
        return redirect('/detail/{}'.format(str(Blok.nid)))
    
def infpage(request):
    is_login = request.COOKIES.get('user')
    LOGIN = False
    if is_login:
        LOGIN = True
        YOU = Users.objects.filter(user=is_login).first()
        logintime = LoginTime.objects.filter(tk_user=is_login).all()
        alls = []
        for i in logintime:
            alls.append(i)
        if len(alls) > 10:
            alls = alls[-10:]
    else:
        YOU = None
    
    return render(request,"inf.html",{'LOGIN':LOGIN,"YOU":YOU,'ALLS':alls})

def loginS(request):
    if request.method == "POST":
        user = request.POST.get("name")
        pwd = request.POST.get("pwd")
        comics = Users.objects.filter(user=user).first()
        if not comics:
            return render(request,"login.html",{'USER_WRONG':True,'PWD_WRONG':False})
        if comics.pwd == pwd:
            curr_time = datetime.datetime.now()
            tm = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
            data = LoginTime(tk_user=user,tk_time=tm)
            data.save()
            obj = redirect('/inf/')
            obj.set_cookie('user',user)
            return obj
        else:
            return render(request,"login.html",{'USER_WRONG':False,'PWD_WRONG':True})

def signS(request):
    if request.method == "POST":
        user = request.POST.get("name")
        pwd = request.POST.get("pwd")
        name = request.POST.get("name2")
        pwd2 = request.POST.get("pwd2")
        email = request.POST.get("email")
        curr_time = datetime.datetime.now()
        tm = datetime.datetime.strftime(curr_time,'%Y-%m-%d %H:%M:%S')
        comics = Users.objects.filter(user=user).first()
        if comics:
            return render(request,"sign.html",{'USER_WRONG':True,'PWD_WRONG':False})
        comics = Users.objects.filter(name=name).first()
        if comics:
            return render(request,"sign.html",{'USER_WRONG':True,'PWD_WRONG':False})
        if pwd != pwd2:
            return render(request,"sign.html",{'USER_WRONG':False,'PWD_WRONG':True})
        data = Users(user=user,pwd=pwd,name=name,email=email,time=tm,basicpwd=pwd,aut=0)
        data.save()
        obj = redirect('/login/')
        # obj.set_cookie('user',user)
        return obj

def talkS(request):
    is_login = request.COOKIES.get('user')
    if is_login:
        YOU = Users.objects.filter(user=is_login).first()
    else:
        return redirect('/')
    if request.method == "POST":
        num = request.POST.get("title")
        text = request.POST.get("text")
        tm = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
        data = Talk(tk_bk=num,tk_author=YOU.name,tk_text=text,tk_time=tm)
        data.save()
        return redirect('/detail/{}'.format(str(num)))

def changepwd(request):
    is_login = request.COOKIES.get('user')
    LOGIN = False
    if is_login:
        LOGIN = True
    return render(request,"change_pwd.html",{'LOGIN':LOGIN,'PWD_WRONG':False,'OK':False})

def changepwdS(request):
    is_login = request.COOKIES.get('user')
    if request.method == "POST":
        pwd = request.POST.get("name")
        pwd_new = request.POST.get("pwd")
        Yo = Users.objects.filter(user=is_login).first()
        if pwd != Yo.pwd:
            return render(request,"change_pwd.html",{'LOGIN':True,'PWD_WRONG':True,'OK':False})
        Yo.pwd = pwd_new
        Yo.save()
        return render(request,"change_pwd.html",{'LOGIN':True,'PWD_WRONG':False,'OK':True})

def returnpwd(request):
    return render(request,"return_pwd.html",{'NotOK':False,'OK':False})

def returnpwdS(request):
    if request.method == "POST":
        user = request.POST.get("name")
        email = request.POST.get("email")
        Yo = Users.objects.filter(user=user).first()
        if not Yo or Yo.email != email:
            return render(request,"return_pwd.html",{'NotOK':True,'OK':False})
        Yo.pwd = Yo.basicpwd
        Yo.save()
        return render(request,"return_pwd.html",{'NotOK':False,'OK':True})

def logout(request):
    obj = redirect('/')
    obj.set_cookie('user','')
    return obj

def admin(request):
    user = Users.objects.all()
    a1 = []
    for i in user:
        a1.append(i)

    block = Bloks.objects.all()
    a2 = []
    for i in block:
        a2.append(i)

    talk = Talk.objects.all()
    a3 = []
    for i in talk:
        a3.append(i)

    logintime = LoginTime.objects.all()
    a4 = []
    for i in logintime:
        a4.append(i)

    a = [len(a1), len(a2), len(a3), len(a4)]

    return render(request, "admin.html", {'a': a})

def admin_message_show(request):
    page = request.GET.get('page', 1)
    ALL = Bloks.objects.all()
    alls = []
    for i in ALL:
        alls.append(i)
    paginator = Paginator(alls, 20)
    page_data = paginator.page(page)
    return render(request, "admin_message_show.html", {'page_data': page_data})

def delete_message(request):
    message_id = request.GET.get('message_id')
    Bloks.objects.filter(nid=message_id).delete()
    return redirect('/admin_message_show/')

def admin_talk_show(request):
    page = request.GET.get('page', 1)
    ALL = Talk.objects.all()
    alls = []
    for i in ALL:
        alls.append(i)
    paginator = Paginator(alls, 20)
    page_data = paginator.page(page)
    return render(request, "admin_talk_show.html", {'page_data': page_data})

def delete_talk(request):
    talk_id = request.GET.get('talk_id')
    Talk.objects.filter(nid=talk_id).delete()
    return redirect('/admin_talk_show/')

def admin_user_show(request):
    page = request.GET.get('page', 1)
    ALL = Users.objects.all()
    alls = []
    for i in ALL:
        alls.append(i)
    paginator = Paginator(alls, 20)
    page_data = paginator.page(page)
    return render(request, "admin_user_show.html", {'page_data': page_data})

def delete_user(request):
    user_id = request.GET.get('user_id')
    Users.objects.filter(nid=user_id).delete()
    return redirect('/admin_user_show/')

def change_aut(request):
    user_id = request.GET.get('user_id')
    a = Users.objects.get(nid=user_id)
    if a.aut == 0:
        a.aut = 1
    else:
        a.aut = 0
    a.save()
    return redirect('/admin_user_show/')