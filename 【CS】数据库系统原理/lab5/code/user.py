import pymysql


def userlogin(uid, upassword):
    user_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'user', password = 'UserPassword', db = 'LibraryManagement') 

    try:
        with user_connection.cursor() as cursor:
            sql = 'SELECT password from card where cid = "%s"' % uid
            cursor.execute(sql)
            res = cursor.fetchone()
            if res[0] == upassword:
                return 1
    except:
        print("登录失败\n")
        user_connection.rollback()
        return 0

def userchname(cid):
    user_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'user', password = 'UserPassword', db = 'LibraryManagement') 

    new_name = input("请输入新的姓名：")
    try:
        with user_connection.cursor() as cursor:

            sql = 'UPDATE card SET cname = "%s" WHERE cid = "%s"' % (new_name, cid)
            cursor.execute(sql)
            user_connection.commit()
            print("修改成功！\n")
    except:
        user_connection.rollback()
        print("修改失败\n")


def userchpassword(cid):
    user_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'user', password = 'UserPassword', db = 'LibraryManagement') 

    new_password = input("请输入新的密码：")
    new_password1 = input("请再次输入新的密码进行确认：")
    if new_password == new_password1:
        try:
            with user_connection.cursor() as cursor:
                sql = 'UPDATE card SET password = "%s" WHERE cid = "%s"' % (new_password, cid)
                cursor.execute(sql)
                user_connection.commit()
                print("修改成功！\n")
        except:
            user_connection.rollback()
            print("修改失败\n")


def userchdepartment(cid):
    user_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'user', password = 'UserPassword', db = 'LibraryManagement') 

    new_depart = input("请输入新的部门：")
    try:
        with user_connection.cursor() as cursor:

            sql = 'UPDATE card SET department = "%s" WHERE cid = "%s"' % (new_depart, cid)
            cursor.execute(sql)
            user_connection.commit()
            print("修改成功！\n")
    except:
        user_connection.rollback()
        print("修改失败\n")