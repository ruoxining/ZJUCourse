import pymysql
from visitor import *
import datetime         #用来做目前的时间

def adminlogin(aid, apassword):
    admin_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'admin', password = 'AdminPassword', db = 'LibraryManagement')
    try:
        with admin_connection.cursor() as cursor:
            sql = 'SELECT password from administrator where aid = "%s"' % aid
            cursor.execute(sql)
            res = cursor.fetchone()
    except:
        print("登录失败\n")
        return 0

    if apassword in res:
        return 1

def testuser(uid, upassword):
    admin_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'admin', password = 'AdminPassword', db = 'LibraryManagement')
    try:
        with admin_connection.cursor() as cursor:
            sql = 'SELECT password from card where cid = "%s"' % uid
            cursor.execute(sql)
            res = cursor.fetchone()
            if upassword in res:
                return 1
    except:
        print("您的用户名或密码错误，或您未持有本图书馆借书证～\n")
        return 0

def adminborrow(cid, aid, b_name):
    admin_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'admin', password = 'AdminPassword', db = 'LibraryManagement')
    # get bid
    try:
        with admin_connection.cursor() as cursor:
            sql = 'SELECT bid from book where title = "%s"' % b_name
            cursor.execute(sql)
            res = cursor.fetchone()
            bid = res[0]
    except:
        print("没有查到您想要的书，请检查书名是否输入正确\n")
        return

    if find_book(b_name):
        try:
            with admin_connection.cursor() as cursor:
                sql = 'SELECT stock from book where title = "%s"' % b_name
                cursor.execute(sql)
                res = cursor.fetchone()
                if res[0] <= 0:
                    print("抱歉，该书已经借完了！\n")
                    today = datetime.date.today()
                    try:
                        sql = 'SELECT min(borrow_date) from borrow where bid = "%s"' % bid
                        cursor.execute(sql)
                        res = cursor.fetchone()
                    except:
                        print("出现错误\n")
                        return
                    min_return = res[0] + datetime.timedelta(days=30)
                    print("最早的一次借书日期是"+ str(res[0]) + "，这本书将在" + str(min_return) + "前归还。请在此之后来借这本书～\n")
                    return
        except:
            print("出现错误\n")
            return 0 

    # 增加borrow记录
        today = datetime.date.today()
        oneday = datetime.timedelta(days=1)
        yesterday = today-oneday  
        try:
            with admin_connection.cursor() as cursor:
                sql = 'INSERT into borrow values ("%s", "%s", "%s", "%s", "%s")' % (cid, bid, datetime.date.today(), yesterday, aid)
                cursor.execute(sql)
                admin_connection.commit()
            print("借阅成功\n") 
        except:
            print("借阅失败, 可能是您在同一天已经借阅过相同的书。请先阅读手中的那本，改日再来～\n")
            admin_connection.rollback()
            return

        # 减少book库存
        try:
            with admin_connection.cursor() as cursor:
                sql = 'UPDATE book SET stock = stock - 1 WHERE title = "%s"' % b_name
                cursor.execute(sql)
                admin_connection.commit()
        except:
            print("出现错误\n")
            admin_connection.rollback()
            return



