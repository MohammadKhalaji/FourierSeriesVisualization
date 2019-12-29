from django.db import models
import numpy as np

from numpy import *

def u(t):
    return np.heaviside(t, 1)
# Create your models here.


class Signal(models.Model):
    periodStart = models.CharField(max_length=100)
    periodEnd = models.CharField(max_length=100)
    equation = models.CharField(max_length=500)

    def get_characteristics(self):
        s = float(self.periodStart)
        e = float(self.periodEnd)
        period = e - s
        t = np.arange(s, e, 0.01)
        eqstr = self.equation.replace('^', '**')
        x = eval(eqstr)
        if not isinstance(x, np.ndarray):
            x = np.full(t.shape, x)

        return t, x, period
