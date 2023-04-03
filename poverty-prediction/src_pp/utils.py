import math

def create_lat_lon_square(square_size_in_km, lat_val, lon_val):
    """
    Create a square of size `square_size_in_km` around a point 
    given in latitude and longitude
    """

    lat_distance = 111 # km, roughly constant everywhere
    lon_distance = 111.320*math.cos(math.radians(lat_val))

    # https://stackoverflow.com/questions/1253499/simple-calculations-for-working-with-lat-lon-and-km-distance
    # https://stackoverflow.com/questions/9875964/how-can-i-convert-radians-to-degrees-with-python

    v_lat_delta = 1/(lat_distance/square_size_in_km) * 0.5
    v_lon_delta = 1/(lon_distance/square_size_in_km) * 0.5
    
    # set grid
    grid = (lat_val - v_lat_delta, lon_val - v_lon_delta, \
            lat_val + v_lat_delta, lon_val + v_lon_delta)
    
    return grid

create_lat_lon_square(10, 8, 9)

