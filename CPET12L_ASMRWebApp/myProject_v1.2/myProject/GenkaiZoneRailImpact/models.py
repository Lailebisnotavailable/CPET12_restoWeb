from django.db import models
from django.utils.timezone import now

class Accounts(models.Model):
    AccountID = models.CharField(default='0000000',unique=True,max_length=30,verbose_name='AccountID')
    FirstName = models.CharField(default='Aaron',max_length=30,verbose_name='FirstName') 
    LastName = models.CharField(default='Ayapana',max_length=30,verbose_name='LastName')
    Password = models.CharField(default='Aaron123',max_length=30,verbose_name='Password')
    Email = models.EmailField(default='default@gmail.com',unique=True,max_length=50,verbose_name='Email')
    Birthday = models.DateField(default=now,auto_now=False,auto_now_add=False,verbose_name='Birthday')
    Contact_No = models.CharField(default='09212121212',max_length=30,verbose_name='Contact_No')
    Credit_Wallet = models.IntegerField(default=1,verbose_name='Credit')   
    Sec_Question = models.TextField(default="What is a programmer's first words?",verbose_name='Question')
    Sec_Answer = models.CharField(default='Hello World!',max_length=30,verbose_name='Answer')
    Sec_Pin = models.CharField(default='0000',max_length=30,verbose_name='PIN')

    def __str__ (self):
        return self.AccountID


