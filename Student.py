class Student:
    def __init__(self, id, name, Chinese, Math, English,totalScore):
        self.id = id
        self.name = name
        self.Chinese = int(Chinese)
        self.Math = int(Math)
        self.English = int(English)
        self.totalScore = int(totalScore)