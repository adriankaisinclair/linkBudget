# blast 500um path cascaded microwave link budget
from linkBudgetCalc import *
# Create cascade of components, addAmp, addAtten, addCable, addLEKID
# first component does not pass parameter array p
# addCable ctype choices "SC-086/50-SS-SS" "SC-219/50-SS-SS" "SC-086/50-NbTi-NbTi" "S086MMHF"
##########################################
# RF input path
###########################################
p = addCable(220,241.3,500.0,ctype="SC-086/50-SS-SS") # 300K to VCS2 
p = addCable(90,101.6,500.0,ctype="SC-086/50-SS-SS",p=p) # VCS2 to VCS1
p = addCable(22,749.3,500.0,ctype="SC-219/50-SS-SS",p=p) # VCS1 to 4K
p = addCable(2.5,863.6,500.0,ctype="SC-086/50-SS-SS",p=p) # 4K to 1K
p = addAtten(1,20.0,p=p) # attenuator on 1K plate
p = addCable(0.625,190.5,500.0,ctype="SC-086/50-SS-SS",p=p) # 1K to 300mK
p = addAtten(0.300,20.0,p=p) # attenuator on input to FPA
# ARRAY 
addLEKID("500um Array") # LEKID function does not take or return parameter array p
###########################################
# RF output path
###########################################
p = addCable(2.,700.,500.0,ctype="SC-086/50-NbTi-NbTi",p=p)
p = addAmp(6,20,S=-77.942,p=p)
p = addAtten(4,3,p=p)
p = addAmp(6,20,p=p)
p = addCable(4,520.,500.0,ctype="SC-086/50-SS-SS",p=p) #LNA to 4K
p = addCable(10,749.3,500.0,ctype="SC-219/50-SS-SS",p=p) #4K to VCS1
p = addCable(40,101.6,500.0,ctype="SC-086/50-SS-SS",p=p) #VCS1 to VCS2
p = addCable(140,241.3,500.0,ctype="SC-086/50-SS-SS",p=p) #VCS2 to 300K

# DRAW DIAGRAM AND PLOT
d.draw()
d.save("blast500um.pdf")
