import json


class Car:


    def __init__(self, brand, model, consumption, license_plate, price_per_hour, price_per_day, price_per_week):
        self.brand = brand
        self.model = model
        self.consumption = consumption
        self.license_plate = license_plate
        self.price_per_hour = price_per_hour
        self.price_per_day = price_per_day
        self.price_per_week = price_per_week
        self.is_available = True


    def __str__(self):
        return self.brand + "; " + self.model + "; " + str(self.consumption) + "; " + self.license_plate + "; " + \
               str(self.price_per_hour) + "; " + str(self.price_per_day) + "; " + str(self.price_per_week) + "; " +\
               str(self.is_available)



class User:


    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email



class Menager:


    def fill_list(self, file_name):
        with open(file_name, "r") as list:
            try:
                data = json.load(list)
                for c in data:
                    car = Car(brand = c["brand"], model = c["model"], consumption = c["consumption"],
                              license_plate = c["license_plate"], price_per_hour = c["price_per_hour"],
                              price_per_day = c["price_per_day"], price_per_week = c["price_per_week"])
                    self.all_cars.append(car)
            except:
                print("An exception occurred")


    def __init__(self, file_name):
        self.all_cars = []
        self.fill_list(file_name)


    def get_all_available_cars(self):
        print("Available Cars: ")
        for obj in self.all_cars:
            if obj.is_available:
                print(obj)


    def get_car_by_brand(self, brand):
        for i in self.all_cars:
            if i.brand == brand:
                return i


    def get_car_by_brand_and_model(self, brand, model):
        for i in self.all_cars:
            if i.brand == brand and i.model == model:
                return i


    def rent_car(self, list, car):
        if car is not None and car.is_available:
            list.append(car)
            car.is_available = False
            print("The Car is available and Added to your Order")
        else:
            print("The Car isn't available")


    def get_nth_car(self, n):
        if n < 0:
            print("Enter Valid Number")
            return

        if len(self.all_cars) <= n:
            print("Can't find that car in the list")
            return

        return self.all_cars[n]



class Order:


    def __init__(self, user, cars, hours):
        self.user = user
        self.cars = cars
        self.hours = hours


    def calculate_price_when_hours_less_than_a_day(self, price_per_hour):
        return price_per_hour * self.hours


    def calculate_price_when_hours_more_than_a_day(self, price_per_day, price_per_hour):
        days = int(self.hours / 24)
        hours1 = int(self.hours % 24)
        return price_per_day * days + price_per_hour * hours1


    def calculate_price_when_hours_more_than_a_week(self, price_per_week, price_per_day, price_per_hour):
        weeks = int(self.hours / 168)
        hours1 = int(self.hours % 168)
        days = int(hours1 / 24)
        hours3 = int(hours1 % 24)
        return price_per_week * weeks + price_per_day * days + price_per_hour * hours3


    def calculate_price(self):
        self.price = 0
        for obj in self.cars:
            if self.hours < 24:
                self.price += self.calculate_price_when_hours_less_than_a_day(obj.price_per_hour)

            elif self.hours >= 24 and self.hours < 168:
                self.price += self.calculate_price_when_hours_more_than_a_day(obj.price_per_day,
                                                                              obj.price_per_hour)

            elif self.hours >= 168:
                self.price += self.calculate_price_when_hours_more_than_a_week(obj.price_per_week,
                                                                               obj.price_per_day, obj.price_per_hour)

        if len(self.cars) > 3:
            self.price *= 0.7


    def get_price(self):
        self.calculate_price()
        return round(self.price, 2)



def main():
    menager = Menager("cars.json")
    #menager = Menager("cars_bad.json") #for exception testing
    #menager = Menager("cars_bad_values.json")

    user = User("GoshoV", "GoshoPass", "GoshoMail")

    list = []
    car = menager.get_nth_car(1)
    car1 = menager.get_car_by_brand("Mazda")
    car2 = menager.get_car_by_brand_and_model("Mazda", "3")
    #car3 = menager.all_cars[1]


    menager.rent_car(list, car)
    menager.rent_car(list, car1)
    menager.rent_car(list, car2)
    #menager.rent_car(list, car3) #this should return that this car isn't available

    hours = 169

    order = Order(user, list, hours)
    price = order.get_price()

    if len(list) == 0:
        print("You can't rent 0 cars")
    else:
        print("You rented " + str(len(list)) + " car/s for " + str(hours) + " hours and will cost you " + str(price))
        print()

    menager.get_all_available_cars()

main()
