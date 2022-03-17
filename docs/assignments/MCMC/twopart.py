import math, random, sys


v = 0.005


def logLikelihood(v):
    logsame = 2.0*math.log(0.25) + math.log(1.0 + 3.0*math.exp(-4.0*v/3.0))
    logdiff = 2.0*math.log(0.25) + math.log(1.0 - math.exp(-4.0*v/3.0))
    return (2.0*logdiff + 30.0*logsame)

def logPrior(v):
    exponential_rate = 100.0
    return (math.log(exponential_rate) - v*exponential_rate)

def logPosteriorKernel(v):
    return (logLikelihood(v) + logPrior(v))




print('v = %12.5f' %v)
print('log(likelihood) = %12.5f' % logLikelihood(v))
print('log(prior) = %12.5f' % logPrior(v))
print('log(posterior kernel) = %12.5f' % logPosteriorKernel(v))



#---------generate random numbers-------------

import random
u1 = random.random()
print('u1 = %12.5f' %u1)

u2 = random.random()
logu2 = math.log(u2)
print('u2 = %12.5f' %u2)


print('log(u2) = %12.5f' %logu2)
