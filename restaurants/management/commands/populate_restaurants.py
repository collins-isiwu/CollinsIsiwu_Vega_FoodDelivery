from django.core.management.base import BaseCommand
from restaurants.models import Restaurant

class Command(BaseCommand):
    help = 'Prepopulates the database with a list of Serbian restaurants'

    def handle(self, *args, **kwargs):
        # List of restaurant data
        restaurant_data = [
            {"name": "Tri Šešira", "location": "Skadarska 29, Belgrade, Serbia"},
            {"name": "Little Bay", "location": "Dositejeva 9a, Belgrade, Serbia"},
            {"name": "Kalemegdanska Terasa", "location": "Mali Kalemegdan bb, Belgrade, Serbia"},
            {"name": "Dva Jelena", "location": "Skadarska 32, Belgrade, Serbia"},
            {"name": "Zavičaj", "location": "Gavrila Principa 77, Belgrade, Serbia"},
            {"name": "Lorenzo & Kakalamba", "location": "Cvijićeva 110, Belgrade, Serbia"},
            {"name": "Ambar", "location": "Karađorđeva 2-4, Belgrade, Serbia"},
            {"name": "Restoran Durmitor", "location": "Omladinskih brigada 16a, Belgrade, Serbia"},
            {"name": "Gušti Mora", "location": "Strahinjića Bana 72, Belgrade, Serbia"},
            {"name": "Toro Latin Gastrobar", "location": "Karadjordjeva 2-4, Belgrade, Serbia"},
        ]

        # Bulk create restaurant objects
        Restaurant.objects.bulk_create(
            [Restaurant(name=restaurant['name'], location=restaurant['location']) for restaurant in restaurant_data]
        )

        # Output success message
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with Serbian restaurants!'))
