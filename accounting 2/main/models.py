from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings



# the table of  the clints 
class clints(models.Model):
    #blog = models.ForeignKey(Blog, related_name='inner_contents', on_delete=models.CASCADE)
    clint_name = models.TextField()
    clint_tex= models.IntegerField(blank=True, null=True)
    clint_email = models.EmailField(blank=True, null=True)
    c_number = models.CharField(max_length=255)
    c_sorce = models.CharField(max_length=255)
    clint_iban = models.TextField(blank=True, null=True)
    is_company = models.BooleanField()
    clint_tr_name= models.CharField(max_length=255)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_clints')

    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.clint_name


class buyes(models.Model):
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    clint_id = models.ForeignKey(clints , related_name="chose_clint" , on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} from  {self.clint_id.clint_name} "

class accounts(models.Model):
    account_name = models.CharField(max_length=255)
    balance = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)])


    def __str__(self):
      return self.account_name



# this class  inherts from the   mony account and in the same time from the clints account
class payment(models.Model):
    transaction_date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)])
    account = models.ForeignKey(accounts, related_name="payments", on_delete=models.CASCADE)
    client = models.ForeignKey(clints, related_name="payments", on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return f"{self.amount} from account {self.account.account_name} to client {self.client.clint_name}"

# the branc is loke the storge  so with it we ca deside where is the sorce gose 
class branches(models.Model):
    branch_name = models.CharField(max_length=255)
    branch_address = models.TextField()
    branch_code = models.CharField(max_length=255)
    def __str__(self):
        return self.branch_name



class mainPoduct(models.Model):
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()

    def __str__(self):
        return self.product_name


class buyesInner(models.Model):
    product_id = models.ForeignKey(mainPoduct , related_name="product" , on_delete=models.CASCADE)
    buysid = models.ForeignKey(buyes , related_name="product" , on_delete=models.CASCADE)
    type = models.ForeignKey(branches , related_name="product" , on_delete=models.CASCADE)
    e_bill = models.BooleanField(False)
    quantity = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    price = models.DecimalField(max_digits=10, decimal_places=2)
    extra = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    def __str__(self) :
       return f" from {self.buysid.clint_id.clint_name}  item  {self.product_id.product_name} amount  {self.quantity} kg"
    
    def calculate(self):
        return self.price * self.quantity + self.extra


    





    

                                   
    

    

    
