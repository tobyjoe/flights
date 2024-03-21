from FlightRadar24 import FlightRadar24API
import time
import sys
import math

try:
    import unicornhathd as unicorn
    print("16x16 unicorn detected")
except ImportError:
    from unicorn_hat_sim import unicornhathd as unicorn

unicorn.clear()

this = sys.modules[__name__]
this.bounds = []
this.flights = []
this.sightings = []
this.my_airports = ["IAD", "BWI", "DCA"]
this.home = [117,210,71]#[37,167,124]
this.away = [252,76,2]#[237,95,28]
this.landing = [67,89,255]
def setup():
    this.fr_api = FlightRadar24API()
    this.bounds = this.fr_api.get_bounds_by_point(39.047569, -77.202663, 35000)#16093
    unicorn.rotation(-90)
    unicorn.clear()
    unicorn.brightness(0.2)
    print("Setup complete.")

def update():
    this.flights = this.fr_api.get_flights(bounds = this.bounds)
    this.flights.sort(key=lambda x: x.altitude, reverse=True)
    print(len(this.flights))

def draw():
    unicorn.clear()
    x = 0
    alt_unit = 600/16
    print("***")
    for f in this.flights:
        if f.destination_airport_iata == "" or f.altitude < 10:
            continue

        if x >= 15:
            break
            x = 0
        else:
            x = x+1
        if f.origin_airport_iata in this.my_airports:
            color = this.home
        elif f.destination_airport_iata in this.my_airports:
            color = this.landing
        else:
            color = this.away

        max_y = math.ceil(int(f.ground_speed / alt_unit))
        if max_y > 15: max_y = 15
        if max_y < 1: max_y = 1
        # print(f"Number: {f.number}\nX: {x}\nOrig: {f.origin_airport_iata}\nDest: {f.destination_airport_iata}\nMax Y: {max_y}\nAltitude: {f.altitude}\n")
        print(f"Altitude: {f.altitude}")
        for y in range(0, 15):
            if y >= max_y:
                unicorn.set_pixel(x, y, 0, 0, 0)
            else:
                unicorn.set_pixel(x, y, *color)

    #unicorn.set_pixel(0, 0, 0, 0, 0)
    unicorn.show()
    time.sleep(3)

def shutdown():
    unicorn.clear()
    unicorn.off()

# flights = fr_api.get_flights(bounds = bounds)
# for f in flights:
#     flight_details = fr_api.get_flight_details(f)
#     pprint(flight_details)