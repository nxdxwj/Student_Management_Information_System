import sqlite3
import pandas as pd

class StudentList:
    def __init__(self):
        self.conn = ''
        self.cur = ''
    def connect(self,db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        try:
            sql = '''
            create table studentList (
            序号 integer autoincrement,
            学号 integer ,
            姓名 text,
            专业 text,
            年级 text,
            高等数学 integer,
            大学物理 integer,
            Python程序设计基础 integer,
            )
            '''
            self.cur.execute(sql)
            self.conn.commit()
        except:
            pass

    def close(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def infoProcess(self,db):
        self.connect(db)
        while True:
            self.show_menu()
            s = input("\033[94minfo==> \033[0m").strip().lower()
            if s == "1":
                self.show()
            elif s == "2":
                self.add()
            elif s == "3":
                id = int(input("请输入学生学号："))
                action = input("请选择操作（find/delete/update）：").strip().lower()
                if action == "find":
                    print(self.find_by_id(id))
                elif action == "delete":
                    self.delete(id)
                elif action == "update":
                    self.update_by_id(id)
                else:
                    print("无效操作！")
            elif s == "4":
                keyword = input("请输入要查找的姓名关键字：")
                print(self.find_by_name_keyword(keyword))
            elif s == "5":
                self.__sort_menu()
            elif s == "6":
                self.save()
                print("保存成功")
            elif s == "7":
                print("See you ~")
                break
            else:
                print("\033[91m输入错误\033[0m")
            input("\nPress enter key to continue...")

        self.close()
    def show(self):
        print("{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}"
              .format("序号","学号", "姓名", "专业","年级","高等数学", "大学物理", "Python程序设计基础"))
        sql = 'select * from studentList'
        self.cur.execute(sql)
        rows = self.cur.fetchall()

        for student in rows:
            print('{:<8}\t{:8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}'
                  .format(student[0], student[1], student[2], student[3], student[4],student[5],student[6],student[7]))


    def __enterScore(self, score):
        while True:
            try:
                score = int(input(score))
                if 0 <= score <= 100:
                    return score
                else:
                    print("输入错误，成绩应该在0-100之间")
            except ValueError:
                print("输入错误，请输入一个整数")

    #按照 id 查看学生是否存在
    def __exists(self, id):
        sql = 'select * from studentList where 学号 = ?'
        result = self.cur.execute(sql,(id,))
        rows = result.fetchall()
        if len(rows) >0:
            return True
        return False

    # 按照 name 查看学生是否存在
    def __add(self,id,Name,Major,Year,Math,Physics,Python):
        sql = 'insert into studentList(学号,姓名,专业,年级,高等数学,大学物理,Python程序设计基础) values (?,?,?,?,?,?,?)'
        self.cur.execute(sql,(id,Name,Major,Year,Math,Physics,Python))
        self.conn.commit()
        print("添加成功")

    def add(self):
        while True:
            id = int(input("学号："))
            if self.__exists(id):
                print("该学号已存在，请重新输入！")
                continue
            else:
                name = input("姓名：")
                major = input("专业：")
                year = input("年级：")
                math = self.__enterScore("高等数学成绩：")
                physics = self.__enterScore("大学物理成绩：")
                python = self.__enterScore("Python程序设计基础成绩：")
                self.__add(id,name,major,year,math,physics,python)
                choice = input("继续添加（y/n）？").lower()
                if choice == "n":
                    break

    def find_by_id(self, id):
        sql = 'select * from studentList where 学号 = %d' %id
        self.cur.execute(sql)
        data = self.cur.fetchall()
        return data[0]

    def find_by_name_keyword(self, name):
        sql = 'select * from studentList where 姓名 = ?'
        self.cur.execute(sql, (name,))
        data = self.cur.fetchall()
        return data[0]

    def __delete(self,id):
        sql = 'delete from studentList where 学号 = ?'
        self.cur.execute(sql,(id,))
        self.conn.commit()
    def delete(self, id):
        if self.__exists(id):
            self.__delete(id)
            print("学生信息已删除！")
            return
        print("未找到该学生信息！")

    def __update(self,id,math,physics,python):
        sql = 'update studentList set 高等数学=?, 大学物理=?, Python程序设计基础=? where 学号=?'
        self.cur.execute(sql,(math,physics,python,id))
        self.conn.commit()
    def update_by_id(self, id):
        student = self.find_by_id(id)
        if student:
            print("学生信息已找到：")
            print('{:<8}\t{:8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}'
                  .format(student[0], student[1], student[2], student[3], student[4], student[5], student[6],
                          student[7]))
            print("请输入更新后的信息：")
            math = self.__enterScore("高等数学成绩：")
            physics = self.__enterScore("大学物理成绩：")
            python = self.__enterScore("Python程序设计基础成绩：")
            self.__update(id,math,physics,python)
            print("学生信息已更新！")
        else:
            print("未找到该学生信息！")

    def show_menu(self):
        print("\n" + "-" * 40)
        print("{: ^30}".format("学生基本信息管理系统"))
        print("-" * 40)
        print(" {:<3} {:<30}|".format("1)", "展示学生信息"))
        print(" {:<3} {:<30}|".format("2)", "添加学生信息"))
        print(" {:<3} {:<23}|".format("3)", "根据学号查找、删除、更新学生信息"))
        print(" {:<3} {:<25}|".format("4)", "根据姓名关键字查找学生信息"))
        print(" {:<3} {:<31}|".format("5)", "保存数据"))
        print(" {:<3} {:<31}|".format("6)", "结束系统"))
        print("-" * 40)



    def save(self):
        sql = 'select * from studentList'
        self.cur.execute(sql)
        data = self.cur.fetchall()
        data = [[student[1], student[2], student[3], student[4], student[5], student[6], student[7]] for student in data]
        df = pd.DataFrame(data, columns=["学号", "姓名", "专业", "年级", "高等数学","大学物理","Python程序设计基础"])
        # 将数据写入Excel文件
        df.to_excel('studentlist.xlsx', index=False)

    def __show_sort_menu(self):
        print("\n" + "-" * 40)
        print("{: ^30}".format("学生基本信息管理系统"))
        print("-" * 40)
        print(" {:<3} {:<30}|".format("1)", "按高等数学成绩排序"))
        print(" {:<3} {:<30}|".format("2)", "按大学物理成绩排序"))
        print(" {:<3} {:<23}|".format("3)", "按Python程序设计基础排序"))
        print("-" * 40)

    def __sort_menu(self, db):
        self.connect(db)
        while True:
            self.__show_sort_menu
            s = input("\033[94minfo==> \033[0m").strip().lower()
            if s == "1":
                self.sort_advancedMathematics()
            elif s == "2":
                self
            elif s == "3":
                self
            else:
                print("\033[91m输入错误\033[0m")
            input("\nPress enter key to continue...")

    def sort_advancedMathematics(self):
        sql = 'select * from studentList'
        self.cur.execute(sql)
        data = self.cur.fetchall()
        mathList = [student[5] for student in data]
        mathList.sort(reverse = True)

        sql = 'select * from studentlist where 高等数学=?'
        print("{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}"
              .format("序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"))
        for each_student_math in data:
            self.cur.excute(sql,(each_student_math,))
            student = self.cur.fetchall()
            print('{:<8}\t{:8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}'
                .format(student[0], student[1], student[2], student[3], student[4], student[5], student[6], student[7]))

    def sort_collegePhysics(self):
        sql = 'select * from studentList'
        self.cur.execute(sql)
        data = self.cur.fetchall()
        mathList = [student[6] for student in data]
        mathList.sort(reverse=True)

        sql = 'select * from studentlist where 大学物理=?'
        print("{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}"
              .format("序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"))
        for each_student_physics in data:
            self.cur.excute(sql, (each_student_physics,))
            student = self.cur.fetchall()
            print('{:<8}\t{:8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}'
                  .format(student[0], student[1], student[2], student[3], student[4], student[5], student[6], student[7]))
