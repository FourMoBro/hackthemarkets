from django.db import models

# Create your models here.
class Stock(models.Model):    
    symbol = models.CharField(max_length=7, unique=True, blank=False)
    name = models.CharField(max_length=200, blank=False)
    exchange = models.CharField(max_length=10, blank=False)
    shortable = models.BooleanField(blank=False)

    class Meta:
        ordering = ["-name"]


class StockPrice(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    date = models.DateField(blank=False)
    open = models.FloatField(blank=False)
    high = models.FloatField(blank=False)
    low = models.FloatField(blank=False)
    close = models.FloatField(blank=False)
    volume = models.IntegerField(blank=False)
    sma_20 = models.FloatField(null=True, blank=True)
    sma_50 = models.FloatField(null=True, blank=True)
    rsi_14 = models.FloatField(null=True, blank=True)

class Strategy(models.Model):
    name = models.CharField(max_length=40, null=False)

class StockStrategy(models.Model):
    stock_id = models.ForeignKey(Stock, on_delete=models.CASCADE)
    strategy_id = models.ForeignKey(Strategy, on_delete=models.CASCADE)
