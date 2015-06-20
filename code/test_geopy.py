from geopy.geocoders import GoogleV3


geolocator = GoogleV3()
location = geolocator.geocode("175 5th Avenue NYC")

location = geolocator.reverse("57.05,9.93")
print location