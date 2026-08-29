class Vehicle:
    def __init__(self,brand:str,model:str,cost_per_km:float):
        self.brand = brand
        self.model = model
        self.cost_per_km = cost_per_km

    def running_cost(self,distance):
        return float(distance * self.cost_per_km)

class ElectricVehicle(Vehicle):
    def __init__(self,brand:str,model:str,kwh_per_km:float,price_per_km:float):
        super().__init__(brand,model,price_per_km)
        self.kwh_per_km = kwh_per_km

    def running_cost(self, distance):
        return float(super().running_cost(distance) * self.kwh_per_km)


if __name__ == "__main__":
    ev = ElectricVehicle("audi","q4",0.18,14)
    print("Electric Vehicle", ev.running_cost(100))

    v = Vehicle("Bwm","X5",9)
    print("Vehicle",v.running_cost(50))
