from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render
import random

# Create your views here.
def home(request):
    return render(request, 'bluemarble_app/start_page.html')


def index_ing(request):  #DB에 사용자 이름과 학과를 전달하는 것
    if request.POST.get('name') == '':
        return HttpResponse("다시 입력하세요")
    else:
        user_name= request.POST.get('name', False)
        user_major= request.POST.get('major',False)
        UserInfo.objects.create(name=user_name, major=user_major)
        user = UserInfo.objects.get(name=user_name, major=user_major)
        request.session['user_id'] = request.POST['name']
        user.save()
        return HttpResponseRedirect("/main/{}/".format(user.id))

def main(request, myname):
    room = RoomInfo.objects.filter(full=1)
    me = UserInfo.objects.get(id=myname)
    potal = {'rooms': room, 'me': me}
    return render(request, 'bluemarble_app/main.html', potal)

def make(request,myname):

    me=UserInfo.objects.get(id=myname)
    context={'me':me}
    return render(request, 'bluemarble_app/make.html', context)

def make_ing(request, myname):

    user = UserInfo.objects.get(name=request.session['user_id'])
    user.one_or_two = 1
    str = request.POST.get('roomname', False)
    RoomInfo.objects.create(name=str)
    room = RoomInfo.objects.get(name=str)
    room.user1 = user.name
    room.save()
    context = {'roominform': room, 'room_no': room.id}
    return HttpResponseRedirect("/room/{}/{}".format(room.id, myname ))


def room(request, room_id, myname):
    me = UserInfo.objects.get(id=myname)
    room = RoomInfo.objects.get(id=int(room_id))
    if (room.full == 0):
        room.user1 = me.name
        room.major1 = me.major
        room.countOfVictory1 = me.countOfVictory
        room.full = 1
        room.save()
        context = {'room': room, 'me': me}
        return render(request, 'bluemarble_app/room.html', context)

    elif (room.full == 1 and room.user1 != me.name):
        room.user2 = me.name
        room.major2 = me.major
        room.countOfVictory2 = me.countOfVictory
        room.full = 2
        room.save()
        context = {'room': room, 'me': me}

        return render(request, 'bluemarble_app/room.html', context)

    elif (room.user1 != me.name and room.user2 != me.name and room.full == 2):
        return HttpResponseRedirect("/main/{}/".format(myname))

    else:
        """
        저장 후 반환 
        """
        context = {'room': room, 'me': me}
        return render(request, 'bluemarble_app/room.html', context)

def out(request, room_id, myname): # out
    me = UserInfo.objects.get(id=myname)
    room = RoomInfo.objects.get(id=int(room_id))
    context = {'room' : room, 'me': me }
    if(room.full == 2 and room.user1 != me.name):
        room.user1 = me.name
        room.user2 = 'none'
        room.full = 1
        room.save()
        return render(request, 'bluemarble_app/out.html',context) #방나가
    elif(room.full == 2 and room.user2 != me.name):
        room.user1 = 'none'
        room.user2 = me.name
        room.full = 1
        room.save()
        return render(request, 'bluemarble_app/out.html',context) #방나가

    elif(room.full == 1 and room.user1 != me.name):
        room.user1 = 'none'
        room.user2 = 'none'
        room.full = 0
        room.save()
        return render(request, 'bluemarble_app/out.html',context) #방나가
    elif(room.full == 1 and room.user2 != me.name):
        room.user1 = 'none'
        room.user2 = 'none'
        room.full = 0
        room.save()
        return render(request, 'bluemarble_app/out.html',context) #방나가
    return render(request, 'bluemarble_app/out.html', context)  # 방나가


