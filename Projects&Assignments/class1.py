class Student(object):
    """
    Student class for data of a student
    """
    def __init__(self,name,age,gender,Class,subject,subgrades):
        self.name=name
        self.age=age
        self.gender=gender
        self.Class=Class
        self.subject=subject
        self.subgrades=subgrades
    def getName(self):
        """
        get name
        :return: name
        """
        return self.name
    def getAge(self):
        """
        get age
        :return: age
        """
        return self.age
    def getGender(self):
        """
        get gender
        :return: gender
        """
        return self.gender
    def getClass(self):
        """
        get class
        :return: class
        """
        return self.Class
    def getSubject(self):
        """
        get subject
        :return: subject
        """
        return self.subject
    def getGrades(self):
        """
        get grades
        :return: grades
        """
        return self.subgrades
    def setName(self,name):
        """
        :param name: new name
        :return: None
        """
        self.name=name
    def setAge(self,age):
        """
        :param age:new age
        :return: None
        """
        self.age=age
    def setGender(self,gender):
        """
        :param gender: new gender
        :return: None
        """
        self.gender=gender
    def setClass(self,Class):
        """
        :param Class: new class
        :return: None
        """
        self.Class=Class
    def setSubject(self,subject):
        """
        :param subject: new subject
        :return: None
        """

        self.subject=subject
    def setGrades(self,subgrages):
        """
        :param subgrages: new grades for each subject
        :return: None
        """
        self.subgrades=subgrages
    def avgGrades(self):
        """
        :return: average grades for each subject
        """

        q=0
        sum=0
        for i in self.getGrades():
            q+=1
            sum+=i
        return sum/q
    def showGradesLevel(self):
        """
        :return: the grades level for avegrades
        """
        k=self.avgGrades()
        if k < 60:
            return "D"
        elif k < 70:
            return "C"
        elif k<80:
            return "B"
        else:
            return "A"
    def __str__(self):
        """
        print out
        :return: a string containing all data for the student
        """

        return self.getName()+" "+ str(self.getAge())+" "+self.getGender()+" " +self.getClass()+ ' '+ str(self.getSubject())+" "+str(self.getGrades())

class TEST(Student):
    """
    take the Student into a test
    """
    def __init__(self,student):
        self.subject=student.getSubject()
        self.grades=student.getGrades()
        self.avg=student.avgGrades()
    def predict(self):
        """
        :return: predict the grade for the student
        """
        return "from "+str(self.avg-5)+" to "+str(self.avg+5)

a=Student("Rick",7,"M","S2C1",["Math","CS","Man","Eco"],[89,70,66,90])
a.setAge(16)
print(a)
b=TEST(a)
print(b.predict())
