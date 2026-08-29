class Employee:
    def __init__(self,name,employee_id,basic_salary,bonus):
        self.name = name
        self.employee_id = employee_id
        self.basic_salary = basic_salary
        self.bonus = bonus

    def calculate_salary(self):
        return self.basic_salary + self.bonus

class Manager(Employee):
    def __init__(self,name,employee_id,basic_salary,bonus_percentage):
        super().__init__(name,employee_id,basic_salary, basic_salary * bonus_percentage)
        self.bonus_percentage = bonus_percentage

    def calculate_salary(self):
        return super().calculate_salary()


if __name__ == "__main__":
    e = Manager("John",1,50000,0.1)
    print(e.calculate_salary())
    p = Manager("Priya",2,60000,0.15)
    print(p.calculate_salary())
