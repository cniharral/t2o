from django.db import models

# Create your models here.

class BidsAsks (models.Model):
    crypto = models.CharField('crypto', null=False, max_length=3)
    realmoney = models.CharField('realmoney', null=False, max_length=3)
    order = models.CharField('order', null=False, max_length=4)
    px = models.FloatField('px', null=False)
    qty = models.FloatField('qty', null=False, max_length=80)
    num = models.IntegerField('num', null=False, unique=True)

    def __unicode__(self):
        return u"%s-%s: %s -> {'px': %f, 'qty': %f, 'num': %d, 'value': %f}" % (self.crypto, self.realmoney, self.order, self.px, self.qty, self.num, self.px*self.qty)