def room_to_marble(requset, room_id, myname):
    me = UserInfo.objects.get(id=myname)
    room = RoomInfo.objects.get(id=room_id)

    if room.user1 == 'none' or room.user2 == 'none':
        return HttpResponseRedirect("/room/{}/{}".format(room.id, myname))

    global ok_1
    global ok_2
    ok_1 = 0
    ok_2 = 0

    while True:

        if room.user1 == me.name:
            ok_1 = 1

        if room.user2 == me.name:
            ok_2 = 1

        if ok_1 == 1 and ok_2 == 1:
            return HttpResponseRedirect("/game/{}/{}/".format(room.user1,room.user2))
            '''return HttpResponseRedirect("/game/{}/{}/{}/{}/{}/{}/".format(room.user1, room.user2, room.major1, room.major2, room.countOfVictory1, room.countOfVictory2))'''
            #return HttpResponseRedirect("/main/{}/".format(user.id))


landList = []
majorList = []
indexList = []
gradeList = []
turnTemp = 1
count=0;
str = ""
priceStr = 0
diceNum = 0
answer1 = ""
bankruptcyTemp = False

class gradeIndex:
   def __init__(self, top, left, index):
      self.top = top
      self.left = left
      self.index = index


class positionIndex:
    def __init__(self, top1, left1, top2, left2):
        self.top1 = top1
        self.left1 = left1
        self.top2 = top2
        self.left2 = left2


class user:
    def __init__(self, name, major):
        self.name = name  # 로그인
        self.major = major  # 로그인
        self.countOfVictory = 0  # 로그인
        self.position = 0  # 게임시작
        self.num = 0;  # 게임시작
        self.money = 3000000  # 게임시작
        self.library = False  # 게임시작
        self.station = False  # 게임시작


class land:
    def __init__(self, name, price, rentable):
        self.name = name
        self.price = price
        self.rentable = rentable
        self.owner = 0
        self.grade = 0


def setMajor(user, majorNum):
    for i in range(1, 9):
        if majorNum == i:
            user.major = majorList[i]


def turn(user1, user2):
    global turnTemp
    if turnTemp == 1:
        turnTemp = 2
        move(user1, user2)
        print(
        "User1 :", landList[user1.position].name, " Money :", user1.money, "\nUser2 :", landList[user2.position].name,
        " Money :", user2.money)
    else:
        turnTemp = 1
        move(user2, user1)
        print(
        "User1 :", landList[user1.position].name, " Money :", user1.money, "\nUser2 :", landList[user2.position].name,
        " Money :", user2.money)


def move(user, other):
    global str
    if user.library == True:
        str = user.name + "은(는) 도서관에 갇혀 한턴 쉽니다."
        user.library = False
    elif user.station == True:
        goStation(user, other)
    else:
        user.position += getDice()
        if user.position > 15:
            user.money += 200000
            user.position = user.position % 16
        arrive(user, other)


def getDice():
    global diceNum
    diceNum = diceValue = (random.randrange(6) + 1)
    return diceValue


def arrive(user, other):
    global str
    if landList[user.position].rentable:
        if landList[user.position].owner == 0:
            buy(user, other)
        elif landList[user.position].owner == user.num:
            upgrade(user, other)
        else:
            pay(user, other)
    elif landList[user.position].name == '시작':
        str = "시작점입니다!"
    elif landList[user.position].name == '도서관':
        library(user, other)
    elif landList[user.position].name == '골뱅이':
        drink(user, other)
    elif landList[user.position].name == '화전역':
        station(user, other)


def buy(user, other):
    global str
    global priceStr
    if user.money > landList[user.position].price:
        str = "Player :" + user.name + "," + landList[user.position].name + "을(를) 사시겠습니까?    가격 :"
        priceStr = landList[user.position].price


def upgrade(user, other):
    global str
    global priceStr
    upgradePrice = int(landList[user.position].price * landList[user.position].grade / 10)
    if user.money > upgradePrice:
        if landList[user.position].grade != 3:
            priceStr = upgradePrice
            str = " Player :" + user.name + "," + landList[user.position].name + "을(를) 업그레이드하시겠습니까?가격 :"


