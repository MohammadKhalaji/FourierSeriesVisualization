from django.shortcuts import render, redirect
from . import forms
import matplotlib.pyplot as plt
from random import randint
from . import models
import numpy as np
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg
# Create your views here.


def signalSubmit(request):
    if request.method == 'GET':
        form = forms.SignalForm(initial={'periodStart': '-5', 'periodEnd': '5', 'equation': 'u(t+2)-u(t-2)'})
        default = True
    else:
        if 'preview' in request.POST:
            form = forms.SignalForm(request.POST)
            if form.is_valid():
                signal, created = models.Signal.objects.get_or_create(**form.cleaned_data)
                signal.save()
                t, x, period = signal.get_characteristics()
                plt.title('x(t)', y=1.03)
                plt.plot(t, x)
                plt.savefig('fs/static/fs/img/plot.png'.format(signal.id), dpi=700)
                plt.clf()
                default = False

        elif 'finalize' in request.POST:
            form = forms.SignalForm(request.POST)
            if form.is_valid():
                signal, created = models.Signal.objects.get_or_create(**form.cleaned_data)
                signal.save()

                return redirect('fourier', signal.id)

    return render(request, 'fs/signalSubmit.html', {'form': form, 'default': default})

@csrf_exempt
def fourier(request, pk):
    signal = models.Signal.objects.get(pk=pk)
    t, x, period = signal.get_characteristics()

    if request.method == 'GET':
        file = open('coeffs.txt', 'w')
        file.write(str(5))
        coeffs = 5
        file.close()
        fs = fourier_series(t, x, period, coeffs)
        plt.plot(list(t-period)+list(t)+list(t+period), list(x)+list(x)+list(x), 'b', label='original signal')
        plt.plot(list(t-period)+list(t)+list(t+period), list(fs)+list(fs)+list(fs), 'r', label='FS approximation')
        plt.legend()
        plt.title('$\sum_{k=-' + str(coeffs) + '}^{' + str(coeffs) + '} a_k e^{' + 'jk\omega_0 t}$', y=1.03)
        plt.savefig('fs/static/fs/img/plot2.png', dpi=700)
        plt.clf()

        return render(request, 'fs/fourier.html', {'pk': pk, 'coeffs': coeffs})

    else:
        filename = request.POST['src'].split('/')[-1]
        file = open('coeffs.txt', 'r')
        coeffs = int(file.read())
        file.close()
        file = open('coeffs.txt', 'w')
        if 'increase' in request.POST['req']:
            coeffs = coeffs + 1
            file.write(str(coeffs))
            file.close()
            filename = 'plot2.png'
            fs = fourier_series(t, x, period, coeffs)
            plt.plot(list(t-period)+list(t)+list(t+period), list(x) + list(x) + list(x), 'b', label='original signal')
            plt.plot(list(t-period)+list(t)+list(t+period), list(fs) + list(fs) + list(fs), 'r', label='FS approximation')
            plt.legend()
            plt.title('$\sum_{k=-' + str(coeffs) + '}^{' + str(coeffs) + '} a_k e^{' + 'jk\omega_0 t}$', y=1.03)
            plt.savefig('fs/static/fs/img/' + filename, dpi=700)
            plt.clf()
            response = HttpResponse(json.dumps({'newsrc': '/static/fs/img/'+filename+'?dummy='+str(randint(1000, 1000000))}), content_type="application/json")
            return response

        elif 'decrease' in request.POST['req']:
            if coeffs >= 2:
                coeffs = coeffs - 1
            file.write(str(coeffs))
            file.close()
            filename = 'plot2.png'
            fs = fourier_series(t, x, period, coeffs)
            # my_time = np.arange(min(t) - period, max(t) + period, 0.01)
            plt.plot(list(t-period)+list(t)+list(t+period), list(x) + list(x) + list(x), 'b', label='original signal')
            plt.plot(list(t-period)+list(t)+list(t+period), list(fs) + list(fs) + list(fs), 'r', label='FS approximation')
            plt.legend()
            plt.title('$\sum_{k=-' + str(coeffs) + '}^{' + str(coeffs) + '} a_k e^{' + 'jk\omega_0 t}$', y=1.03)
            plt.savefig('fs/static/fs/img/'+filename, dpi=700)
            plt.clf()
            response = HttpResponse(json.dumps({'newsrc': '/static/fs/img/'+filename+'?dummy='+str(randint(1000, 1000000))}), content_type="application/json")
            return response

    return render(request, 'fs/fourier.html', {'pk': pk, 'coeffs': coeffs})



def fourier_series(t, x, period, coeffs):
    ans = np.zeros(x.shape)
    for k in range(-coeffs, coeffs+1):
        argument = x * np.exp(-1j*k*2*np.pi*t/period)
        ak = np.trapz(argument, x=t)
        ak = ak / period
        ans += (ak * np.exp(1j*k*2*np.pi*t/period)).real
    return ans

