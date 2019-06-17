# Link Budget calculator for cascaded microwave systems
# Adrian Sinclair
import numpy as np
import SchemDraw as schem
import SchemDraw.elements as e
from cable import *
# manual for SchemDraw
# https://cdelker.bitbucket.io/SchemDraw/SchemDraw.html

# initialize
#S = -10 # dBm input signal power
d = schem.Drawing() # initialize schematic
nParams = 5 # number of parameters for each component stored in array p
p = np.zeros(nParams) # initialize component parameter array p

##########################
# Amplifier function
##########################
def addAmp(T,G,S=0.,p=0):
    """
    Params: 
    T : noise temperature of the attenuator [K]
    G: gain value in [dB]
    S: signal power in [dBm]
    p : parameter array for components
    """
    
    NSD = 0
    Tf = 0
    Ti = 0
    P = 0
    Gprod = 0
    
    if np.size(np.shape(p)) == 0:
      Tf = T
      # output signal power
      P = S+G # [dBm]
      NSD =10.0*np.log10( 1.38e-23*T*1000.0) # noise spectral density [dBm/Hz]
      p = np.array([S, T, G, P, NSD])
    
    else:
      #Noise calculation
      p = np.vstack((p,np.array([S,T,G,P,0])))      
      # output signal power
      S,p[-1][0] = p[-2][3], p[-2][3]
      P = p[-1][0]+G # [dBm]
      p[-1][3] = P  # assign output power to new array      
      Gc = 10.0**(p[:,2]/10.0) # component gain array and convert to linear
      p_flat = p.flatten()
      for i in range(len(p_flat)/nParams): # Friis cascade noise loop
          Ti = p[i][1] # grab specific components noise, or thermal temp
          if i == 0:
            Tf += Ti
          else:
            Gprod = np.prod(Gc[:i])
            Tf += Ti / Gprod
      NSD =10.0*np.log10( 1.38e-23*Tf*1000.0) # noise spectral density [dBm/Hz]
      # add NSD for component
      p[-1][-1] = NSD    
    # draw component and label with params S, T, G, P, NSD
    a1 = d.add(e.AMP,d = 'right')
    a1.add_label("Amp",loc='top')
    a1.add_label("S [dBm]: "+str(round(S,4)),loc='bot')
    a1.add_label("T [K]: "+str(round(T,4)),loc='bot',ofst=1.0)
    a1.add_label("G [dB]: "+str(round(G,4)),loc='bot',ofst=2.0)
    a1.add_label("P [dBm]: "+str(round(P,4)),loc='bot',ofst=3.0)
    a1.add_label("Tcas [K]: "+str(round(Tf,4)),loc='bot',ofst=4.0)
    a1.add_label("NSD [dBm/Hz]: "+str(round(NSD,2)),loc='bot',ofst=5.0)
    d.add(e.LINE, d='right', l=4)
    return p

##########################
# Attenuator function
##########################
def addAtten(T,A,S=0.,p=0):
    """
    Params:
    T : physical temperature of the attenuator [K]
    A: attenuation value in [dB]
    S: signal power in [dBm]
    p : parameter array for components
    """
    NSD = 0
    Tf = 0
    Ti = 0
    P = 0
    Gprod = 0
    
    if np.size(np.shape(p)) == 0:
      Tf = T*(10**(abs(A)/10.) - 1.) # effective noise temp of atten
      # output signal power
      P = S-abs(A) # [dBm]
      NSD =10.0*np.log10( 1.38e-23*Tf*1000.0) # noise spectral density [dBm/Hz]
      p = np.array([S, T, -abs(A), P, NSD])
    
    else:
      #Noise calculation with temperature modified for attenuator T_equiv = T_phys*(Atten-1)
      p = np.vstack((p,np.array([S,T*(10.**(abs(A)/10.0)-1.),-abs(A),P,0])))
      # output signal power
      S,p[-1][0] = p[-2][3], p[-2][3]
      P = p[-1][0]-abs(A) # [dBm]
      p[-1][3] = P  # assign output power to new array      
      Gc = 10.0**(p[:,2]/10.0) # component gain array and convert to linear
      #print(Gc)
      p_flat = p.flatten()
      for i in range(len(p_flat)/nParams): # Friis cascade noise loop
          Ti = p[i][1] # grab specific components noise, or thermal temp
          if i == 0:
            Tf += Ti
          else:
            Gprod = np.prod(Gc[:i])
            Tf += Ti / Gprod
      NSD =10.0*np.log10( 1.38e-23*Tf*1000.0) # noise spectral density [dBm/Hz]
      # add NSD for component
      p[-1][4] = NSD
    # draw component and label with params S, T, G, P, NSD
    a1 = d.add(e.RES,d = 'right')
    a1.add_label("Atten",loc='top')
    a1.add_label("S [dBm]: "+str(round(S,4)),loc='bot')
    a1.add_label("T [K]: "+str(round(T,4)),loc='bot',ofst=1.0)
    a1.add_label("A [dB]: "+str(round(-abs(A),4)),loc='bot',ofst=2.0)
    a1.add_label("P [dBm]: "+str(round(P,4)),loc='bot',ofst=3.0)
    a1.add_label("Tcas [K]: "+str(round(Tf,4)),loc='bot',ofst=4.0)
    a1.add_label("NSD [dBm/Hz]: "+str(round(NSD,2)),loc='bot',ofst=5.0)
    d.add(e.LINE, d='right', l=4)
    return p

