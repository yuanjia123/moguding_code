import json
import datetime
import xlrd
import mogu_function as mo
import time

users=[]
#打开excel文件
book = xlrd.open_workbook('account.xlsx')

while True:

    user = {"phone": '18391622076', "password": "123456",
            "loginType": "android"}
    login_result = mo.Login(user)

    #如果登陆成功
    if login_result["code"] == "200":
        print('赵咪娟'+'['+str(datetime.datetime.now())+'] 登录成功')

    if login_result["code"] == "200":
        token = login_result['token']
        planId = mo.GetPlanID(token)
        #获取planId
        if planId != "erro":
            #提交数据
            result = mo.Day(token, planId,"9月4","今天是个好日子")
            if result != "erro":
                print("赵咪娟:日报撰写成功")

    if login_result["code"] == "200":
        token = login_result['token']
        planId = mo.GetPlanID(token)
        #获取planId
        if planId != "erro":
            #提交数据
            result = mo.Week(token, planId,"9月4","这周都是个好日子")
            if result != "erro":
                print("赵咪娟:周报撰写成功")

    if login_result["code"] == "200":
        token = login_result['token']
        planId = mo.GetPlanID(token)
        #获取planId
        if planId != "erro":
            #提交数据
            result = mo.Month(token, planId,"9月4","这个月是个好日子")
            if result != "erro":
                print("赵咪娟:月报撰写成功")

    break