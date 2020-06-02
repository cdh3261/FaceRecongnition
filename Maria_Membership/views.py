from django.shortcuts import render, redirect, get_object_or_404
from . import faceReconition, takePicture
from .models import Info, Menu, RMENU, Store
from .forms import InfoForm, MenuForm
# Create your views here.

userName = ''
userPhoneNumber = ''


def home(request):
    global userName, userPhoneNumber
    # store = Store.objects.get(sID=1)
    # print(store.sName)
    userName = ''
    userPhoneNumber = ''
    context = {
        'username':userName,
    }
    return render(request, 'home.html', context)

def information(request):
    form = InfoForm()
    context = {
        'form': form,
    }
    return render(request, 'form.html', context)


def reqfacePicture(request):
    global userName, userPhoneNumber
    if request.method == 'POST':
        form = InfoForm(request.POST)
        userName = request.POST['uName']
        userPhoneNumber = request.POST['uPhone']

        if form.is_valid():
            keyNumber = takePicture.takePt(userName, userPhoneNumber)

            # 스페이스 바를 누르면 저장을 진행
            if keyNumber == 32:
                user = form.save()
                return render(request, 'check.html')

            # ESC를 누를 경우 회원가입을 취소하고 회원정보 입력페이지로 돌아간다.
            elif keyNumber == 27:
                context = {
                    'form': form,
                }
                return render(request, 'cancel.html', context)

            # 사진이 제대로 찍히지 않은 경우
            elif keyNumber == 999:
                context = {
                    'form': form,
                }
                return render(request, 'noRecog.html', context)
        else:
            return render(request, 'return.html')

    # post방식이 아닌 주소를 쳐서 들어오면 홈으로 돌아간다.
    return redirect('Maria_membership:home')


def reqfaceRecog(request):
    global userPhoneNumber, userName

    if request.method == 'POST':
        try:
            userPhoneNumber = faceReconition.face()
        except:
            return redirect('Maria_membership:home')
        # 회원이 아닌 경우 홈화면으로 이동
        if userPhoneNumber == 'unknown':
            return redirect('Maria_membership:home')
        userinfo = get_object_or_404(Info, uPhone=userPhoneNumber)
        userName = userinfo.uName
        try:
            menuinfo = get_object_or_404(Menu, user=userinfo)
            menu_id = menuinfo.id
            menuinfo = get_object_or_404(Menu, user=userinfo, id=menu_id)
            americano = menuinfo.americano
            latte = menuinfo.latte
            smoothy = menuinfo.smoothy
            total = menuinfo.total
            favorite = [['아메리카노', americano, '3,000'], [
                '라떼', latte, '4,000'], ['스무디', smoothy, '5,000']]
            favorite = sorted(favorite, key=lambda x: x[1], reverse=True)
            context = {
                'userName': userName,
                'userPhoneNumber': userPhoneNumber,
                'first': favorite[0][1],
                'first_menu': favorite[0][0],
                'second': favorite[1][1],
                'second_menu': favorite[1][0],
                'third': favorite[2][1],
                'third_menu': favorite[2][0],
                'first_price': favorite[0][2],
                'second_price': favorite[1][2],
                'third_price': favorite[2][2],
                'total': total,
            }
        except:
            context = {
                'userName': userName,
                'userPhoneNumber': userPhoneNumber,
                'first': 0,
                'first_menu': '아메리카노',
                'second': 0,
                'second_menu': '라떼',
                'third': 0,
                'third_menu': '스무디',
                'first_price': '3,000',
                'second_price': '4,000',
                'third_price': '5,000',
                'total': 0,
            }
        return render(request, 'complete.html', context)

    return redirect('Maria_membership:home')

# 메인메뉴


def menu(request):
    global userPhoneNumber, userName
    menuForm = MenuForm()
    if request.method == 'POST':
        if userPhoneNumber != '':
            # 메뉴폼에 받은 정보 넣기
            form = MenuForm(request.POST)
            if form.is_valid():
                context = {
                    'form': form,
                }
                if request.POST.get('total') == '0':
                    return redirect('Maria_membership:menu')
                return render(request, 'order.html', context)
        else:
            context = {
                'username':userName,
                'form':menuForm,
            }
            return render(request,'menu.html',context)

    context = {
        'form': menuForm,
        'username': userName,
    }
    return render(request, 'menu.html', context)


