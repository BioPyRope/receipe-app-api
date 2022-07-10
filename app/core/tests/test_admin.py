'''Test admin is it work??'''

# 要玩 DJANGO TDD: CLIENT要研究研究...

from django.urls import reverse
from django.test import TestCase,Client
from django.contrib.auth import get_user_model

class AdminUserTest(TestCase):
    
    
    def set_up(self):
        
        self.client=Client()
        self.superuser=get_user_model().objects.create_superuser(
            email='adminTest@example.com',
            password="test1234"
        )
        
        self.normaluser=get_user_model().objects.create_user(
            email='mockuser1@example.com',
            password="test1234",
            user_name="fuckA"
        )
        self.client.force_login(self.superuser)
        
    
    def test_admin_getUserList(self):
        self.set_up()
        url=reverse("admin:core_user_changelist")
        res=self.client.get(url)
        
        self.assertContains(res,self.normaluser.user_name) # check normaluser's name in res
        self.assertContains(res,self.normaluser.email) # check normaluser's email in res
    
    def test_admin_changeUser(self):
        self.set_up()
        url=reverse("admin:core_user_change",args=[self.normaluser.id])
        res=self.client.get(url)
       
        self.assertEqual(res.status_code,200)
        
    def test_admin_AddUser(self):
         self.set_up()
         url=reverse("admin:core_user_add")
         res=self.client.get(url)
         print(url)
         self.assertEqual(res.status_code,200)