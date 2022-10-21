import pymysql

def find_book(book_name):
    visitor_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'visitor', password = 'VisitorPassword', db = 'LibraryManagement')
    try:
        with visitor_connection.cursor() as cursor:
            sql = 'SELECT title, author, year, stock from book where title = "%s"' % book_name
            cursor.execute(sql)
            res = cursor.fetchall()
            print("找到啦！您要的书《" + str(res[0][0]) + "》(" + str(res[0][1]) + "著，" + str(res[0][2]) + "年出版)，库存还有" + str(res[0][3]) + "本！\n")
    except:
        print("我们这里没有您想要的书！\n")
        return 0
    return 1


def show_all_book():
    visitor_connection = pymysql.connect(host = 'localhost', port = 3306, user = 'visitor', password = 'VisitorPassword', db = 'LibraryManagement')

    try:
        with visitor_connection.cursor() as cursor:
            show_all_books_sql = 'SELECT * from book'
            cursor.execute(show_all_books_sql)
            res = cursor.fetchall()
    except:
        print("出现了一些小错误\n")
        return
    print("您想要的书有：\n")
    for i in res:
        print("《" + str(i[2]) + "》(" + str(i[5]) + "著，" + str(i[4]) + "年出版)，库存还有" + str(i[8]) + "本！")
    return