def stamp(request):
    global userName, userPhoneNumber
    if request.method == "POST":
        userinfo = get_object_or_404(Info, uPhone=userPhoneNumber)
        try:

            menuinfo = get_object_or_404(Menu, user=userinfo)
            menu_id = menuinfo.id
            menuinfo = get_object_or_404(Menu, user=userinfo, id=menu_id)
            if menuinfo.total >= 10:
                menuinfo.total -= 10
                menuinfo.save()
            else:
                return redirect('Maria_membership:mypage')
        except:
            return redirect('Maria_membership:mypage')

        americano = menuinfo.americano
        latte = menuinfo.latte
        smoothy = menuinfo.smoothy
        total = menuinfo.total
        favorite = [['아메리카노', americano, '3,000'], [
            '라떼', latte, '4,000'], ['스무디', smoothy, '5,000']]
        favorite = sorted(favorite, key=lambda x: x[1], reverse=True)
        context = {
            'userName': userName,
            'userPhoneNumber': userPhoneNumber,
            'first': favorite[0][1],
            'first_menu': favorite[0][0],
            'second': favorite[1][1],
            'second_menu': favorite[1][0],
            'third': favorite[2][1],
            'third_menu': favorite[2][0],
            'first_price': favorite[0][2],
            'second_price': favorite[1][2],
            'third_price': favorite[2][2],
            'total': total,
        }
        return render(request, 'complete.html', context)

    return redirect('Maria_membership:home')


def mypage(request):
    global userPhoneNumber, userName
    if userPhoneNumber != '':
        try:
            userinfo = get_object_or_404(Info, uPhone=userPhoneNumber)
            menuinfo = get_object_or_404(Menu, user=userinfo)
            menu_id = menuinfo.id
            menuinfo = get_object_or_404(Menu, user=userinfo, id=menu_id)
            americano = menuinfo.americano
            latte = menuinfo.latte
            smoothy = menuinfo.smoothy
            total = menuinfo.total
            favorite = [['아메리카노', americano, '3,000'], [
                '라떼', latte, '4,000'], ['스무디', smoothy, '5,000']]
            favorite = sorted(favorite, key=lambda x: x[1], reverse=True)
            context = {
                'userName': userName,
                'userPhoneNumber': userPhoneNumber,
                'first': favorite[0][1],
                'first_menu': favorite[0][0],
                'second': favorite[1][1],
                'second_menu': favorite[1][0],
                'third': favorite[2][1],
                'third_menu': favorite[2][0],
                'first_price': favorite[0][2],
                'second_price': favorite[1][2],
                'third_price': favorite[2][2],
                'total': total,
            }
        except:
            context = {
                'userName': userName,
                'userPhoneNumber': userPhoneNumber,
                'first': 0,
                'first_menu': '아메리카노',
                'second': 0,
                'second_menu': '라떼',
                'third': 0,
                'third_menu': '스무디',
                'first_price': '3,000',
                'second_price': '4,000',
                'third_price': '5,000',
                'total': 0,
            }
        return render(request, 'complete.html', context)
    else:
        return redirect('Maria_membership:home')


def order_complete(request):
    global userName, userPhoneNumber
    if request.method == 'POST':
        form = MenuForm(request.POST)
        # 유니크한 폰번호로 db접근
        userinfo = get_object_or_404(Info, uPhone=userPhoneNumber)
        menu = form.save(commit=False)
        # 기존에 주문한 적이 있으면 try, 없으면 except문
        try:
            menuinfo = get_object_or_404(Menu, user=userinfo)
            menu_id = menuinfo.id
            menuinfo = get_object_or_404(Menu, user=userinfo, id=menu_id)
            menuinfo.americano += menu.americano
            menuinfo.latte += menu.latte
            menuinfo.smoothy += menu.smoothy
            menuinfo.total += menu.total
            menuinfo.save()

            context = {
                'form': menu,

            }
        except:
            menu.user = userinfo
            menu.save()
            context = {
                'form': form,

            }

        return redirect('Maria_membership:mypage')

    return redirect('Maria_membership:home')
