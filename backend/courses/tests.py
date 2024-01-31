from django.test import TestCase, Client
from django.contrib.auth import get_user_model


User = get_user_model()
    

class TokenTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.superuser = User.objects.create_superuser(
            'my_admin', 'my@ad.min', 'psss'
        )
        self.teacheruser = User.objects.create_user(
            username='Makar', email='ma@ka.ru', password='maka', 
            is_staff = True
        )
        self.studuser = User.objects.create_user(
            username='Luk', email='ta@tu.in', password='force',
            is_staff = False
        )
    
    def PagesPerms(self):
        response = self.client.get('api/v1/rubrics/')
        self.assertEqual(response.status_code, 200,
                         msg='страница рубрики недоступна')
        