##########################
# Cable function
##########################
def addCable(T,L,fin,ctype="SC-086/50-SS-SS",S=0.0,p=0):
    """
    Params:
    T : physical temperature of the attenuator in [K]
    L : length of cable segment in [mm]
    fin : center frequency of input signal in [MHz]
    ctype: cable type as a string, "SS/SS","Cu/Cu", ...
    S: signal power in [dBm]
    p : parameter array for components
    """
    NSD = 0
    Tf = 0
    Ti = 0
    P = 0
    Gprod = 0
    
    #Call cable temperature and frequency attenuation function from cable.py
    A = getLoss(fin,T,L,ctype)
    
    if np.size(np.shape(p)) == 0:
      Tf = T*(10**(abs(A)/10.) - 1.)
      # output signal power
      P = S-abs(A) # [dBm]
      NSD =10.0*np.log10( 1.38e-23*Tf*1000.0) # noise spectral density [dBm/Hz]
      p = np.array([S, T, -abs(A), P, NSD])
    
    else:
      #Noise calculation with temperature modified for attenuator T_equiv = T_phys*(Atten-1)
      p = np.vstack((p,np.array([S,T*(10.**(abs(A)/10.0)-1.),-abs(A),P,0])))
      # output signal power
      S,p[-1][0] = p[-2][3], p[-2][3]
      P = p[-1][0]-abs(A) # [dBm]
      p[-1][3] = P  # assign output power to new array      
      Gc = 10.0**(p[:,2]/10.0) # component gain array and convert to linear
      #print(Gc)
      p_flat = p.flatten()
      for i in range(len(p_flat)/5): # Friis cascade noise loop
          Ti = p[i][1] # grab specific components noise, or thermal temp
          if i == 0:
            Tf += Ti
          else:
            Gprod = np.prod(Gc[:i])
            Tf += Ti / Gprod
      NSD =10.0*np.log10( 1.38e-23*Tf*1000.0) # noise spectral density [dBm/Hz]
      # add NSD for component
      p[-1][4] = NSD
    # draw component and label with params S, T, G, P, Tcas, NSD
    a1 = d.add(e.CABLE,d = 'right')
    a1.add_label(ctype+" Cable",loc='top')
    a1.add_label("S [dBm]: "+str(round(S,4)),loc='bot')
    a1.add_label("T [K]: "+str(round(T,4)),loc='bot',ofst=1.0)
    a1.add_label("A [dB]: "+str(round(-abs(A),4)),loc='bot',ofst=2.0)
    a1.add_label("P [dBm]: "+str(round(P,4)),loc='bot',ofst=3.0)
    a1.add_label("Tcas [K]: "+str(round(Tf,4)),loc='bot',ofst=4.0)
    a1.add_label("NSD [dBm/Hz]: "+str(round(NSD,2)),loc='bot',ofst=5.0)
    a1.add_label("Length [mm]: "+str(round(L,2)),loc='bot',ofst=6.0)
    d.add(e.LINE, d='right', l=4)
    return p

def addLEKID(arrayName):
    """
    Params:
    arrayName: String of LEKID array
    """
    # draw component and label
    a1 = d.add(e.LEKID,d = 'right')
    a1.add_label(arrayName,loc='top')
    d.add(e.LINE, d='right', l=4)
    return



