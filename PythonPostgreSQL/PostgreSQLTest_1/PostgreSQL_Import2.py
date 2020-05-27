# -*-coding:utf-8-*-

import psycopg2

# 通过connect方法创建数据库连接
conn = psycopg2.connect(dbname="ZYTest", user="postgres", password="123456", host="127.0.0.1", port="5432")

# 创建cursor以访问数据库
cur = conn.cursor()
# 创建表
cur.execute('create table student(id serial primary key,student_name varchar(20),age int ,class_name varchar(20));')

# 插入数据
cur.execute("insert into student (student_name,age,class_name) values('p1',15,'class3');\
insert into student (student_name,age,class_name) values('p2',26,'class3');\
insert into student (student_name,age,class_name) values('p3',13,'class2');")

# 查询并打印(读取Retrieve)
cur.execute("select * from student")
rows = cur.fetchall()
print('--------------------------------------------------------------------------------------')
for row in rows:
    print('id=' + str(row[0]) + ' student_name=' + str(row[1]) + 'age =' + str(row[2]) + ' class_name=' + str(row[3]))
print('--------------------------------------------------------------------------------------\n')

# 提交事务
conn.commit()

# 关闭连接
conn.close()