def adminreturn(cid, bname):
    admin_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'admin', password = 'AdminPassword', db = 'LibraryManagement')
    # get bid
    try:
        with admin_connection.cursor() as cursor:
            sql = 'SELECT bid from book where title = "%s"' % bname
            cursor.execute(sql)
            res = cursor.fetchone()
    except:
        print("出现错误\n")
        return
    
    bid = res[0]

    # 判断是否借过这本书
    
    try:
        with admin_connection.cursor() as cursor:
            sql = 'SELECT * from borrow where cid = "%s" and bid = "%s"' % (cid, bid)
            cursor.execute(sql)
            res = cursor.fetchone()
    except:
        print("出现了一些小错误\n")
        return
    if res == None:
        print("这本书你还没借过！\n")
        return

    # 判断是否还过这本书
    admin_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'admin', password = 'AdminPassword', db = 'LibraryManagement')
    try:
        with admin_connection.cursor() as cursor:
            sql = 'SELECT borrow_date, return_date from borrow where cid = "%s" and bid = "%s"' % (cid, bid)
            cursor.execute(sql)
            res = cursor.fetchone()
    except:
        print("出现了一些小错误\n")
        return
    
    today = res[0] 
    oneday = datetime.timedelta(days=1) 
    yesterday = today-oneday  

    if res[1] != yesterday:
        print("这本书你已经还啦！\n")
        return 

    # 增加book库存
    try:
        with admin_connection.cursor() as cursor:
            sql = 'UPDATE book SET stock = stock + 1 WHERE bid = "%s"' % bid
            cursor.execute(sql)
            admin_connection.commit()
    except:
        print("我们出了一点小问题，请重试一下\n")
        admin_connection.rollback()
        return
    # 修改borrow记录
    try:
        with admin_connection.cursor() as cursor:
            sql = 'UPDATE borrow SET return_date = "%s" WHERE cid = "%s" and bid = "%s"' % (datetime.date.today(), cid, bid)
            cursor.execute(sql)
            admin_connection.commit()
            print("还书成功\n")
    except:
        print("我们出了一点小问题，请重试一下\n")
        admin_connection.rollback()
        return


def adminaddbook(bid, btype, bname, byear, bauthor, bprice, bpublisher, bstock):
    admin_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'admin', password = 'AdminPassword', db = 'LibraryManagement')
    try:
        with admin_connection.cursor() as cursor:
            sql = 'INSERT into book values ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (bid, btype, bname, bpublisher, byear, bauthor, bprice, bstock, bstock)
            cursor.execute(sql)
            admin_connection.commit()
            print("添加成功\n")
    except: 
        print("添加失败\n")
        admin_connection.rollback()
        return



def adminadduser(uid, uname, udepartment, upassword, utype):
    admin_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'admin', password = 'AdminPassword', db = 'LibraryManagement')
    try:
        sql = 'SELECT * from card where cid = "%s"' % uid
        with admin_connection.cursor() as cursor:
            cursor.execute(sql)
            res = cursor.fetchone()
        if res != None:
            print("该用户已存在！\n")
            return
    except:
        pass
    try:
        with admin_connection.cursor() as cursor:
            sql = 'INSERT into card values ("%s", "%s", "%s", "%s", "%s")' % (uid, uname, udepartment, upassword, utype)
            cursor.execute(sql)
            admin_connection.commit()
            print("添加成功\n")
    except:
        print("添加失败\n")
        admin_connection.rollback()
        return

def admindeleteuser(uid):
    admin_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'admin', password = 'AdminPassword', db = 'LibraryManagement')
    # 检查这个card有没有没还的书
    try:
        with admin_connection.cursor() as cursor:
            sql = 'SELECT * from borrow where cid = "%s"' % uid
            cursor.execute(sql)
            res = cursor.fetchone()
    except:
        print("出现了一些小错误\n")
        return

    while(True):
        really = input("您确定要删除该用户吗？输入yes / no\n")
        if(really == "no"):
            return
        if(really == "yes"):
            if res != None:
                reallyreally = input("这个读者还有书没还，确定删除嘛？输入yes/no：")
                if(reallyreally == "no"):
                    return
                if(reallyreally == "yes"):
                    try:
                        with admin_connection.cursor() as cursor:
                            sql ='SET foreign_key_checks = 0'
                            cursor.execute(sql)
                            admin_connection.commit() 

                            sql = 'DELETE from card where cid = "%s"' % uid
                            cursor.execute(sql)
                            admin_connection.commit()  
                            
                            sql = 'SET foreign_key_checks = 1'
                            cursor.execute(sql)
                            admin_connection.commit()  
                            print("删除成功！\n")
                            
                    except:
                        print("删除失败，可能是不存在该用户，请重试\n")
                        admin_connection.rollback()
                        return 0

                    return 1

                else:
                    continue
        else:
            continue