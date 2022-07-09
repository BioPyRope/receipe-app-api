'''
Comfirm Django init app before database alive
Django會自動找management的資料夾並執行commands??
django.core.management.base
'''
from psycopg2 import OperationalError as psycopg2Error
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from time import sleep

class Command(BaseCommand):
    
    def handle(self,*arg, **options):
        ''' Entry point for command '''
        self.stdout.write("waiting for database...")
        db_up=False
        
        while db_up is False:
            
            try: 
               isready=self.check(databases=["default"])
               db_up=True
               print(isready,"isready")
            except(psycopg2Error,OperationalError):
                self.stdout.write("Not ready yet...you need to be patient...")
                sleep(20)
            print(isready,"isready")    
        self.stdout.write(self.style.SUCCESS("! DB IS NOW AVAILABLE"))
                
        