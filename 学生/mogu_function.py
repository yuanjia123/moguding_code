import urllib.request as ur
import ssl
import json
import random
import datetime

context = ssl._create_unverified_context()


# 登录函数
def Login(login_data):
    request_data = ur.Request(
        url='https://api.moguding.net:9000/session/user/v1/login',
        data=json.dumps(login_data).encode(),
        headers={'Content-Type': 'application/json; charset=UTF-8'}
    )
    try:
        token = json.loads(ur.urlopen(request_data, context=context).read().decode())[
            'data']['token']
        if token:
            return {
                'code': '200',
                'info': '登录成功',
                'token': token
            }
    except Exception as e:
        if str(e) == '<urlopen error Remote end closed connection without response>':
            return {
                'code': '404',
                'info': '网络链接超时'
            }
        else:
            return {
                'code': '505',
                'info': '账号或密码错误'
            }


# 签到函数
def SignIn(token, point):
    request_data = ur.Request(
        url='https://api.moguding.net:9000/attendence/clock/v1/save',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(point).encode("utf-8"))
    try:
        if json.loads(ur.urlopen(request_data, context=context).read().decode())['code'] == 200:
            return True
        else:
            return False
    except Exception as e:
        print(e)


# 获取PlanID
def GetPlanID(token):
    requst_data = ur.Request(
        url='https://api.moguding.net:9000/practice/plan/v1/getPlanByStu?state=1',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps('').encode("utf-8")
    )
    try:
        requst = ur.urlopen(requst_data, context=context).read().decode()
        planID = json.loads(requst)['data'][0]['planId']
        return planID
    except Exception as e:
        print(e)
        return 'erro'


# 写日报
def Day(token, planId, title, content):
    day = {"attachments": "", "attachmentList": [], "title": title,
           "content": content, "planId": planId, "reportType": "day"}
    request_data = ur.Request(
        url='https://api.moguding.net:9000/practice/paper/v1/save',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(day).encode("utf-8"))
    try:
        request = ur.urlopen(request_data, context=context).read().decode()
        return json.loads(request)['msg']
    except Exception as e:
        print(e)
        return 'erro'


# 写周报
def Week(token, planId, title, content):
    date = datetime.datetime.now()
    y = date.year
    m = date.month
    startday = date.day-date.isocalendar()[2]+1
    endday = startday+6
    week = {"attachments": "", "attachmentList": [], "title": title, "content": content, "planId": planId,
            "reportType": "week", "weeks": "第"+str(52+date.isocalendar()[1])+"周", "startTime": ""+str(y)+'-'+str(m)+'-'+str(startday)+" 00:00:00", "endTime": ""+str(y)+'-'+str(m)+'-'+str(endday)+" 23:59:59"}

    request_data = ur.Request(
        url='https://api.moguding.net:9000/practice/paper/v1/save',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(week).encode("utf-8"))
    try:
        request = ur.urlopen(request_data, context=context).read().decode()
        return json.loads(request)['msg']
    except Exception as e:
        print(e)
        return 'erro'


# 写月报
def Month(token, planId, title, content):
    month = {"attachments": "", "attachmentList": [], "title": title,
             "content": content, "planId": planId, "reportType": "month"}
    request_data = ur.Request(
        url='https://api.moguding.net:9000/practice/paper/v1/save',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(month).encode("utf-8"))
    try:
        request = ur.urlopen(request_data, context=context).read().decode()
        return json.loads(request)['msg']
    except Exception as e:
        print(e)


# 获取学生日报（day）、周报（week）、月报（month）列表
def GetReports(token, reportType):
    ids = []
    day = {"currPage": 1, "pageSize": 25, "batchId": "", "classId": "",
           "teaId": "", "reportType": reportType, "planId": "", "state": 0}
    request_data = ur.Request(
        url='https://api.moguding.net:9000/practice/paper/v1/list',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(day).encode("utf-8"))
    try:
        request = ur.urlopen(request_data, context=context).read().decode()
        for dayID in json.loads(request)['data']:
            ids.append(dayID['reportId'])
            print('正在获取批阅文件,类型： '+reportType+'  '+dayID['reportId'])
        return ids
    except Exception as e:
        print(e)


# 批阅日报、周报、月报信息
def PassReport(token, reportID):
    print('正在批阅：ID='+reportID)
    post = {"reportId": reportID, "score": 100, "state": 1, "starNum": 5}
    request_data = ur.Request(
        url='https://api.moguding.net:9000/practice/paper/v1/audit',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(post).encode('utf-8')
    )
    try:
        request = ur.urlopen(request_data, context=context).read().decode()
        if json.loads(request)['code'] == '200':
            print('批阅完毕！')
            return True
        else:
            return json.loads(request)['msg']
    except Exception as e:
        print(e)

# 获取补签
def GetLoginInfo(token):
    ids = []
    day = {"currPage":1,"pageSize":25,"batchId":"","startTime":"","endTime":"","state":"APPLYINT","username":"","studentNumber":""}
    request_data = ur.Request(
        url='https://api.moguding.net:9000/attendence/attendanceReplace/v1/list',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(day).encode("utf-8"))
    try:
        request = ur.urlopen(request_data, context=context).read().decode()
        data=json.loads(request)['data']
        for dayID in data:
            ids.append(dayID['attendanceId'])
            print('正在获取批阅文件,类型： 补签  '+dayID['attendanceId'])
        return ids
    except Exception as e:
        print(e)

# 批阅补签
def PassLogin(token,loginid):
    print('正在批阅：ID='+loginid)
    post = {"attendenceIds":[loginid],"comment":"","applyState":1}
    request_data = ur.Request(
        url='https://api.moguding.net:9000/attendence/attendanceReplace/v1/audit',
        headers={
            'Authorization': token,
            'Content-Type': 'application/json; charset=UTF-8'
        },
        data=json.dumps(post).encode('utf-8')
    )
    try:
        request = ur.urlopen(request_data, context=context).read().decode()
        if json.loads(request)['code'] == '200':
            print('批阅完毕！')
            return True
        else:
            return json.loads(request)['msg']
    except Exception as e:
        print(e)

