from django.db import models
from accounts.models import User

class TokenPackage(models.Model):
    name = models.CharField(max_length=50)
    tokens = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.tokens} tokens"

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    tokens = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wallet: {self.user.username}"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('purchase', 'Token Purchase'),
        ('subscription', 'Subscription'),
        ('call', 'Video Call'),
        ('gift', 'Gift'),
        ('withdrawal', 'Withdrawal'),
        ('refund', 'Refund'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tokens = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, default='completed')
    payment_method = models.CharField(max_length=50, blank=True)
    reference_id = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type} by {self.user.username}"

class ModelEarning(models.Model):
    model = models.ForeignKey(User, on_delete=models.CASCADE, related_name='earnings')
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True, related_name='model_earnings')
    tokens = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Earning for {self.model.username}: {self.tokens} tokens"