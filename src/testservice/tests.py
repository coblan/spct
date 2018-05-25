from django.test import TestCase
from maindb.models import TbAppversion

# Create your tests here.

class AnimalTestCase(TestCase):
    def setUp(self):
        TbAppversion.objects.all().delete()
        TbAppversion.objects.create(terminal = 1, packageurl = 'wooww', required = 1, md5 = 'sssss', versionid = 123, valid = 1)
        #Animal.objects.create(name="lion", sound="roar")
        #Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        print(TbAppversion.objects.count())
        #"""Animals that can speak are correctly identified"""
        #lion = Animal.objects.get(name="lion")
        #cat = Animal.objects.get(name="cat")
        #self.assertEqual(lion.speak(), 'The lion says "roar"')
        #self.assertEqual(cat.speak(), 'The cat says "meow"')