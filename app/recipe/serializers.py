from rest_framework.serializers import ModelSerializer
from core.models import Recipes

class RecipeSerializer(ModelSerializer):
    
    class Meta:
        model = Recipes
        fields = ["id","title","time","price","link",]
        read_only_fields=["id"]
        
class RecipeDetailSerializer(ModelSerializer):
    
    class Meta:
        model = Recipes
        fields = ["id","title","time","price","link","description"]
        read_only_fields=["id"]
        