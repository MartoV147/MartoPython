import json
class Car:
    is_available = True
    brand = ""

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
    all_cars = []

    #without json
    #all_cars.append(Car("Mazda", "6", 0.10, "BH3565AB", 19.99, 499.99, 3459.99))
    #all_cars.append(Car("VW", "Golf 4", 0.08, "PA2589BH", 15.99, 379.99, 2599.99))
    #all_cars.append(Car("Audi", "A6", 0.11, "PB4296HH", 20.99, 499.99, 3459.99))
    #all_cars.append(Car("Alfa Romeo", "156", 0.07, "E2996XA", 17.99, 429.99, 2999.99))
    #all_cars.append(Car("Mercedes", "C280", 0.10, "BH3565AB", 19.99, 499.99, 3459.99))
    #all_cars.append(Car("BMW", "320", 0.11, "PA2586AH", 15.99, 379.99, 2599.99))
    #all_cars.append(Car("Opel", "Astra", 0.09, "BH2214AB", 19.99, 499.99, 3459.99))
    #all_cars.append(Car("Citroen", "407", 0.08, "CT3369KM", 16.99, 389.99, 2699.99))
    #all_cars.append(Car("Mazda", "3", 0.10, "BH5589AB", 19.99, 499.99, 3459.99))
    #all_cars.append(Car("Lexus", "IS250", 0.08, "A0937TT", 15.99, 379.99, 2599.99))


    #with json
    def __init__(self):
        with open("cars.json", "r") as list:
            data = json.load(list)
            for c in data:
                car = Car(brand = c["brand"], model = c["model"], consumption = c["consumption"],
                          license_plate = c["license_plate"], price_per_hour = c["price_per_hour"],
                          price_per_day = c["price_per_day"], price_per_week = c["price_per_week"])
                self.all_cars.append(car)


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
        if car.is_available:
            list.append(car)
            car.is_available = False
            print("The Car is available and Added to your Order")
        else:
            print("The Car isn't available")

class Order:
    user = User
    cars = []
    price = 0
    hours = 0

    def __init__(self, user, cars, hours):
        self.user = user
        self.cars = cars
        self.hours = hours

    def calculate_price_when_hours_less_than_a_day(self, hours, price_per_hour):
        return price_per_hour * hours
    def calculate_price_when_hours_more_than_a_day(self, hours, price_per_day, price_per_hour):
        days = int(hours / 24)
        hours1 = int(hours % 24)
        return price_per_day * days + price_per_hour * hours1
    def calculate_price_when_hours_more_than_a_week(self, hours, price_per_week, price_per_day, price_per_hour):
        weeks = int(hours / 168)
        hours1 = int(hours % 168)
        days = int(hours1 / 24)
        hours3 = int(hours1 % 24)
        return price_per_week * weeks + price_per_day * days + price_per_hour * hours3

    def calculate_price(self):
        for obj in self.cars:
            if self.hours < 24:
                self.price += self.calculate_price_when_hours_less_than_a_day(self.hours, obj.price_per_hour)

            elif self.hours >= 24 and self.hours < 168:
                self.price += self.calculate_price_when_hours_more_than_a_day(self.hours, obj.price_per_day,
                                                                              obj.price_per_hour)

            elif self.hours >= 168:
                self.price += self.calculate_price_when_hours_more_than_a_week(self.hours, obj.price_per_week,
                                                                               obj.price_per_day, obj.price_per_hour)

        if len(self.cars) > 3:
            self.price *= 0.7

    def get_price(self):
        self.calculate_price()
        return round(self.price, 2)


def main():
    menager = Menager()
    user = User("GoshoV", "GoshoPass", "GoshoMail")

    list = []
    car = menager.all_cars[1]
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

    print("You rented " + str(len(list)) + " car/s for " + str(hours) + " hours and will cost you " + str(price))
    print()
    menager.get_all_available_cars()

main()
