from django.core.management.base import BaseCommand
from restaurants.models import Restaurant
from opencage.geocoder import OpenCageGeocode
from django.conf import settings

class Command(BaseCommand):
    help = 'Prepopulates the database with a list of Serbian restaurants'

    def handle(self, *args, **kwargs):
        key = settings.OPENCAGE_API_KEY
        geocoder = OpenCageGeocode(key)

        # List of restaurant data
        restaurant_data = [
            {"name": "Tri Šešira", "address": "Skadarska 29, Belgrade, Serbia"},
            {"name": "Little Bay", "address": "Dositejeva 9a, Belgrade, Serbia"},
            {"name": "Kalemegdanska Terasa", "address": "Mali Kalemegdan bb, Belgrade, Serbia"},
            {"name": "Dva Jelena", "address": "Skadarska 32, Belgrade, Serbia"},
            {"name": "Zavičaj", "address": "Gavrila Principa 77, Belgrade, Serbia"},
            {"name": "Lorenzo & Kakalamba", "address": "Cvijićeva 110, Belgrade, Serbia"},
            {"name": "Ambar", "address": "Karađorđeva 2-4, Belgrade, Serbia"},
            {"name": "Restoran Durmitor", "address": "Omladinskih brigada 16a, Belgrade, Serbia"},
            {"name": "Gušti Mora", "address": "Strahinjića Bana 72, Belgrade, Serbia"},
            {"name": "Toro Latin Gastrobar", "address": "Karadjordjeva 2-4, Belgrade, Serbia"},
        ]

        for restaurant in restaurant_data:
            result = geocoder.geocode(restaurant['address'])
            
            if result and len(result):
                lat = result[0]['geometry']['lat']
                lng = result[0]['geometry']['lng']
                restaurant['latitude'] = lat
                restaurant['longitude'] = lng
            else:
                self.stdout.write(self.style.WARNING(f"Could not find coordinates for {restaurant['name']}"))
                restaurant['latitude'] = None
                restaurant['longitude'] = None

        Restaurant.objects.bulk_create(
            [Restaurant(
                name=restaurant['name'],
                address=restaurant['address'],
                latitude=restaurant['latitude'],
                longitude=restaurant['longitude']
            ) for restaurant in restaurant_data]
        )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with Serbian restaurants!'))
