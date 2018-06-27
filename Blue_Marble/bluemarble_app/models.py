from django.db import models

# Create your models here.
from django.db import models

#player 정보 class명 playerInfo
class UserInfo(models.Model):

    name = models.CharField(max_length =10)
    major = models.CharField(max_length=10)
    countOfVictory = models.IntegerField(default = 0)
    position = models.IntegerField(default=0)
    num = models.IntegerField(default = 0)
    money = models.IntegerField(default=3000000)
    library = models.BooleanField(default=False)
    station = models.BooleanField(default=False)

    def __str__(self):
        return self.name
# 방 정보 class명 Room
class RoomInfo(models.Model):
    name = models.CharField(max_length = 15)
    full = models.IntegerField(default=0)
    user1 = models.CharField(max_length=15,default = 'none')
    user2 = models.CharField(max_length=15,default = 'none')
    major1 = models.CharField(max_length=10,default = 'none')
    major2 = models.CharField(max_length=10,default = 'none')
    countOfVictory1 = models.IntegerField(default = 0)
    countOfVictory2 = models.IntegerField(default = 0)
# Player1,2 , 방 가득찬 경우 Room_full

# 게임판 정보 board, num는 방 번호
class Board(models.Model):
    board = models.TextField(max_length = 200)
    room_num = models.IntegerField(default=0)

class RoomMaster(models.Model):
   name=models.CharField(max_length=10)