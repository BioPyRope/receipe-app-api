

from django.test import TestCase, testcases
from django.urls import reverse
from django.contrib.auth import get_user_model #方法
from rest_framework.test import APIClient
from rest_framework import status #class??
from core.tests.testTool import *

## path
PATH_USER_CREATE=reverse("user:create")
PATH_AUTH_TOKEN=reverse("user:token")
PATH_ME=reverse("user:me")
##

def legency_stdOutWarper(func):
    capturedOutput = io.StringIO()                  # Create StringIO object
    sys.stdout = capturedOutput 
    
    def wrapper(arg):
        try:
           
            res= func(arg)
            sys.stdout = sys.__stdout__                     # Reset redirect.
            print ('Captured', capturedOutput.getvalue())   # Now works as before.
            return res 
        
        except:
            
            sys.stdout = sys.__stdout__
            
            raise  ValueError ('CapturedError', capturedOutput.getvalue())   # See below.
    
    return wrapper

def createUser(arg):
    
    return get_user_model().objects.create_user(**arg)

class USER_API(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_create_user_with_userapi(self):
        ''' test create_user_with_userapi '''
        
        payload={
            "email":"test134@example.com",
            "password":"aaaaaaaaaaaaaaaaaa",
            "user_name": "johnwick"
        }
        
        #todo_Q: Is it res return a USER? have info? 
        
        res = self.client.post(PATH_USER_CREATE,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        
        #comfirm: status & user/payload password are match
      
        user = get_user_model().objects.get(email=payload["email"])
        QQ=("user",user)
        self.assertTrue(user.check_password("aaaaaaaaaaaaaaaaaa"),msg=QQ)

       
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
       
    def test_create_user_with_userap_emailExisted(self):
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
       
    def test_auth_token(self):
      
        user=createUser({
            "email":"user5551@example.com",
            "password":"pass1234",
            "user_name": "johnwick"
        })
        
        payload={"email":"user5551@example.com",
                 "password":"pass1234"
                 }
        res= self.client.post(PATH_AUTH_TOKEN,payload) #get token
        
        #response
        
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn("token",res.data)
        
    def test_auth_token_bad_cendental(self):
        
        user=createUser({
            "email":"user155@example.com",
            "password":"pass1234",
            "user_name": "johnwick"
        })
        
        payload={"email":"user3@example.com",
                 "password":"pass1234"
                 }
        res= self.client.post(PATH_AUTH_TOKEN,payload) #get token FAIL
        
        #response
        self.assertNotIn("token",res.data)
        self.assertTrue(res.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_auth_token_NoPassword(self):
        
        user=createUser({
            "email":"user9991@example.com",
            "password":"pass1234",
            "user_name": "johnwick"
        })
        
        payload={"email":"user3@example.com",
                 "password":""
                 }
        res= self.client.post(PATH_AUTH_TOKEN,payload) #get token FAIL
        
        #response
        self.assertNotIn("token",res.data)
        self.assertTrue(res.status_code,status.HTTP_400_BAD_REQUEST)

    
    def test_comfirm_NoAuth(self):
        res=self.client.get(PATH_ME)
        
        self.assertTrue(res.status_code,status.HTTP_401_UNAUTHORIZED)

class Meprofile(TestCase):
    
    def setUp(self):
        #做一個強制登入的mock
        self.user=createUser({
            "email":"user5551@example.com",
            "password":"pass1234",
            "user_name": "johnwick"
        })
        self.client=APIClient()
        self.client.force_authenticate(self.user)
    
    def test_MEprofile_auth_get(self):
        res=self.client.get(PATH_ME)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,{
            "email":"user5551@example.com",
            "user_name": "johnwick"
        })
    
    def test_MEprofile_public_get_ERR(self):
        publicUser=APIClient()
        res=publicUser.get(PATH_ME)
        self.assertNotEqual(res.status_code,status.HTTP_200_OK)
        
    def test_MEprofile_notPost(self):
       
        res=self.client.post(PATH_ME)
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
    
    @stdOutWarper
    def test_MEprofile_auth_patch(self):
        
        payload={
           "email":"user5551@example.com",
           "password":"dogg1234",
           
        }
       
        res=self.client.patch(PATH_ME,payload)
        userInfo=get_user_model().objects.get(email=payload["email"])
        print("userInf",type(userInfo))
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(userInfo.email,payload["email"])
        self.assertEqual(userInfo.user_name,self.user.user_name)
        self.assertTrue(userInfo.check_password(payload["password"]))