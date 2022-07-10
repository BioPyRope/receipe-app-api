'''
Test custom Model
'''

#SIMPLE? What's different?
from django.test import TestCase
from django.contrib.auth import get_user_model


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
        
        
        