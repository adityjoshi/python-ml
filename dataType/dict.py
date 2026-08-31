# d = {
#     "a":10,
#     "b":20,
#     "c":30
# }
# print(d)

# d["d"] = 40
# print(d)

# di =  [{"Name":"adi","Age":25},
#     {"Name":"lakshita","Age":21},
#     {"Name":"gaurav","Age":25},
#     {"Name":"Dhattu","Age":22}]

# print(di)

# print(d.keys())

# for key in di:
#     print(key)

# for k in di:
#     print(k["Name"])

# for k in di:
#    print(k["Age"])

# #sort dict
# x = sorted(di,key=lambda x:x["Name"])
# print(x)

# for i in di:
#     i["Name"] = i["Name"].lower()
# print("lower case")
# print(di)

# y = sorted(di, key=lambda x: x["Age"], reverse=True)
# print(y)





# def filter_plants_by_criteria(plants,plant_type,min_posts):
#     list = []
#     for plant in plants:
#         if plant["type"] == plant_type and plant["pots_available"] >=min_posts:
#             list.append(plant)
#     print(list)

# def sort_plants_by_availability(plants):
#     result = sorted(plants, key=lambda x:x["pots_available"], reverse=True)
#     print(list(result))

# def summarize_totals(plants):
#     di = {}

#     for x in plants:
#         if x["type"] not in di:
#             di[x["type"]] = 0
#             di[x["type"]] += x["pots_available"]
#         else:
#             di[x["type"]] += x["pots_available"]

#     print(di)

#     for i,j in di.items():
#         print(i,j)

# if __name__ == "__main__":
#     plants = [
#     {"name": "Rose", "type": "Flower", "sunlight": "Full Sun", "pots_available": 4},
#     {"name": "Tulip", "type": "Flower", "sunlight": "Full Sun", "pots_available": 9},
#     {"name": "Basil", "type": "Herb", "sunlight": "Partial Sun", "pots_available": 6}    ]
#     plant_type = "Flower"
#     min_pots = 3

#     filter_plants_by_criteria(plants,plant_type,min_pots)
#     print()
#     sort_plants_by_availability(plants)
#     print()
#     summarize_totals(plants)


class GymMembership:
    def __init__(self,member_name,plan,cost_per_class):
        self.member_name = member_name
        self.plan = plan
        self.cost_per_class = cost_per_class

    def monthly_cost(self,num_classes):
        try:
            if num_classes > 0:
                return float(self.cost_per_class * num_classes)

            else:
                raise ValueError("Number of classes must be greater than 0")
        except ValueError as e:
            print(e)

class PremiumMembership(GymMembership):
    def __init__(self,member_name,plan,sessions_per_class,price_per_session):
        super().__init__(member_name,plan,sessions_per_class*price_per_session)
        self.session_per_class = sessions_per_class
        self.price_per_session = price_per_session

    def monthly_cost(self, num_classes):
        return super().monthly_cost(num_classes)


class EliteMembership(PremiumMembership):
    def __init__(self,member_name,plan,sessions_per_class,price_per_session,monthly_access_fee):
        super().__init__(member_name,plan,sessions_per_class,price_per_session)
        self.monthly_access_fee = monthly_access_fee

    def monthly_cost(self, num_classes):
        return super().monthly_cost(num_classes) + self.monthly_access_fee


if __name__ == "__main__":
    m = GymMembership("Ravi Kumar", "Standard", 8.0)
    m.monthly_cost(12)
    pm = PremiumMembership("Anita Rao", "Premium", 2.0, 15.0)
    pm.monthly_cost(10)
    em = EliteMembership("Karan Mehta", "Elite", 2.5, 12.0, 500.0)
    em.monthly_cost(8)
    m = GymMembership("Ravi Kumar", "Standard", 8.0)
    m.monthly_cost(-3)
