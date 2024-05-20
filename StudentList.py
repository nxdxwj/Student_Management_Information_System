import Student
import pandas as pd


class StudentList:
    def __init__(self):
        self.studentList = []

    def infoProcess(self):
        while True:
            self.show_menu()
            s = input("\033[94minfo==> \033[0m").strip().lower()
            if s == "1":
                self.show()
            elif s == "2":
                self.add()
            elif s == "8":
                break
            elif s == "3":
                id = int(input("请输入学生学号："))
                action = input("请选择操作（find/delete/update）：").strip().lower()
                if action == "find":
                    student = self.find_by_id(id)
                    if student:
                        print("学生信息已找到：")
                        print("学号：", student.id)
                        print("姓名：", student.name)
                        print("语文成绩：", student.Chinese)
                        print("数学成绩：", student.Math)
                        print("英语成绩：", student.English)
                        print("总分：", student.totalScore)
                    else:
                        print("未找到该学生信息！")
                elif action == "delete":
                    self.delete(id)
                elif action == "update":
                    self.update_by_id(id)
                else:
                    print("无效操作！")
            elif s == "4":
                keyword = input("请输入要查找的姓名关键字：")
                results = self.find_by_name_keyword(keyword)
                if results:
                    print("查找结果：")
                    for student in results:
                        print("学号：", student.id)
                        print("姓名：", student.name)
                        print("语文成绩：", student.Chinese)
                        print("数学成绩：", student.Math)
                        print("英语成绩：", student.English)
                        print("总分：", student.totalScore)
                else:
                    print("未找到匹配的学生信息！")
            elif s == "5":
                self.save()
                print("保存成功")
            elif s == "6":
                self.load()
                print("导入成功!")
            elif s == "7":
                self.sort_by_subject()

            else:
                print("\033[91m输入错误\033[0m")
            input("\nPress enter key to continue...")
    def show(self):
        print("{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}"
              .format("学号", "姓名", "语文", "数学", "英语", "总分"))
        for student in self.studentList:
            print('{:<8}\t{:8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}'
                  .format(student.id, student.name, student.Chinese, student.Math, student.English, student.totalScore))

    def sort_by_subject(self):
        subject = input("请选择要按照哪个科目排序（语文/数学/英语/总分）：").strip().lower()
        if subject == "语文":
            self.sort_by_chinese()
        elif subject == "数学":
            self.sort_by_math()
        elif subject == "英语":
            self.sort_by_english()
        elif subject == "总分":
            self.sort_by_total_score()
        else:
            print("无效的科目选择！")
            return
        print("按照{}成绩排序完成：".format(subject))
        self.show_sorted()
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
        for student in self.studentList:
            if student.id == id:
                return True
        return False

    # 按照 name 查看学生是否存在
    def __exists(self, name):
        for student in self.studentList:
            if student.name == name:
                return True
        return False

    def add(self):
        while True:
            id = input("学号：")
            if self.__exists(id):
                print("该学号已存在，请重新输入！")
                continue
            else:
                name = input("姓名：")
                Chinese = self.__enterScore("语文成绩：")
                Math = self.__enterScore("数学成绩：")
                English = self.__enterScore("英语成绩：")
                totalScore = Chinese + Math + English
                student = Student.Student(id, name, Chinese, Math, English, totalScore)
                self.studentList.append(student)
                choice = input("继续添加（y/n）？").lower()
                if choice == "n":
                    break

    def find_by_id(self, id):
        for student in self.studentList:
            if student.id == id:
                return student
        return None

    def find_by_name_keyword(self, keyword):
        results = []
        for student in self.studentList:
            if keyword.lower() in student.name.lower():
                results.append(student)
        return results

    def delete(self, id):
        for student in self.studentList:
            if student.id == id:
                self.studentList.remove(student)
                print("学生信息已删除！")
                return
        print("未找到该学生信息！")

    def update_by_id(self, id):
        student = self.find_by_id(id)
        if student:
            print("学生信息已找到：")
            print("学号：", student.id)
            print("姓名：", student.name)
            print("语文成绩：", student.Chinese)
            print("数学成绩：", student.Math)
            print("英语成绩：", student.English)
            print("请输入更新后的信息：")
            student.name = input("姓名：")
            student.Chinese = self.__enterScore("语文成绩：")
            student.Math = self.__enterScore("数学成绩：")
            student.English = self.__enterScore("英语成绩：")
            print("学生信息已更新！")
        else:
            print("未找到该学生信息！")

    def show_menu(self):
        print("\n" + "-" * 40)
        print("{: ^30}".format("学生基本信息管理系统"))
        print("-" * 40)
        print(" {:<3} {:<30}|".format("1)", "展示学生信息"))
        print(" {:<3} {:<30}|".format("2)", "添加学生信息"))
        print(" {:<3} {:<24}|".format("3)", "根据学号查找、删除、更新学生信息"))
        print(" {:<3} {:<26}|".format("4)", "根据姓名关键字查找学生信息"))
        print(" {:<3} {:<31}|".format("5)", "保存数据"))
        print(" {:<3} {:<31}|".format("6)", "导入数据"))
        print(" {:<3} {:<30}|".format("7)", "将成绩排序"))
        print(" {:<3} {:<31}|".format("8)", "结束系统"))
        print("-" * 40)



    def save(self):
        data = [[student.id, student.name, student.Chinese, student.Math, student.English] for student in self.studentList]
        df = pd.DataFrame(data, columns=["学号", "姓名", "语文", "数学", "英语"])
        # 将数据写入Excel文件
        df.to_excel('StudentList.xlsx', index=False)

    def load(self):
        df = pd.read_excel("studentList.xlsx")
        df_li = df.values.tolist()
        for each_student in df_li:
            id = each_student[0]
            name = each_student[1]
            Chinese = each_student[2]
            Math = each_student[3]
            English = each_student[4]
            student = Student.Student(id, name, Chinese, Math, English, Chinese + Math + English)
            self.studentList.append(student)

    def sort_by_chinese(self):
        self.studentList.sort(key=lambda x: x.Chinese, reverse=True)

    def sort_by_math(self):
        self.studentList.sort(key=lambda y: y.Math, reverse=True)

    def sort_by_english(self):
        self.studentList.sort(key=lambda z: z.English, reverse=True)

    def sort_by_total_score(self):
        self.studentList.sort(key=lambda x: x.totalScore, reverse=True)

    def show_sorted(self):
        print("{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}"
              .format("学号", "姓名", "语文", "数学", "英语", "总分"))
        for student in self.studentList:
            print('{:<8}\t{:8}\t{:<8}\t{:<8}\t{:<8}\t{:<8}'
                  .format(student.id, student.name, student.Chinese, student.Math, student.English, student.totalScore))
