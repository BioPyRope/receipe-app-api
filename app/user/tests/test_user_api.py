from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model #方法
from django.core.exceptions import ObjectDoesNotExist,ValidationError
from rest_framework.test import APIClient
from rest_framework import status #class??

## path
PATH_USER_CREATE=reverse("user:create")
##

def createUser(arg):
    
    return get_user_model().objects.create_user(**arg)

class USER_API(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_with_userapi(self):
        ''' test create_user_with_userapi '''
        
        payload={
            "email":"test134@example.com",
            "password":"testpass123",
            "user_name": "johnwick"
        }
        
        #todo_Q: Is it res return a USER? have info? 
        
        res = self.client.post(PATH_USER_CREATE,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        
        #comfirm: status & user/payload password are match
      
        user = get_user_model().objects.get(email=payload["email"])
        QQ=("user",user)
        self.assertTrue(user.check_password(payload["password"]),msg=QQ)
       
       
        self.assertNotIn("password",res.data)

    def test_create_user_with_userapi_shortPassword(self):
        ''' test create_user_with_userapi '''
        
        payload={
            "email":"test134@example.com",
            "password":"11",
            "user_name": "johnwick"
        }
      
        res = self.client.post(PATH_USER_CREATE,payload)
        
        user=get_user_model().objects.filter(email=payload["email"]).exists()
        
        
        #comfirm: status & user cant created
        
        self.assertFalse(user)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
       
    def test_create_user_with_userapi_emailExisted(self):
        ''' test create_user_with_userapi --handle emailExisted '''
        
        payload={
            "email":"test134@example.com",
            "password":"pass1234",
            "user_name": "johnwick"
        }
        
        dummy_user=createUser(payload)
        
        res = self.client.post(PATH_USER_CREATE,payload)
        
        #comfirm: status & user cant created
        
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
       


#