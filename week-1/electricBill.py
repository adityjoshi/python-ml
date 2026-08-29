class ResidentialConsumer:
    def __init__(self,consumer_id,units,rate_per_unit):
        self.consumer_id = consumer_id
        self.units = units
        self.rate_per_unit = rate_per_unit

    def calculate_bill(self):
        return self.units * self.rate_per_unit


class CommercialConsumer(ResidentialConsumer):
    def __init__(self,consumer_id,units,rate_per_unit,surcharge_rate):
        self.consumer_id = consumer_id
        self.units = units
        self.rate_per_unit = rate_per_unit
        self.surcharge_rate = surcharge_rate

    def calculate_bill(self):
        return super().calculate_bill()*(1+self.surcharge_rate)



if __name__ == "__main__":
    r = ResidentialConsumer(101,100,5)
    print(r.calculate_bill())
    s = CommercialConsumer(101,250,8,0.15)
    print(s.calculate_bill())
