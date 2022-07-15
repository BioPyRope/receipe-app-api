from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Recipes
from rest_framework.test import APIClient
from rest_framework import status #class??
from decimal import Decimal
from core.tests.testTool import stdOutWarper,create_user
from recipe.serializers import RecipeSerializer,RecipeDetailSerializer
def recipe_create(user,**parm):
        '''check the recipe model create function'''
     
        
        default={
            'title':"fish",
            'time':180,
            'price':Decimal("5.50"),
            'description':"oh-i-shi",
            "link": "None"
        }
        default.update(parm)
        
        newRecipe=Recipes.objects.create(
            user=user, **default #class
           
        )
        return newRecipe

RECIPE_URL=reverse("recipe:recipes-list")

def getRECIPE_URL(recipe_id):
    
    return reverse("recipe:recipes-detail",args=[recipe_id])

print("test_recipeapi")

class Public_recipe_test(TestCase):
    def setUp(self):
        self.client=APIClient() #Mock client no user & auth
        
    @stdOutWarper
    def test_recipe_api_required_auth(self):
        
        res= self.client.get(RECIPE_URL)
        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)
    

class Private_recipe_test(TestCase):
    
    def setUp(self):
        self.user=create_user()
        self.client=APIClient() #Mock client no user & auth
        self.client.force_authenticate(self.user)
        
    
    def test_retrieve_recipes(self):
        """Test retrieving a list of recipes."""
        recipe_create(user=self.user)
        recipe_create(user=self.user)

        res = self.client.get(RECIPE_URL)

        recipes = Recipes.objects.all().order_by('-id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    @stdOutWarper
    def test_recipe_api_getSelfList(self):
        another= create_user(user_info={
            "email":"test2@example.com",
            "password":"testpassword1234",
            "user_name":"another"
        })
        reci_1=recipe_create(user=self.user)
        reci_2=recipe_create(user=another)
        
        res= self.client.get(RECIPE_URL) #self.user client get
      
        recipe_list=Recipes.objects.filter(user=self.user).order_by("-id") #self only list 
        recipe_list_serial=RecipeSerializer(recipe_list,many=True) #Serialzer for match with api data
        self.assertEqual(res.status_code,status.HTTP_200_OK) #STATUS_CODE
        self.assertEqual(res.data,recipe_list_serial.data) #List is equal
    
    def test_retrieve_recipe_detail(self):
        
        createRecipe=recipe_create(user=self.user)
        recipe=Recipes.objects.get(id=createRecipe.id) #confirm create success
        serializer=RecipeDetailSerializer(recipe) #get ref to assert
        
        url=getRECIPE_URL(createRecipe.id)
        res=self.client.get(url)
        
        self.assertEqual(res.data,serializer.data)
        self.assertIn("description",res.data.keys())
    
    def test_create_recipe(self):
        
        payload={
            'title':"burger",
            'time':999,
            'price':Decimal("100.50"),
            'description':"fat! fat! fat!",
            "link": "https://www.burgerking.com.tw/branchweb?branch=0&cate=1630593493&gclid=CjwKCAjwoMSWBhAdEiwAVJ2ndhcrPXaz4h9UDs9nbE9Fw92nhO7qXeixatgjjA7fRgo7wcuc5fnhhRoCeUEQAvD_BwE"
        }
        #serializer=RecipeDetailSerializer(payload)  這句也不會,反正你丟髒的data也會在後端通過RecipeDetailSerializer
        res=self.client.post(RECIPE_URL,payload) #"user":self.user, 不用加入,因為client已經有auth啦笨蛋
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        
        recipe=Recipes.objects.get(id=res.data["id"])

        for k,v in payload.items():
             self.assertEqual(getattr(recipe,k),v)
        self.assertEqual(recipe.user,self.user)
    