def pay(user, other):
    global str
    global priceStr
    str = " "
    user.money -= int(landList[user.position].price * landList[user.position].grade / 2)
    other.money += int(landList[user.position].price * landList[user.position].grade / 2)
    if user.money < 0:
        bankruptcy(user, other);
    if landList[user.position].grade != 3:
        landPrice = int(landList[user.position].price * (1 + landList[user.position].grade / 10))
        if user.money > landPrice:
            priceStr = landPrice
            str = " Player :" + user.name + "," + landList[user.position].name + "을(를) 사시겠습니까?\n 가격 :"


def library(user, other):
    global str
    user.library = True
    str = user.name + "은(는) 도서관에 갇혔습니다. 다음턴을 쉬게 됩니다."

def drink(user, other):
    global str
    str = user.name + "은(는) 술을 엄청 마셨습니다. 200000원을 사용했습니다"
    user.money -= 200000
    if user.money < 0:
            bankruptcy(user, other)



def station(user, other):
    global str
    str = "200000원을 지불하고 다음턴에 원하는 곳으로 가시겠습니까?"

def goStation(user, other):
    global str
    str = "원하는 지역의 이름을 입력하세요"

def bankruptcy(user, other):
    global str
    global bankruptcyTemp
    str = user.name + "이(가) 파산했습니다!!"
    bankruptcyTemp = True

def answerGo(user1, user2):
    global answer1
    if user1.station == True:
        for i in range(0, 16):
            if landList[i].name == answer1:
                user1.position = i
                if i<12:
                    user1.money += 200000
                break
        user1.station = False
        arrive(user1, user2)
    elif user1.position == 12:
        if answer1 == 'Y':
            user1.money -= 200000
            user1.station = True
    else:
        if answer1 == 'Y':
            user1.money -= priceStr
            if landList[user1.position].owner==0:
                landList[user1.position].owner = user1.num
                landList[user1.position].grade = 1
            elif landList[user1.position].owner==user1.num:
                landList[user1.position].grade += 1
            elif landList[user1.position].owner!=user1.num:
                landList[user1.position].owner = user1.num
                landList[user1.position].grade += 1

landList.append(land('시작', 0, False))
landList.append(land('과학관', 100000, True))
landList.append(land('마산국수', 100000, True))
landList.append(land('삼호정', 150000, True))
landList.append(land('도서관', 0, False))
landList.append(land('장수감자탕', 200000, True))
landList.append(land('센트럴파크', 300000, True))
landList.append(land('기계관', 400000, True))
landList.append(land('골뱅이', 200000, False))
landList.append(land('전자관', 300000, True))
landList.append(land('두꺼비', 200000, True))
landList.append(land('학관', 400000, True))
landList.append(land('화전역', 200000, False))
landList.append(land('꼬기꼬기', 500000, True))
landList.append(land('캠퍼스당구장', 400000, True))
landList.append(land('강의동', 1000000, True))

majorList.append('소프트웨어학과')
majorList.append('항공전자정보공학부')
majorList.append('항공우주기계공학부')
majorList.append('경영학과')
majorList.append('항공교통물류법학과')
majorList.append('자율전공')
majorList.append('항공운항과')
majorList.append('재료공학과')
majorList.append('JAZZING YOU')

indexList.append(positionIndex(375, 360, 375, 370))
indexList.append(positionIndex(375, 270, 375, 280))
indexList.append(positionIndex(375, 180, 375, 190))
indexList.append(positionIndex(375, 90, 375, 100))
indexList.append(positionIndex(375, 0, 375, 10))
indexList.append(positionIndex(290, 0, 290, 10))
indexList.append(positionIndex(200, 0, 200, 10))
indexList.append(positionIndex(110, 0, 110, 10))
indexList.append(positionIndex(20, 0, 20, 10))
indexList.append(positionIndex(20, 90, 20, 100))
indexList.append(positionIndex(20, 180, 20, 190))
indexList.append(positionIndex(20, 270, 20, 280))
indexList.append(positionIndex(20, 360, 20, 370))
indexList.append(positionIndex(110, 360, 110, 370))
indexList.append(positionIndex(200, 360, 200, 370))
indexList.append(positionIndex(290, 360, 290, 370))

