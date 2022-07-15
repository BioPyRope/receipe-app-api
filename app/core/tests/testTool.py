from django.core.exceptions import ObjectDoesNotExist,ValidationError
import io
import sys
from django.contrib.auth import get_user_model 
'''
stdOutWarper
create_user'''

def stdOutWarper(func):
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

def create_user(user_info={
    "email":"test@example.com",
    "password":"testpassword1234",
    "user_name":"testMan1234"
}):
    
    user=get_user_model().objects.create_user(**user_info)
    return user