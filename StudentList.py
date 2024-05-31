import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.simpledialog import askstring, askinteger

# 设置字体路径
font_path = 'C:/Windows/Fonts/SimHei.ttf'  # 修改为实际字体文件路径
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams['font.sans-serif'] = font_prop.get_name()
plt.rcParams['axes.unicode_minus'] = False  # 解决负号 '-' 显示为方块的问题


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


    #按照 id 查看学生是否存在
    def __exists(self, id):
        sql = 'select * from studentList where 学号 = ?'
        result = self.cur.execute(sql,(id,))
        rows = result.fetchall()
        if len(rows) >0:
            return True
        return False

    def add(self,id,name,major,year,math,physics,python):
        sql = 'insert into studentList(学号,姓名,专业,年级,高等数学,大学物理,Python程序设计基础) values (?,?,?,?,?,?,?)'
        self.cur.execute(sql, (id, name, major, year, math, physics, python))
        self.conn.commit()

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

    def __delete(self, id):
        sql = 'delete from studentList where 学号 = ?'
        self.cur.execute(sql, (id,))
        self.conn.commit()

    def delete(self, id):
        if self.__exists(id):
            self.__delete(id)

    def __update(self,id,math,physics,python):
        sql = 'update studentList set 高等数学=?, 大学物理=?, Python程序设计基础=? where 学号=?'
        self.cur.execute(sql,(math,physics,python,id))
        self.conn.commit()
    def update_by_id(self, id,math,physics,python):
        self.__update(id,math,physics,python)

    def sort_collegePhysics(self):
        sql = 'select * from studentList '
        self.cur.execute(sql)
        data = self.cur.fetchall()

        columns = ["序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"]
        df = pd.DataFrame(data=data, columns=columns)
        df.sort_values(by="大学物理", ascending=False, inplace=True)
        data = df.values.tolist()
        return data

    def sort_programming(self):
        sql = 'select * from studentList'
        self.cur.execute(sql)
        data = self.cur.fetchall()

        columns = ["序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"]
        df = pd.DataFrame(data=data, columns=columns)
        df.sort_values(by="Python程序设计基础", ascending=False, inplace=True)
        data = df.values.tolist()
        return data

    def sort_math(self):
        sql = 'select * from studentList'
        self.cur.execute(sql)
        data = self.cur.fetchall()

        columns = ["序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"]
        df = pd.DataFrame(data=data, columns=columns)
        df.sort_values(by="高等数学", ascending=False, inplace=True)
        data = df.values.tolist()
        return data

    def save(self):
        sql = 'select * from studentList'
        self.cur.execute(sql)
        data = self.cur.fetchall()
        data = [[student[1], student[2], student[3], student[4], student[5], student[6], student[7]] for student in data]
        df = pd.DataFrame(data, columns=["学号", "姓名", "专业", "年级", "高等数学","大学物理","Python程序设计基础"])
        # 将数据写入Excel文件
        df.to_excel('studentlist.xlsx', index=False)

    def plot_subject_scores(self):
        try:
            sql = 'SELECT 高等数学, 大学物理, Python程序设计基础 FROM studentList'
            self.cur.execute(sql)
            data = self.cur.fetchall()

            if not data:
                print("No data found in the database.")
                return

            math_scores = [row[0] for row in data]
            physics_scores = [row[1] for row in data]
            python_scores = [row[2] for row in data]

            subjects = ['高等数学', '大学物理', 'Python程序设计基础']
            average_scores = [
                sum(math_scores) / len(math_scores) if math_scores else 0,
                sum(physics_scores) / len(physics_scores) if physics_scores else 0,
                sum(python_scores) / len(python_scores) if python_scores else 0
            ]

            plt.figure(figsize=(10, 6))
            plt.bar(subjects, average_scores, color=['blue', 'green', 'red'])
            plt.xlabel('科目')
            plt.ylabel('平均成绩')
            plt.title('学生平均成绩')
            plt.ylim(0, 100)
            plt.show()

        except sqlite3.Error as e:
            print("Error fetching data:", e)


