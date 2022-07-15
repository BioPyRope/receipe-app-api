'''
Test custom Model
'''

#SIMPLE? What's different?

from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Recipes
from rest_framework.test import APIClient
from rest_framework import status #class??




def create_user(user_info={
    "email":"test@example.com",
    "password":"testpassword1234",
    "user_name":"testMan1234"
}):
    
    user=get_user_model().objects.create(user_info)
    return user

class Model_test(TestCase):
    
    def test_create_user_model_success(self):
        '''Test creating user with email & password  '''
        
        test_email = "test@example.com"
        test_password = "test1234"
        
        user=get_user_model().objects.create_user(email=test_email,
                                             password=test_password,user_name="qq123")
        self.assertEqual(user.email, test_email)
        self.assertTrue(user.check_password(test_password))
        
    def test_std_email(self):
        test_emails = [["test1@EXAMPLE.com","test1@example.com"],
                       ["Test2@example.com","Test2@example.com"],
                       ["TEST3@example.com","TEST3@example.com"],
                       ["test4@example.COM","test4@example.com"],
                       ]
        test_password = "test1234"
        
        for em,exp in test_emails:
            user=get_user_model().objects.create_user(email=em,
                                             password=test_password,user_name="qq123")
            self.assertEqual(user.email,exp)
    
    def test_email_noinput_error(self):
        
        with self.assertRaises(ValueError):
              user=get_user_model().objects.create_user(email="em",
                                             password="test_password",user_name="qq123")
    
    def test_superuser_create(self):
        
        admin=get_user_model().objects.create_superuser(email="Admin1@example.com",password="test_password",user_name="qq123")
        
        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
   

     
