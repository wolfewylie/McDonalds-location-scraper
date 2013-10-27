import re
import urllib
import time
import csv
from pygeocoder import Geocoder

topcolumns = ['Address', 'City', 'Province', 'Postal', 'Phone', 'lat', 'long']

MacFile = csv.writer(file('DoubleChecking.csv','a'),dialect='excel')
MacFile.writerow(topcolumns)

def provincescraper(every_province, provinceURL): 
	provincepagesource = urllib.urlopen(provinceURL)
	provincepagesource = provincepagesource.read()
	for every_city in re.finditer('value="(.+?)">', provincepagesource): 
		every_city = every_city.group(1)
		basecityurl = "http://www.worksforme.ca/services/communicator.asp?rnd=6477&act=loadLocTable&city="
		basecityurlmiddle = "&province="
		basecityurlender = "&lang=en"
		cityURL = basecityurl + every_city + basecityurlmiddle + every_province + basecityurlender
		cityscraper(cityURL, every_province, every_city)

def cityscraper(cityURL, every_province, every_city):
	citypagesource = urllib.urlopen(cityURL)
	citypagesource = citypagesource.read()
	for every_restaurant in re.finditer('class="location">(.+?)<\/div>', citypagesource, re.S|re.DOTALL): 
		restaurantscraper(every_restaurant, every_province, every_city)
		time.sleep(5)

def restaurantscraper(every_restaurant, every_province, every_city):
	MacFile = csv.writer(file('DoubleChecking.csv','a'),dialect='excel')
	city = every_city
	province = every_province
	if re.search('\D\d\D \d\D\d', every_restaurant.group(1)): 
		postal = re.search('\D\d\D \d\D\d', every_restaurant.group(1))
		postal = postal.group(0)
	else:
		postal = "not available"
	address = re.search('<\/b><br \/>\s(\d?\D?(.+?))<br \/>', every_restaurant.group(1), re.S)
	address = address.group(2)
	address = re.sub('\t', '', address)
	if re.search('<em>(.+?)<\/em>', every_restaurant.group(1)):
		phone = re.search('<em>(.+?)<\/em>', every_restaurant.group(1))
		phone = phone.group(1)
	else:
		phone = "not available"
	geocodingstring = address + ", " + city + ", " + province + ", Canada"
	try: 
		latlong = Geocoder.geocode(geocodingstring)
		latlong = (latlong[0].coordinates)
	except:
		latlong = "unavailable"
	row_data = [address, city, province, postal, phone, latlong]
	MacFile.writerow(row_data)
	print row_data

provincelist = ['BC', 'AB', 'SK', 'MB', 'ON', 'QC', 'NB', 'NS', 'NL', 'YT', 'NT', 'PE']

for every_province in provincelist: 
	baseprovinceurl = "http://www.worksforme.ca/services/communicator.asp?rnd=11233&act=loadCities&province="
	baseprovinceurlender = "&lang=en"
	provinceURL = baseprovinceurl + every_province + baseprovinceurlender
	provincescraper(every_province, provinceURL)