class StudentManagementGUI:
    def __init__(self, root):
        self.db = StudentList()
        self.db.connect('test.db')

        self.root = root
        self.root.title("学生基本信息管理系统")

        self.create_widgets()

    def create_widgets(self):
        #创建标题
        title_label = tk.Label(self.root, text="欢迎来到学生成绩管理系统", font=("Helvetica", 16))
        title_label.grid(row=0, column=0, padx=10, pady=10,sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)

        frame = tk.Frame(self.root)
        frame.grid(row=1,column=0,ipadx=10, ipady=10)
        ttk.Button(frame, text="展示学生信息", command=self.show_students).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame, text="添加学生信息", command=self.add_student).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="查找/删除/更新学生信息", command=self.modify_student).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(frame,text="排序成绩",command=self.sort_student).grid(row=1,column=3, padx=5, pady=5)
        ttk.Button(frame, text="保存数据", command=self.save_data).grid(row=1, column=4, padx=5, pady=5)
        ttk.Button(frame, text="绘制成绩图表", command=self.plot_scores).grid(row=1, column=5, padx=5, pady=5)
        ttk.Button(frame, text="退出系统", command=self.root.quit).grid(row=1, column=6, padx=5, pady=5)
        #创建文本框
        self.text = tk.Text(self.root, width=120, height=20)
        self.text.grid(row=2, column=0, columnspan=6,padx=10, pady=10)

    def show_students(self):
        self.text.delete(1.0, tk.END)
        sql = 'SELECT * FROM studentList'
        self.db.cur.execute(sql)
        rows = self.db.cur.fetchall()
        self.text.insert(tk.END, "{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
            "序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"))
        for row in rows:
            self.text.insert(tk.END, "{:<8}\t{:<15}\t{:<8}\t{:<10}\t{:<15}\t{:<14}\t{:<17}\t{:<13}\n".format(*row))

    def add_student(self):
        id = askinteger("输入", "学号：")
        name = askstring("输入", "姓名：")
        major = askstring("输入", "专业：")
        year = askstring("输入", "年级：")
        math = askinteger("输入","高等数学成绩：")
        physics = askinteger("输入","大学物理成绩：")
        python = askinteger("输入","Python程序设计基础成绩：")

        self.db.add(id, name, major, year, math, physics, python)
        messagebox.showinfo("信息", "添加成功")

    def modify_student(self):
        id = askinteger("输入", "请输入学生学号：")
        action = askstring("输入", "请选择操作（find/delete/update）：").strip().lower()

        if action == "find":
            student = self.db.find_by_id(id)
            if student:
                self.text.delete(1.0, tk.END)
                self.text.insert(tk.END, "{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
                    "序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"))
                self.text.insert(tk.END, "{:<8}\t{:<15}\t{:<8}\t{:<10}\t{:<15}\t{:<14}\t{:<17}\t{:<13}\n".format(*student))
            else:
                messagebox.showerror("错误", "未找到该学生信息！")
        elif action == "delete":
            self.db.delete(id)
            messagebox.showinfo("信息", "学生信息已删除！")
        elif action == "update":
            student = self.db.find_by_id(id)
            if student:
                math = askinteger("输入","高等数学成绩：")
                physics = askinteger("输入","大学物理成绩：")
                python = askinteger("输入","Python程序设计基础成绩：")
                self.db.update_by_id(id, math, physics, python)
                messagebox.showinfo("信息", "学生信息已更新！")
            else:
                messagebox.showerror("错误", "未找到该学生信息！")
        else:
            messagebox.showerror("错误", "无效操作！")

    def sort_student(self):
        action = askstring("输入","请输入要排序的学科（math,physics,python）：")
        if action == "math":
            self.text.delete("1.0", tk.END)
            data = self.db.sort_math()
            sql = 'select * from studentList where 学号=? and 高等数学=?'
            self.text.insert(tk.END, "{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
                "序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"))
            for each_student_math in data:
                self.db.cur.execute(sql, (each_student_math[1], each_student_math[5]))
                student = self.db.cur.fetchall()[0]
                self.text.insert(tk.END,
                                 "{:<8}\t{:<15}\t{:<8}\t{:<10}\t{:<15}\t{:<14}\t{:<17}\t{:<13}\n".format(*student))
        if action == "physics":
            self.text.delete("1.0", tk.END)
            data = self.db.sort_collegePhysics()
            sql = 'select * from studentList where 学号=? and 大学物理=?'
            self.text.insert(tk.END, "{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
                "序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"))
            for each_student_physics in data:
                self.db.cur.execute(sql, (each_student_physics[1], each_student_physics[6]))
                student = self.db.cur.fetchall()[0]
                self.text.insert(tk.END,
                                 "{:<8}\t{:<15}\t{:<8}\t{:<10}\t{:<15}\t{:<14}\t{:<17}\t{:<13}\n".format(*student))
        if action == "python":
            self.text.delete("1.0", tk.END)
            data = self.db.sort_programming()
            sql = 'select * from studentList where 学号=? and Python程序设计基础=?'
            self.text.insert(tk.END, "{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
                "序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"))
            for each_student_python in data:
                self.db.cur.execute(sql, (each_student_python[1], each_student_python[7]))
                student = self.db.cur.fetchall()[0]
                self.text.insert(tk.END,
                                 "{:<8}\t{:<15}\t{:<8}\t{:<10}\t{:<15}\t{:<14}\t{:<17}\t{:<13}\n".format(*student))


    def save_data(self):
        self.db.save()
        messagebox.showinfo("信息", "保存成功")

    def plot_scores(self):
        self.db.plot_subject_scores()







