from geocode import getGeocodeLocation
import json
import httplib2

# from findARestaurant import findARestaurant as FR
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "QDE0GG4AOHLBTXRZHYOMLM1SZTACKI1AJVRFIFXQFYA3RUDN"
foursquare_client_secret = "IJP24LGRTS0BOM4JFSUSHQSQULZN5LYVSJGXPI3CGZEE4R1O"
google_api_key = "AIzaSyA5wflBvVHnNIyMa-mtSXXr430QZygP4Vs"

def fixFoursquare(inputString):
    newstring = inputString.replace("u","")
    return newstring

def getGeocodeLocation(inputString):

    locationString = inputString.replace(" ", "+")
    url = ('https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s' % (locationString, google_api_key))
    h = httplib2.Http()
    response, content = h.request(url,'GET')
    result = json.loads(content)

    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lat']
    return [latitude,longitude]

def findARestaurant(mealType,location):
    coordinates = getGeocodeLocation(location)
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = "https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20171110&ll=%s,%s&query=%s" % (foursquare_client_id, foursquare_client_secret, coordinates[0], coordinates[1], mealType)
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
    return result
    if result['response']['venues']:
        firstRestaurant = result['response']['venues'][0]
        venue_id = firstRestaurant['id']
        restaurant_name = firstRestaurant['name']
        restaurant_address = firstRestaurant['location']['formattedAddress']
        address = ""
        for i in restaurant_address:
            address += i + " "
        restaurant_address = address

        url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&v=20171110&client_secret=%s'% (venue_id,foursquare_client_id,foursquare_client_secret))
        result = json.loads(h.request(url,'GET')[1])
        if result['response']['photos']['items']:
            firstpic = result['response']['photos']['items'][0]
            prefix = firstpic['prefix']
            suffix = firstpic['suffix']
            imageURL = prefix + "300x300" + suffix
        else:
            imageURL = 'http://pixabay.com/get/8926af5eb597ca51ca4c/1433440765/cheeseburger-34314_1280.png?direct'

        restaurantInfo = {'name': restaurant_name, 'address': restaurant_address,'image': imageURL}
        print  "Restaurant Name: %s" % restaurantInfo['name']
        print "Restaurant Address: %s" % restaurantInfo['address']
        print "Image: %s \n" % restaurantInfo['image']
        return restaurantInfo
    else:
        print "No %s Restaurants found for %s" % (mealType, location)
        return "No Restaurants Found"

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
