import pymysql
from admin import *
from visitor import *
from user import *

while True:
    identity = input("图书管理系统，请输入数字选择身份登录！以回车结束。\n1.管理员\n2.用户\n3.访客\n")  
    
    # 管理员的
    if identity == "1":
        username = input("请输入学工号：")
        password = input("请输入密码：")
        status = adminlogin(aid = username, apassword = password)
        if status == 0:
            continue

        else:
            func = input("请输入要执行的操作：1: 借书 2: 还书 3: 添加书籍 4: 添加用户 5: 删除用户 6: 退出\n")
            if func == "1":
                while(True):
                    username1 = input("请输入要借书用户的学工号：")
                    password1 = input("请输入要借书用户的密码：")
                    status1 = testuser(uid = username1, upassword = password1)
                    if status1 == 0:
                        break
                    else:
                        bname = input("请输入要借的书名：")
                        adminborrow(aid = username, cid = username1, b_name = bname)
                        break

            if func == "2":
                while(True):
                    username1 = input("请输入要还书用户的用户名：")
                    bname = input("请输入要还的书名：")
                    adminreturn(username1, bname)
                    break

            if func == "3":
                while(True):
                    print("请输入要添加的书籍的以下信息，如插入结束，请在书号处输入#号")
                    bid = input("请输入要添加的ISBN（假的，我们这里默认是8位）：")
                    if bid == "#":
                        break
                    bname = input("请输入要添加的书名：")
                    btype = input("请输入要添加的书的类型：")
                    bpublish = input("请输入要添加的书的出版社：")
                    byear = input("请输入要添加的书的出版年份：")
                    bprice = input("请输入要添加的书的价格：")
                    bauthor = input("请输入要添加的书的作者：")
                    bstock = input("请输入要添加的书的库存：")
                    adminaddbook(bid = bid, bname = bname, btype = btype, bprice = bprice, bpublisher = bpublish, byear = byear, bauthor = bauthor, bstock = bstock)
                    continue

            if func == "4":
                uid = input("请输入要添加的用户的学工号（默认是7位）：")
                username = input("请输入要添加的用户的姓名：")
                password = input("请输入要添加的用户的密码：")
                department = input("请输入要添加的用户的部门：")
                while(True):
                    utype = input("请输入要添加的用户的类型：1: 学生 2: 老师\n")
                    if(utype != "1" and utype != "2"):
                        print("输入错误！")
                        continue
                    else:
                        break
                adminadduser(uid, username, department, password, utype)

            if func == "5":
                uid = input("请输入要删除的用户的学工号（默认是7位）：")
                admindeleteuser(uid)

            if func == "6":
                print("欢迎下次再来！")
                break

    # 用户的
    if identity == '2':
        username = input("请输入学工号：")
        password = input("请输入密码：")
        status = userlogin(uid = username, upassword = password)
        if status == 0:
            continue
        else:
            func = input("请输入要执行的操作：1: 修改姓名 2: 修改密码 3: 修改部门 4: 退出\n")
            if func == "1":
                userchname(username)

            if func == "2":
                userchpassword(username)

            if func == "3":
                userchdepartment(username)

            if func == "4":
                print("欢迎下次再来！")
                break 


    # 访客的
    if identity == '3':
        print("欢迎访客！")
        func = input("请选择您需要的功能！1:查询指定图书，2: 查看所有图书，3：退出\n")
        if func == '1':
            book_name = input("请输入要查询的书名：")
            find_book(book_name)

        if func == '2':
            show_all_book()

        if func == '3':
            print("欢迎下次再来！")
            break