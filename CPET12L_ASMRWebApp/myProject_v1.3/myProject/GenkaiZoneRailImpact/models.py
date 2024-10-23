from django.db import models

class Accounts(models.Model):
    AccountID = models.AutoField(primary_key=True)
    FirstName = models.CharField(null=False,max_length=30,verbose_name='FirstName') 
    LastName = models.CharField(null=False,max_length=30,verbose_name='LastName')
    Password = models.CharField(null=False,max_length=30,verbose_name='Password')
    Email = models.EmailField(null=False,unique=True,max_length=50,verbose_name='Email')
    Birthday = models.DateField(null=True,blank=True)
    ContactNo = models.CharField(null=True,unique=True,max_length=11,verbose_name='ContactNo.')
    Wallet = models.DecimalField(null=True, default=0.00, max_digits=6, decimal_places=2, verbose_name='Wallet')
    Sec_Question = models.CharField(null=True, max_length=200, verbose_name='SecurityQuestion')
    Sec_Answer = models.CharField(null=True,blank=True, max_length=50, verbose_name='Security Answer')
    Sec_Pin = models.CharField(null=True, max_length=4, verbose_name='Security PIN')  # 4

    def __str__ (self):
        return f'{self.FirstName} {self.LastName} (ID: {self.AccountID})'
    
class FoodCatalog(models.Model):
    FoodId = models.AutoField(primary_key=True)
    FoodCategory = models.CharField(max_length=30,verbose_name='Category')
    FoodImage = models.ImageField(upload_to='food_images/')
    FoodName = models.CharField(max_length=200,unique=True)
    FoodPrice = models.DecimalField(max_digits=5, decimal_places=2)
    FoodDescription = models.TextField()
    FoodRating = models.DecimalField(null=True,blank=True,max_digits=2, decimal_places=1) 
    FoodViews = models.IntegerField(null=True,blank=True,default=0)
    DateAdded = models.DateField(auto_now_add=True) 

    def __str__(self):
        return self.food_name  # Returns the food name when the object is printed

class TempTransaction(models.Model):
    TempTransactID = models.AutoField(primary_key=True)
    Food = models.ForeignKey(FoodCatalog,on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)
    TransactionDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.TempTransactID} for {self.Food.FoodName}"