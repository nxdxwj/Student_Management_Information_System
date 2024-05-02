class Student:
    def __init__(self, id, name, Chinese, Math, English):
        self.id = id
        self.name = name
        self.Chinese = int(Chinese)
        self.Math = int(Math)
        self.English = int(English)


class StudentList:
    def __init__(self):
        self.studentList = []

    def show(self):
        print("{:8}\t{:8}\t{:8}\t{:8}\t{:8}"
              .format("学号", "姓名", "语文", "数学", "英语"))
        for student in self.studentList:
            print('{:8}\t{:8}\t{:<8}\t{:<8}\t{:<8}'
                  .format(student.id, student.name, student.Chinese, student.Math, student.English))

    def __enterScore(self, message):
        while True:
            try:
                score = int(input(message))
                if 0 <= score <= 100:
                    return score
                else:
                    print("输入错误，成绩应该在0-100之间")
            except ValueError:
                print("输入错误，请输入一个整数")

    def __exists(self, id):
        for student in self.studentList:
            if student.id == id:
                return True
        return False

    def __exists(self,name):
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
                student = Student(id, name, Chinese, Math, English)
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

    def update(self, id):
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
        print("|{: ^30}|".format("学生基本信息管理系统"))
        print("-" * 40)
        print("|{:<3} {:<30}|".format("1)", "展示学生信息"))
        print("|{:<3} {:<30}|".format("2)", "添加学生信息"))
        print("|{:<3} {:<24}|".format("3)", "根据学号查找、删除、更新学生信息"))
        print("|{:<3} {:<26}|".format("4)", "根据姓名关键字查找学生信息"))
        print("|{:<3} {:<31}|".format("5)", "结束系统"))
        print("-" * 40)

    def infoProcess(self):
        while True:
            self.show_menu()
            s = input("\033[94minfo==> \033[0m").strip().lower()
            if s == "1":
                self.show()
            elif s == "2":
                self.add()
            elif s == "3":
                break
            elif s == "4":
                id = input("请输入学生学号：")
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
                    else:
                        print("未找到该学生信息！")
                elif action == "delete":
                    self.delete(id)
                elif action == "update":
                    self.update(id)
                else:
                    print("无效操作！")
            elif s == "5":
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
                else:
                    print("未找到匹配的学生信息！")
            else:
                print("\033[91m输入错误\033[0m")


if __name__ == '__main__':
    studentList = StudentList()
    studentList.infoProcess()
