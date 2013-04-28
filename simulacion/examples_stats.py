import numpy.random as rand
import numpy as np
#Expontenial
mean = 3.0
print rand.exponential(scale=mean)

#Zipf
a = 2 #Parametro a, a>1.0
print rand.zipf(a)

#Zipf
#a = 2 #Parametro a, a>1.0
#numMuestras = 1000
#print rand.zipf(a, numMuestras) #Devuelve un array con 1000 numeros

#Lognormal
mu = -0.10
sigma = 2.43

s = rand.lognormal(mu, sigma, 10)
print s
print np.mean(s)




print rand.random_sample()
