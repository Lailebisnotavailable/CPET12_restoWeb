from django.db import models
from django.utils import timezone
from django.utils.timezone import now


###COMONMSONSOD
class FoodCatalog(models.Model):
    FoodId = models.AutoField(primary_key=True)
    FoodCategory = models.CharField(max_length=30, verbose_name='Category', null=True, blank=True)
    FoodImage = models.ImageField(upload_to='food_images/', null=True, blank=True)
    FoodName = models.CharField(max_length=200, unique=True, null=True, blank=True)
    FoodPrice = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    FoodDescription = models.TextField(null=True, blank=True)
    FoodViews = models.IntegerField(null=True, blank=True, default=0)
    DateAdded = models.DateField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.FoodName  # Fixed the attribute name to match the field

class Accounts(models.Model):
    AccountID = models.AutoField(primary_key=True)
    AccountType = models.CharField(null=True, max_length = 30, verbose_name='Account Type' )
    FirstName = models.CharField(null=False, max_length = 30, verbose_name='First Name') 
    LastName = models.CharField(null=False, max_length = 30, verbose_name='Last Name')
    Password = models.CharField(null=False,max_length = 255, verbose_name='Password', default='P@ssw0rd')  # Keep this as TextField to store the password
    Email = models.EmailField(null=False, unique=True, max_length = 50, verbose_name='Email')
    Birthday = models.DateField(null=True, blank=True)
    ContactNo = models.CharField(null=True, unique=True, max_length=11, verbose_name='Contact No.')
    Wallet = models.DecimalField(null=True, default=0.00, max_digits=10, decimal_places=2, verbose_name='Wallet')
    BlockLot = models.CharField(null=True, max_length=100, verbose_name='Block & Lot')
    Street = models.CharField(null=True, max_length=100, verbose_name='Street')
    Subdivision = models.CharField(null=True, max_length=100, verbose_name='Subdivision')
    Barangay = models.CharField(null=True, max_length=100, verbose_name='Barangay')
    City = models.CharField(null=True, max_length=100, verbose_name='City')
    Province = models.CharField(null=True, max_length=100, verbose_name='Province')
    otp = models.IntegerField(null=True, blank=True) #added for otp
    otp_created_at = models.DateTimeField(null=True, blank=True) #this too added

    def save(self, *args, **kwargs):
        print(f"Password length: {len(self.Password)}")
        super().save(*args, **kwargs)
    def __str__ (self):
        return f'{self.FirstName} {self.LastName} (ID: {self.AccountID})'
    
class CashierApplication(models.Model):
    ApplicantID = models.AutoField(primary_key=True)
    AccountType = models.CharField(null=True, max_length = 30, verbose_name='Account Type' )
    FirstName = models.CharField(null=False, max_length = 30, verbose_name='First Name') 
    LastName = models.CharField(null=False, max_length = 30, verbose_name='Last Name')
    Password = models.CharField(null=False,max_length = 255, verbose_name='Password', default='P@ssw0rd')  # Keep this as TextField to store the password
    Email = models.EmailField(null=False, unique=True, max_length = 50, verbose_name='Email')
    Birthday = models.DateField(null=True, blank=True)
    ContactNo = models.CharField(null=True, unique=True, max_length=11, verbose_name='Contact No.')
    Sec_Question = models.CharField(null=True, max_length=200, verbose_name='Security Question')
    Sec_Answer = models.CharField(null=True, blank=True, max_length=50, verbose_name='Security Answer')
    Sec_Pin = models.CharField(null=True, max_length=4, verbose_name='Security PIN')
    last_login = models.DateTimeField(null=True, blank=True)
    
class Cart(models.Model):
    CartID = models.AutoField(primary_key=True)
    AccountID = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True, blank=True)  # Temporarily nullable
    FoodID = models.ForeignKey(FoodCatalog, on_delete=models.CASCADE, null=True, blank=True)
    Quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"Cart {self.CartID} for Account {self.AccountID} with Food {self.FoodID}"

    class Meta:
        unique_together = ('AccountID', 'FoodID')  # Ensures one Cart item per Food for each Account

    
class Checkout(models.Model):
    CheckoutID = models.AutoField(primary_key=True)
    AccountID = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True, blank=True)  # Temporarily nullable
    FoodID = models.ForeignKey(FoodCatalog, on_delete=models.CASCADE, null=True, blank=True)
    OrderID = models.IntegerField(default=0) #This separates orders from one another
    Quantity = models.IntegerField(default=1)
    Status = models.CharField(null=True, max_length=100, verbose_name='Status', default='Standby')
    #POSSIBLE STATUS STATES: Standby, Received, NotReceived, Refunded, Rejected
    #Standby = Default Value
    #Received = When user pressed received in 'to receive' page. Will be transferred in history of purchase
    #NotReceived = When user pressed not received in 'to receive' page. this will be in cashier's table
    #Refunded = When cashier pressed refunded in table. returns total amount of payment to the user



    def __str__(self):
        return f"Cart {self.CheckoutID} for Account {self.AccountID} with Food {self.FoodID}"


class Void(models.Model):
    VoidID = models.AutoField(primary_key=True)
    Checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)  
    Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Void {self.VoidID} for Checkout {self.Checkout.CheckoutID}"

class TopUp(models.Model):
    TopUpID = models.AutoField(primary_key=True, null=False)
    AccountID = models.ForeignKey(Accounts, on_delete=models.CASCADE, null=True, blank=True)  # Temporarily nullable
    Status = models.CharField(max_length=10, default='pending')
    TopUpAmount = models.IntegerField(default=1)
    TransactionDate = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Topup {self.TopUpID} for Account {self.AccountID} with amount of {self.TopUpAmount}"