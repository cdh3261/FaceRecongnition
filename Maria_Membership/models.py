from django.db import models
from django.conf import settings


# 가입 유저 모델
class Info(models.Model):
    # name = models.CharField(max_length=30)
    # birthDay = models.CharField(db_column='birthDay', max_length=8)
    # phoneNumber = models.CharField(db_column='phoneNumber', max_length=11, unique=True)
    uID = models.AutoField(primary_key=True)
    isOwner = models.BooleanField(default=False)
    uName = models.CharField(max_length=50)
    uPhone = models.CharField(max_length=11, unique=True)
    uBirthDay = models.CharField(max_length=8)
    uImage = models.CharField(max_length=1, default='')

    class Meta:
        db_table = 'USER'

# 메뉴 모델
class Menu(models.Model):
    user = models.ForeignKey(Info, on_delete=models.CASCADE)
    americano = models.IntegerField()
    latte = models.IntegerField()
    smoothy = models.IntegerField()
    total = models.IntegerField()

    class Meta:
        db_table = 'menu_info'


class Store(models.Model):
    sID = models.AutoField(primary_key=True)
    uID = models.ForeignKey(Info, on_delete=models.CASCADE, db_column="uID")
    sName = models.CharField(max_length=50)
    sPhone = models.CharField(max_length=50)
    class Meta:
        db_table = 'STORE'

class RMENU(models.Model):
    mID = models.AutoField(primary_key=True)
    sID  = models.ForeignKey(Store, on_delete=models.CASCADE, db_column="sID")
    mName = models.CharField(max_length=45)
    mDesc = models.CharField(max_length=45, null=True)
    mPrice = models.IntegerField()
    mImage = models.CharField(max_length=200)

    class Meta:
        db_table = 'MENU'