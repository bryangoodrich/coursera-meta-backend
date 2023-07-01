from django.test import TestCase, Client
from .models import Menu


class MenuViewTest(TestCase):
    def setUp(self):
        Menu.objects.create(Title='Shrimp scampi', Price=10.99, Inventory=8)
        Menu.objects.create(Title='Carbanara', Price=14.99, Inventory=20)
        Menu.objects.create(Title='Cheesecake', Price=9.99, Inventory=16)

    def test_getall(self):
        response = self.client.get("/restaurant/menu")
        self.assertEqual(response.status_code, 200)
        
        menu_items = Menu.objects.all().order_by('Price')
        resp_items = response.data['results']
        self.assertEqual(len(resp_items), len(menu_items))
        
        for response_item, menu_item in zip(resp_items, menu_items):
            self.assertEqual(response_item['Title'], menu_item.Title)
            self.assertEqual(response_item['Price'], str(menu_item.Price))
            self.assertEqual(response_item['Inventory'], menu_item.Inventory)
