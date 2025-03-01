import random
from django.core.management.base import BaseCommand
from menu.models import Food

class Command(BaseCommand):
    help = 'Generates 25 random Serbian dishes and populates the Food model'

    def handle(self, *args, **kwargs):
        # List of random Serbian dishes and descriptions
        dishes = [
            {"name": "Ćevapi", "description": "Grilled minced meat sausages, typically served with flatbread."},
            {"name": "Pljeskavica", "description": "Serbian-style grilled burger made of ground beef or pork."},
            {"name": "Sarma", "description": "Cabbage rolls stuffed with minced meat and rice."},
            {"name": "Karadjordjeva šnicla", "description": "Breaded rolled steak stuffed with cheese and ham."},
            {"name": "Gibanica", "description": "Traditional Serbian cheese pie with layers of pastry and cheese."},
            {"name": "Proja", "description": "Cornbread, a simple but traditional Serbian side dish."},
            {"name": "Ajvar", "description": "Pepper-based condiment, often served as a side or spread."},
            {"name": "Prebranac", "description": "Serbian baked beans with onions, a hearty vegetarian dish."},
            {"name": "Kačamak", "description": "A traditional porridge-like dish made from cornmeal."},
            {"name": "Pasulj", "description": "Serbian bean soup with smoked meat."},
            {"name": "Burek", "description": "Flaky pastry filled with minced meat or cheese."},
            {"name": "Pita sa višnjama", "description": "Cherry pie made with phyllo dough, a sweet Serbian dessert."},
            {"name": "Krofne", "description": "Serbian-style donuts, often filled with jam or custard."},
            {"name": "Musaka", "description": "A layered dish made of potatoes, minced meat, and cream."},
            {"name": "Čorba", "description": "A rich Serbian soup made with meat or fish."},
            {"name": "Riblja čorba", "description": "Traditional Serbian fish soup, served as a starter."},
            {"name": "Podvarak", "description": "Baked sauerkraut with pieces of pork or turkey."},
            {"name": "Pihtije", "description": "Serbian cold meat jelly, made from boiled pork legs."},
            {"name": "Kupus", "description": "Traditional boiled cabbage dish, often served with pork."},
            {"name": "Uštipci", "description": "Serbian fried dough balls, often served as a dessert."},
            {"name": "Baklava", "description": "A sweet dessert made from layers of pastry, nuts, and honey."},
            {"name": "Roštilj", "description": "Mixed grilled meat platter with sausages, steaks, and chops."},
            {"name": "Šopska salata", "description": "Salad made with tomatoes, cucumbers, onions, and cheese."},
            {"name": "Tulumbe", "description": "Sweet syrup-soaked dough pastries, a popular dessert."},
            {"name": "Vanilice", "description": "Serbian sandwich cookies filled with jam and rolled in powdered sugar."}
        ]

        for dish in dishes:
            Food.objects.create(
                name=dish["name"],
                description=dish["description"],
                price=round(random.uniform(5.0, 20.0), 2),  
                is_available=random.choice([True, False])  
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 25 Serbian dishes!'))
