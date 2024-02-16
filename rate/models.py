from django.db import models

class Currency(models.Model):
    date = models.DateField()
    charcode = models.CharField(max_length=3)
    rate = models.DecimalField(max_digits=10, decimal_places=4)

    def __str__(self):
        return f'Курс [{self.charcode}] [{self.date}] - {self.rate}'

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'
