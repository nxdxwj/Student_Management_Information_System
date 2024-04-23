class Student:
    def __init__(self,id,name,Chinese,Math,English):
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
              .format("学号","姓名","语文","数学","英语"))
        for student in self.studentList:
            print('{:8}\t{:8}\t{:<8}\t{:<8}\t{:<8}'
                  .format(student.id,student.name,student.Chinese,student.Math,student.English))

    def __enterScore(self,message):
        while True:
            score = int(input(message))
            if 0 <= score <= 100:
                break
            else:
                print("输入错误，成绩应该在0-100之间")
        return score

    def __exists(self,id):
        for student in self.studentList:
            if student.id == id:
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
                student = Student(id,name,Chinese,Math,English)
                self.studentList.append(student)
                choice = input("继续添加（y/n）？").lower()
                if choice == "n":
                    break

    def infoProcess(self):
        print("--------学生基本信息管理系统--------")
        print("show----------展示学生信息")
        print("add----------添加学生信息")
        print("exit----------结束系统")
        print("----------------------------------")
        while True:
            s = input("info==>").strip().lower()
            if s == "show":
                self.show()
            elif s == "add":
                self.add()
            elif s == "exit":
                break
            else:
                print("输入错误")


if __name__ == '__main__':
    studentList = StudentList()