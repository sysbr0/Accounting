from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Costomers
from django.utils import timezone





class Package(models.Model):
    id = models.IntegerField(primary_key=True) 
    package_name = models.TextField()
    package_arabic = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_package')
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.package_arabic

class Jar(models.Model):
    jar_name = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_jar')
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.jar_name

class ProductHam(models.Model):
    product_name = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_product_ham')
    image = models.URLField(blank=True, null=True)
    top = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    percentage = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])

    def __str__(self):
        return self.product_name

class MainProduct(models.Model):
    product_name = models.TextField()
    product_type = models.TextField()
    product_ham = models.ForeignKey(ProductHam, related_name="select_ham", on_delete=models.CASCADE)
    jar = models.ForeignKey(Jar, related_name="select_jar", on_delete=models.CASCADE)
    package = models.ForeignKey(Package, related_name="select_package", on_delete=models.CASCADE)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_main_product')
    image = models.URLField(blank=True, null=True)
    net_weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    top_weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
    amount_inside = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(1000)])
    qr = models.IntegerField(primary_key=True)

    def __str__(self):
        return f"{self.package.package_arabic} {self.product_name} {self.product_type} الوزن الصافي {self.net_weight} الشد {self.amount_inside}  الرمز [ {self.qr} ]"
    
    def net(self):
        return self.net_weight * self.amount_inside/100
    def top(self):
        return self.top_weight * self.amount_inside/100
    

 

class UdsBills(models.Model):
    id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_uds_bills')
    customer = models.ForeignKey(Costomers, on_delete=models.CASCADE, related_name='uds_bills_customers')
    note = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)
    price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    net = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)
    top = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(9999999999)], default=0)


    def __str__(self):
         return f"فاتورة للسيد {self.customer.name} "
    
    
    def calculate_total(self):
        total = sum(inner.calculate() for inner in self.select_UdsBill_inner.all())
        self.price = total
        self.save()

     
    def calculate_total_net(self):
        total = sum(inner.net() for inner in self.select_UdsBill_inner.all())
        self.net = total
        self.save()

    def calculate_total_top(self):
        total = sum(inner.top() for inner in self.select_UdsBill_inner.all())
        self.top = total
        self.save()

    

    




    def costomer_name(self):
        return self.customer.name



    def save(self, *args, **kwargs):
         if not self.created_at:
              self.created_at = timezone.now().date()
         super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now().date()
        super().save(*args, **kwargs)


    def costomer_tex(self):
        return self.customer.tex


    

    def costomer_number(self):
        return self.customer.number
    
    def costomer_company(self):
        return self.customer.company
    


    def costomer_address(self):
        return self.customer.address
    
    
    
    
    
    
    














class UdsBill_inner(models.Model):

      created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_UdsBill_inner')
      uds_bill = models.ForeignKey(UdsBills, on_delete=models.CASCADE, related_name="select_UdsBill_inner")
      main_product = models.ForeignKey(MainProduct, related_name="select_MainProduct", on_delete=models.CASCADE)
      amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
      price = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)])
      note = models.TextField(blank=True, null=True)
    
      def __str__(self):
        return f"{self.main_product} "
 

      def calculate(self):
        return self.amount * self.price
      
      def net(self):
          return self.amount * self.main_product.net_weight/1000
      
          
      def top(self):
          return self.amount * self.main_product.top_weight/1000
      


      def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.uds_bill.calculate_total()
        self.uds_bill.calculate_total_net()
        self.uds_bill.calculate_total_top()

      def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.uds_bill.calculate_total()
        self.uds_bill.calculate_total_net()
        self.uds_bill.calculate_total_top()

