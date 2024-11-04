from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class FoodCatalog(models.Model):
    FoodId = models.AutoField(primary_key=True)
    FoodCategory = models.CharField(max_length=30, verbose_name='Category')
    FoodImage = models.ImageField(upload_to='food_images/')
    FoodName = models.CharField(max_length=200, unique=True)
    FoodPrice = models.DecimalField(max_digits=5, decimal_places=2)
    FoodDescription = models.TextField()
    FoodRating = models.DecimalField(null=True, blank=True, max_digits=2, decimal_places=1)
    FoodViews = models.IntegerField(null=True, blank=True, default=0)
    DateAdded = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.FoodName  # Fixed the attribute name to match the field

class TempTransaction(models.Model):
    TempTransactID = models.AutoField(primary_key=True)
    TransactionDate = models.DateTimeField(auto_now_add=True)
    FoodItems = models.ManyToManyField(FoodCatalog, through='TempTransactionItem')

    def __str__(self):
        return f"Transaction {self.TempTransactID}"

class TempTransactionItem(models.Model):
    TempTransaction = models.ForeignKey(TempTransaction, on_delete=models.CASCADE)  # Now TempTransaction is defined
    Food = models.ForeignKey(FoodCatalog, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)

class Accounts(models.Model):
    AccountID = models.AutoField(primary_key=True)
    FirstName = models.CharField(null=False, max_length=30, verbose_name='First Name') 
    LastName = models.CharField(null=False, max_length=30, verbose_name='Last Name')
    Password = models.CharField(null=False, max_length=30, verbose_name='Password')
    Email = models.EmailField(null=False, unique=True, max_length=50, verbose_name='Email')
    Birthday = models.DateField(null=True, blank=True)
    ContactNo = models.CharField(null=True, unique=True, max_length=11, verbose_name='Contact No.')
    Wallet = models.DecimalField(null=True, default=0.00, max_digits=6, decimal_places=2, verbose_name='Wallet')
    Sec_Question = models.CharField(null=True, max_length=200, verbose_name='Security Question')
    Sec_Answer = models.CharField(null=True, blank=True, max_length=50, verbose_name='Security Answer')
    Sec_Pin = models.CharField(null=True, max_length=4, verbose_name='Security PIN')  # 4-digit PIN
    last_login = models.DateTimeField(null=True, blank=True)
    
    # New fields added for profile image and address components
    ProfileImage = models.ImageField(upload_to='profile_images/', null=True, blank=True, verbose_name='Profile Image')
    BlockLot = models.CharField(null=True, max_length=100, verbose_name='Block & Lot')
    Street = models.CharField(null=True, max_length=100, verbose_name='Street')
    Subdivision = models.CharField(null=True, max_length=100, verbose_name='Subdivision')
    Barangay = models.CharField(null=True, max_length=100, verbose_name='Barangay')
    City = models.CharField(null=True, max_length=100, verbose_name='City')
    Province = models.CharField(null=True, max_length=100, verbose_name='Province')

    def update_last_login(self):
        self.last_login = timezone.now()
        self.save()

    def __str__ (self):
        return f'{self.FirstName} {self.LastName} (ID: {self.AccountID})'
    
class Cart(models.Model):
    CartID = models.AutoField(primary_key=True)
    TransactionID = models.ForeignKey(TempTransaction,on_delete=models.CASCADE)
    
class Checkout(models.Model):
    CheckoutID = models.AutoField(primary_key=True)
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)  
    DateAdded = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"Checkout {self.CheckoutID} for Cart {self.Cart.CartID}"

class HistoryOfPurchase(models.Model):
    Checkout = models.OneToOneField(Checkout, on_delete=models.CASCADE, primary_key=True)  
    DateCompleted = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return f"Purchase History for Checkout {self.Checkout.CheckoutID}"

class Void(models.Model):
    VoidID = models.AutoField(primary_key=True)
    Checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)  
    DateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Void {self.VoidID} for Checkout {self.Checkout.CheckoutID}"
