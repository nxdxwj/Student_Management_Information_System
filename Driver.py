import tkinter as tk
from StudentList import StudentList, StudentManagementGUI

if __name__ == '__main__':
    # 创建一个StudentList实例并连接到数据库
    studentList = StudentList()
    studentList.connect('test.db')

    # 创建Tkinter根窗口
    root = tk.Tk()

    # 创建StudentManagementGUI实例，传递根窗口和StudentList实例
    app = StudentManagementGUI(root)

    # 启动Tkinter主循环
    root.mainloop()

    # 关闭数据库连接
    studentList.close()
