# Microwave coaxial cable loss calculator
# Adrian Sinclair
# References:
#   coax co,ltd SC-086/50-SS-SS
#   http://www.coax.co.jp/en/product/sc/086-50-ss-ss.html
#   http://www.gb.nrao.edu/electronics/edir/edir223.pdf
#   http://www.coax.co.jp/en/product/sc/219-50-ss-ss.html
#   http://www.coax.co.jp/en/product/sc/086-50-nbti-nbti.html
#   https://rfcoax.com/technical-drawing/S086MMHF-20.5.html

import numpy as np
import matplotlib.pyplot as plt

plotting = False
# input parameters for testing
#ctype = "SC-219/50-SS-SS"
#f_0 = 0.500 # GHz
#length = 1000.0 # mm
#Temp = 4. # K

# Cable Parameters
# f - frequency data points in GHz
# LT1, LT2 - loss in dB/m at two different temperatures
# T1, T2 - Temperatures at which loss was measured
def cableParams(ctype):
  global f
  global LT1
  global LT2
  global T1
  global T2
  if ctype == "SC-086/50-SS-SS":
    # SC-086/50-SS-SS
    # http://www.coax.co.jp/en/product/sc/086-50-ss-ss.html  
    f = np.array([0.5,1,5,10,20]) # GHz
    LT1 = np.array([7.3,10.3,23.,32.7,46.4]) # dB/m
    LT2 = np.array([4.7,6.6,14.8,20.9,29.5]) # dB/m
    T1 = 300 # K
    T2 = 4 # K
  elif ctype == "SC-219/50-SS-SS":
    # SC-219/50-SS-SS
    # http://www.coax.co.jp/en/product/sc/219-50-ss-ss.html
    f = np.array([0.5,1,5,10,20]) # GHz
    LT1 = np.array([3.0,4.2,9.4,13.5,19.2]) # dB/m
    LT2 = np.array([1.9,2.6,5.9,8.3,11.7]) # dB/m
    T1 = 300. # K
    T2 = 4. # K
  elif ctype == "SC-086/50-NbTi-NbTi":  
    # SC-086/50-NbTi-NbTi
    # http://www.coax.co.jp/en/product/sc/086-50-nbti-nbti.html
    f = np.array([0.5,1,5,10,20]) # GHz
    LT1 = np.array([6.8,9.6,21.6,30.5,43.1]) # dB/m
    LT2 = np.array([6.7,9.5,21.5,30.4,43.0]) # dB/m
    T1 = 300. # K
    T2 = 299. # K
  elif ctype == "S086MMHF":  
    # S086MMHF
    # https://rfcoax.com/technical-drawing/S086MMHF-20.5.html
    f = np.array([18.,27.,40.,65.]) # GHz
    LT1 = np.array([3.6,4.6,6.6,7.9]) # dB/m
    LT2 = np.array([3.59,4.59,6.59,7.89]) # dB/m
    T1 = 300. # K
    T2 = 299. # K
  return f, LT1, LT2, T1, T2

def lsFit(f,L):
  logf = np.log(f)
  logL = np.log(L)
  m,b = np.polyfit(logf,logL,1)
  Afit = np.exp(b)
  return Afit

def LT1fit(fin):
  return Afit_T1*np.sqrt(fin)

def LT2fit(fin):
  return Afit_T2*np.sqrt(fin)

def LperMeter(T,f): # frequency in GHz, Temperature in K
  M = ((LT1fit(f)-LT2fit(f)) / (T1-T2))
  b = LT1fit(f) - LT1fit(f)*T1/(T1-T2) + LT2fit(f)*T1/(T1-T2) 
  Lm = M*T + b # loss in [dB/m]
  return Lm

def L(Lm,length):
  L = length*Lm/1.0e3 # loss in [dB]
  return L
 
def getLoss(f_0,Temp,length,ctype):
  global Afit_T1
  global Afit_T2
  f_0 = f_0/1.e3 # convert from MHz to GHz
  if (ctype == "SC-086/50-NbTi-NbTi") and (Temp < 10.0):
    LtoReturn = 0.5*length/1.e3 # superconducting state loss max of 0.5 dB/m
  else:
    f , LT1, LT2, T1, T2 = cableParams(ctype)
    Afit_T1 = lsFit(f,LT1)
    Afit_T2 = lsFit(f,LT2)
    Lm = LperMeter(Temp,f_0)
    LtoReturn = L(Lm,length)
  #print "Loss at freq "+str(f_0)+"GHz at temp "+str(Temp)+"K with cable "+ctype+" :"+str(LtoReturn)+"[dB]"
  return LtoReturn # Loss in [dB]


if plotting == True:
  # for plotting above fitting equations
  f_fit = np.linspace(0,20,2001)
  L_T1_fit = Afit_T1*np.sqrt(f_fit)
  L_T2_fit = Afit_T2*np.sqrt(f_fit)
  Lfit = np.zeros(len(f_fit))
  for i in range(len(f_fit)):
    Lfit[i] = LperMeter(Temp,f_fit[i])
  plt.ion()
  plt.scatter(f,LT1,label="meas 300K",c='red')
  plt.scatter(f,LT2,label="meas 4K",c='orange')
  plt.plot(f_fit,L_T1_fit,label="fit 300K")
  plt.plot(f_fit,Lfit,label="Lfit "+str(Temp)+"K",c='black')
  plt.plot(f_fit,L_T2_fit,label="fit 4K")
  plt.ylabel("Loss [dB/m]",size=14)
  plt.xlabel("Frequency [GHz]",size=14)
  plt.title("Frequency dependent loss of "+ctype)
  plt.legend()
  plt.tight_layout()
  plt.show()
