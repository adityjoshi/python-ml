class Delivery:
    def __init__(self,delivery_id,distance,cost_per_km):
        self.delivery_id=delivery_id
        self.distance = distance
        self.cost_per_km = cost_per_km
    def calculate_cost(self):
        return self.distance * self.cost_per_km


class ExpressDelivery(Delivery):
    def __init__(self,delivery_id,distance,cost_per_km,priority_multiplier):
        super().__init__(delivery_id,distance,cost_per_km)
        self.priority_multiplier=priority_multiplier

    def calculate_cost(self):
        return super().calculate_cost() * self.priority_multiplier


def main():
    d = ExpressDelivery(102,20,8,1.5)
    s = Delivery(101,10,5)
    ans = d.calculate_cost()
    print(ans)
    print(s.calculate_cost())

if __name__ == "__main__":
    main()
