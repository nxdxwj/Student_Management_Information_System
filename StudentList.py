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
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.root.grid_columnconfigure(0, weight=1)

        frame = tk.Frame(self.root)
        frame.grid(row=1, column=0, ipadx=10, ipady=10)
        ttk.Button(frame, text="展示学生信息", command=self.show_students).grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(frame, text="添加学生信息", command=self.add_student).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(frame, text="查找/删除/更新学生信息", command=self.modify_student).grid(row=1, column=2, padx=5,
                                                                                           pady=5)
        ttk.Button(frame, text="排序成绩", command=self.sort_student).grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(frame, text="保存数据", command=self.save_data).grid(row=1, column=4, padx=5, pady=5)
        ttk.Button(frame, text="绘制成绩图表", command=self.plot_scores).grid(row=1, column=5, padx=5, pady=5)
        ttk.Button(frame, text="退出系统", command=self.root.quit).grid(row=1, column=6, padx=5, pady=5)
        # Create text box
        self.text = tk.Text(self.root, width=120, height=20)
        self.text.grid(row=2, column=0, columnspan=6, padx=10, pady=10)

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
        def save_new_student():
            id = int(entry_id.get())
            name = entry_name.get()
            major = entry_major.get()
            year = entry_year.get()
            math = int(entry_math.get())
            physics = int(entry_physics.get())
            python = int(entry_python.get())
            self.db.add(id, name, major, year, math, physics, python)
            add_student_win.destroy()
            messagebox.showinfo("Success", "Student added successfully")

        add_student_win = tk.Toplevel(self.root)
        add_student_win.title("Add Student")

        tk.Label(add_student_win, text="学号:").grid(row=0, column=0)
        entry_id = tk.Entry(add_student_win)
        entry_id.grid(row=0, column=1)

        tk.Label(add_student_win, text="姓名:").grid(row=1, column=0)
        entry_name = tk.Entry(add_student_win)
        entry_name.grid(row=1, column=1)

        tk.Label(add_student_win, text="专业:").grid(row=2, column=0)
        entry_major = tk.Entry(add_student_win)
        entry_major.grid(row=2, column=1)

        tk.Label(add_student_win, text="年级:").grid(row=3, column=0)
        entry_year = tk.Entry(add_student_win)
        entry_year.grid(row=3, column=1)

        tk.Label(add_student_win, text="高等数学:").grid(row=4, column=0)
        entry_math = tk.Entry(add_student_win)
        entry_math.grid(row=4, column=1)

        tk.Label(add_student_win, text="大学物理:").grid(row=5, column=0)
        entry_physics = tk.Entry(add_student_win)
        entry_physics.grid(row=5, column=1)

        tk.Label(add_student_win, text="Python程序设计基础:").grid(row=6, column=0)
        entry_python = tk.Entry(add_student_win)
        entry_python.grid(row=6, column=1)

        ttk.Button(add_student_win, text="保存", command=save_new_student).grid(row=7, column=1)

    def modify_student(self):
        modify_win = tk.Toplevel(self.root)
        modify_win.title("查找/删除/更新学生信息")

        def find_student():
            student_id = int(entry_id.get())
            student = self.db.find_by_id(student_id)
            if student:
                entry_name.insert(0, student[2])
                entry_major.insert(0, student[3])
                entry_year.insert(0, student[4])
                entry_math.insert(0, student[5])
                entry_physics.insert(0, student[6])
                entry_python.insert(0, student[7])
            else:
                messagebox.showerror("Error", "Student not found")

        def delete_student():
            student_id = int(entry_id.get())
            self.db.delete(student_id)
            messagebox.showinfo("Success", "Student deleted successfully")

        def update_student():
            student_id = int(entry_id.get())
            name = entry_name.get()
            major = entry_major.get()
            year = entry_year.get()
            math = int(entry_math.get())
            physics = int(entry_physics.get())
            python = int(entry_python.get())
            self.db.update_by_id(student_id, math, physics, python)
            messagebox.showinfo("Success", "Student updated successfully")

        tk.Label(modify_win, text="学号:").grid(row=0, column=0)
        entry_id = tk.Entry(modify_win)
        entry_id.grid(row=0, column=1)

        tk.Label(modify_win, text="姓名:").grid(row=1, column=0)
        entry_name = tk.Entry(modify_win)
        entry_name.grid(row=1, column=1)

        tk.Label(modify_win, text="专业:").grid(row=2, column=0)
        entry_major = tk.Entry(modify_win)
        entry_major.grid(row=2, column=1)

        tk.Label(modify_win, text="年级:").grid(row=3, column=0)
        entry_year = tk.Entry(modify_win)
        entry_year.grid(row=3, column=1)

        tk.Label(modify_win, text="高等数学:").grid(row=4, column=0)
        entry_math = tk.Entry(modify_win)
        entry_math.grid(row=4, column=1)

        tk.Label(modify_win, text="大学物理:").grid(row=5, column=0)
        entry_physics = tk.Entry(modify_win)
        entry_physics.grid(row=5, column=1)

        tk.Label(modify_win, text="Python程序设计基础:").grid(row=6, column=0)
        entry_python = tk.Entry(modify_win)
        entry_python.grid(row=6, column=1)

        ttk.Button(modify_win, text="查找学生信息", command=find_student).grid(row=7, column=0)
        ttk.Button(modify_win, text="删除学生信息", command=delete_student).grid(row=7, column=1)
        ttk.Button(modify_win, text="更新学生信息", command=update_student).grid(row=7, column=2)

    def sort_student(self):
        sort_win = tk.Toplevel(self.root)
        sort_win.title("排序成绩")

        def show_sorted_students(sort_func):
            self.text.delete(1.0, tk.END)
            sorted_students = sort_func()
            for student in sorted_students:
                self.text.insert(tk.END, student)
                self.text.insert(tk.END, "\n")

        def show_sorted_students(sort_func):
            self.text.delete(1.0, tk.END)
            if sort_func == self.db.sort_collegePhysics:
                title = "按大学物理成绩排序结果"
            elif sort_func == self.db.sort_programming:
                title = "按Python成绩排序结果"
            elif sort_func == self.db.sort_math:
                title = "按高等数学成绩排序结果"
            else:
                title = "排序结果"
            self.text.insert(tk.END, f"{'=' * 50}\n{title}\n{'=' * 50}\n")
            sorted_students = sort_func()
            for student in sorted_students:
                self.text.insert(tk.END, student)
                self.text.insert(tk.END, "\n")

        def show_sorted_students(sort_func):
            self.text.delete(1.0, tk.END)
            if sort_func == self.db.sort_collegePhysics:
                title = "按大学物理成绩排序结果"
            elif sort_func == self.db.sort_programming:
                title = "按Python成绩排序结果"
            elif sort_func == self.db.sort_math:
                title = "按高等数学成绩排序结果"
            else:
                title = "排序结果"
            rows = self.db.cur.fetchall()
            self.text.insert(tk.END, "{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\t{:<10}\n".format(
                "序号", "学号", "姓名", "专业", "年级", "高等数学", "大学物理", "Python程序设计基础"))
            for row in rows:
                self.text.insert(tk.END, "{:<8}\t{:<15}\t{:<8}\t{:<10}\t{:<15}\t{:<14}\t{:<17}\t{:<13}\n".format(*row))

            sorted_students = sort_func()
            for student in sorted_students:
                self.text.insert(tk.END, student)
                self.text.insert(tk.END, "\n")

        ttk.Button(sort_win, text="按大学物理成绩排序",
                   command=lambda: show_sorted_students(self.db.sort_collegePhysics)).grid(row=0, column=0, padx=10,
                                                                                           pady=10)
        ttk.Button(sort_win, text="按Python成绩排序",
                   command=lambda: show_sorted_students(self.db.sort_programming)).grid(row=0, column=1, padx=10,
                                                                                        pady=10)
        ttk.Button(sort_win, text="按高等数学成绩排序", command=lambda: show_sorted_students(self.db.sort_math)).grid(
            row=0, column=2, padx=10, pady=10)

    def save_data(self):
        self.db.save()
        messagebox.showinfo("Success", "Data saved successfully")

    def plot_scores(self):
        self.db.plot_subject_scores()

    def on_closing(self):
        self.db.close()
        self.root.destroy()










