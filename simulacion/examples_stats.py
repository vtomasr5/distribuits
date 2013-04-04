import numpy.random as rand

#Expontenial
mean = 3.0
print rand.exponential(scale=mean)

#Zipf
a = 2 #Parametro a, a>1.0
print rand.zipf(a)

#Zipf
a = 2 #Parametro a, a>1.0
numMuestras = 1000
print rand.zipf(a, numMuestras) #Devuelve un array con 1000 numeros

#Lognormal
mean = 3.0
print rand.lognormal(mean=mean)