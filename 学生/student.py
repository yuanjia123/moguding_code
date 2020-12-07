import json
import random
import datetime
import xlrd
import mogu_function as mo
import time


#打开excel文件
book = xlrd.open_workbook('account.xlsx')

li_week = [{"积极工作":"人生的确如此，不能让它来找你，是你要找它，去懂它"},
{"敬业":"只有敬业，才能提高自身价值"},
{"加油":"只要思想不滑坡，办法总比困难多。"},
{"相信":"相信你做得到，你一定会做到。不断告诉自己某一件事"},
{"穷富":"穷则独善其身，达则兼善天下。"},
{"观察":"观察走在你前面的人，看看他为何领先，学习他的做法。忙碌的人才能把事情做好，呆板的人只会投机取巧。优柔寡断的人"},
{"领航人":"对于最有能力的领航人风浪总是格外的汹涌。"},
{"今天":"一个今天胜过两个明天。蓝天属于你，白云属于你，东南西"},
{"工作":"工作着的傻子，比躺在床上的聪明人强得多。"},
{"目标":"工作中，你要把每一件小事都和远大的固定的目标结合起"},
{"迎接光明":"当一个人用工作去迎接光明，光明很快就会来照耀着他。"},
{"面前退缩":"不要在工作面前退缩，说这不可能，劳动会使你创造一切。"},
{"奥利给":"办法总比苦难多，加油吧打工人奥利给!!"}]

while True:
    users = []
    # 获取teacher  sheet的数据
    sheet = book.sheet_by_name('students')

    print("行数",sheet.nrows)
    for i in range(1, sheet.nrows):
        c = {"username": sheet.row_values(i)[0],"phone":sheet.row_values(i)[1],"password":sheet.row_values(i)[2],"loginType":sheet.row_values(i)[3]}
        users.append(c)

    print(users)

    for user in users:
        stu_dict = {"phone":user.get('phone'),
                    "password":user.get("password"),
                    'loginType':"android"}

    #
    # user = {"phone": '17609104120', "password": "Hp654321",
    #         "loginType": "android"}
        try:
            login_result = mo.Login(stu_dict)

            #如果登陆成功
            if login_result["code"] == "200":
                print(user.get("username")+'['+str(datetime.datetime.now())+'] 登录成功')

            if login_result["code"] == "200":
                token = login_result['token']
                planId = mo.GetPlanID(token)
                # 获取planId
                if planId != "erro":
                    # 提交数据
                    # 随机列表中的数据  取一个字典
                    k = random.sample(li_week, 1)[0]

                    result = mo.Week(token, planId, list(k.keys())[0], list(k.values())[0])
                    if result != "erro":
                        print("{}:周报撰写成功".format(user.get("username")))
        except:
            print("{}:账号出现问题".format(user.get("username")))
    # 日报
    # if login_result["code"] == "200":
    #     token = login_result['token']
    #     planId = mo.GetPlanID(token)
    #     #获取planId
    #     if planId != "erro":
    #         #提交数据
    #         result = mo.Day(token, planId,"9月4","今天是个好日子")
    #         if result != "erro":
    #             print("赵咪娟:日报撰写成功")

    #周报


    #月报
    # if login_result["code"] == "200":
    #     token = login_result['token']
    #     planId = mo.GetPlanID(token)
    #     #获取planId
    #     if planId != "erro":
    #         #提交数据
    #         result = mo.Month(token, planId,"9月4","这个月是个好日子")
    #         if result != "erro":
    #             print("赵咪娟:月报撰写成功")

    break