import json
import datetime
import xlrd
import mogu_function as mo
import time

users=[]
#打开excel文件
book = xlrd.open_workbook('account.xlsx')

while True:

    #获取teacher  sheet的数据
    sheet = book.sheet_by_name('teacher')
    # print("行数",sheet.nrows)
    # sheet.nrows获取该sheet当中的有效行数
    for i in range(1, sheet.nrows):
        users.append({"username":sheet.row_values(i)[0],"userinfo":{"phone":str(int(sheet.row_values(i)[1])),"password":sheet.row_values(i)[2],"loginType":sheet.row_values(i)[3]}})

    # user记录所有的老师的账户信息  比如大院{'username': '张莹', 'userinfo': {'loginType': 'Android', 'phone': '18691098998', 'password': 'wyzy19851021'}}
    print("------------------*-----------------------",users)

    date = "D:\\蘑菇丁_{}_{}_{}日报.txt".format(datetime.datetime.now().year, datetime.datetime.now().month,datetime.datetime.now().day)

    with open(date, 'w', encoding='utf-8') as f:
        pass


    for lo in users:
        t=datetime.datetime.now().hour
        print("t是:",t)
        # if t>23 or t<7:
        #     print('晚上上班')
        #     break
        t = 14
        if t == 14 or t == 17:
            print('每天14点或者5点上班')

            print('*'*80)
            print("老师："+lo['username']+' 正在查看报表'+str(datetime.datetime.now()))

            with open(date, 'a', encoding='utf-8') as f:
                f.write("\n\n----------------------------------------------------------------------")
                f.write("\n\n老师：{}\n".format(lo['username']))

            print("+++++++++++++++++",lo)

            response=mo.Login(lo['userinfo'])
            if response['code']=='200':

                token = response['token']
                all_stu_li = mo.GetUsers(token)

                # print("打印全部学生的列表",all_stu_li)
                user_data_stu = []
                for u in all_stu_li:
                    user_data_stu.append(u.get('stuName'))

                # print("打印全部学生的列表", user_data_stu)
                #获取已经签到的学生
                # signed_stu = GetUserLogin(token)
                signed_stu = list(set(mo.GetUserLogin(token)))
                # print("*****已经签到同学有:  {}位，分别是： {}",format(str(len(signed_stu)),str(signed_stu)))
                print("已经签到同学有:  ",len(signed_stu))
                print("分别是：  ",signed_stu)
                for all_stu in user_data_stu:
                    for signed in signed_stu:
                        if signed in user_data_stu:
                            user_data_stu.remove(signed)
                # print("-----未签到同学有:  {}位，分别是： {}",format(str(len(user_data_stu)),str(user_data_stu)))

                with open(date, 'a', encoding='utf-8') as f:


                    f.write("总人数:  {}\n".format(len(all_stu_li)))
                    f.write("已经签到同学有:  {}\n".format(len(signed_stu)))
                    f.write("签到率： {:.2%} ".format(len(signed_stu)/len(all_stu_li)))



                print("-----未签到的同学有:  ", len(user_data_stu))

                for user in user_data_stu:
                    for a_s in all_stu_li:
                        if user == a_s.get('stuName'):
                            print("分别是：  ",len(user_data_stu))
                            print("班级：  ", a_s.get('className'))
                            print("电话：  ", a_s.get('mobile'))
                            print("-"*50)
                            with open(date, 'a', encoding='utf-8') as f:

                                f.write("\n未签到的同学有:  {}   班级: {}   电话：{}".format(user,a_s.get('className'),a_s.get('mobile')))
                                # f.write("\n\n未签到的同学有:  {}".format(user))
                                # f.write("班级：  {}\n".format(a_s.get('className')))
                                # f.write("电话：   {}\n".format(a_s.get('mobile')))
                                # f.write("-"*50)

                for z in range(1,5):
                    #获取补签 ids
                    ids=mo.GetLoginInfo(token)
                    #遍历每一个补签
                    for y in ids:
                        print('正在批阅补签')

                        #批阅补签
                        mo.PassLogin(token,y)
                        time.sleep(2)
                ids=[]
                for id in ['day','week','month']:
                    print('正在获取'+id+'批阅文件')

                    #获取学生日报（day）、周报（week）、月报（month）列表
                    for x in mo.GetReports(token,id):
                        ids.append(x)
                    time.sleep(1)

                for x in ids:
                    #PassReport
                    mo.PassReport(token,x)
                    time.sleep(2)
                print('老师：'+lo['username']+' 现在没有')
                print('='*60)
            else:
                print(lo['username']+":"+response['info'])

    users.clear()
    print('每天执行2次')
    time.sleep(3600)