def start_turn(request,name1,name2):

    user_1 = UserInfo.objects.get(name=name1)
    user_2 = UserInfo.objects.get(name=name2)
    turn(user_1,user_2)
    user_1.save()
    user_2.save()
    return HttpResponseRedirect("/game/{}/{}/".format(user_1.name, user_2.name))

def game(request,name1,name2):
    global count
    if(count<2):
        user_1 = UserInfo.objects.get(name=name1)
        user_2 = UserInfo.objects.get(name=name2)
        '''users1=(user1,user_1.major)
        users2=(user2,user_2.major)
        users1.position=user_1.position
        users2.position=user_2.position'''
        print("test:")
        user_1.num=1
        user_2.num=2
        user_1.save()
        user_2.save()
        '''users1.num=user_1.num
        users2.num_user_2.num'''

    elif(count>=2):
        user_1 = UserInfo.objects.get(name=name1)
        user_2 = UserInfo.objects.get(name=name2)

        '''users1 = user(name1, major1)
        users2 = user(name2, major2)
        users1.position = int(position1)
        users2.position = int(position2)
        users1.countOfVictory = int(countOfVictory1)
        users2.countOfVictory = int(countOfVictory2)
        users1.money = int(money1)
        users2.money = int(money2)
        users1.num = int(num1)
        users2.num = int(num2)
        users1.library = library1
        users2.library = library2
        users1.station = station1
        users2.station = station2'''
    count=count+1
    #turn(user_1, user_2)
    return render(request, "bluemarble_app/index.html",{'user1': user_1, 'user2': user_2,
                  'indexList1': indexList[user_1.position], 'indexList2': indexList[user_2.position],  'landList1' : landList[1], 'landList2' : landList[2]
   , 'landList3' : landList[3], 'landList5' : landList[5], 'landList6' : landList[6], 'landList7' : landList[7], 'landList9' : landList[9]
   , 'landList10' : landList[10], 'landList11' : landList[11], 'landList13' : landList[13], 'landList14' : landList[14], 'landList15' : landList[15], 'turnTemp' : turnTemp
   , 'str' : str, 'priceStr' : priceStr, 'diceNum' : diceNum, 'bankruptcyTemp' : bankruptcyTemp})

def answer(request,name1,name2):
    global answer1
    user_1 = UserInfo.objects.get(name=name1)
    user_2 = UserInfo.objects.get(name=name2)
    #user_name = request.POST.get('name', False)
    userAnswer = request.POST.get('v', False)
    answer1 = userAnswer
    if turnTemp == 2:
        answerGo(user_1,user_2)
    elif turnTemp == 1:
        answerGo(user_2,user_1)
    user_1.save()
    user_2.save()
    return HttpResponseRedirect("/game/{}/{}/".format(user_1.name, user_2.name))
    '''return render(request, 'bluemarble_app/index.html', {'user1' : user_1, 'user2' : user_2,
   'indexList1' : indexList[user_1.position], 'indexList2' : indexList[user_2.position], 'landList1' : landList[1], 'landList2' : landList[2]
   , 'landList3' : landList[3], 'landList5' : landList[5], 'landList6' : landList[6], 'landList7' : landList[7], 'landList9' : landList[9]
   , 'landList10' : landList[10], 'landList11' : landList[11], 'landList13' : landList[13], 'landList14' : landList[14], 'landList15' : landList[15], 'turnTemp' : turnTemp
   , 'str' : str, 'priceStr' : priceStr, 'diceNum' : diceNum})'''
