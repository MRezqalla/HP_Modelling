TREF = 65

def consumption_R410a(temp, demand):
    if (temp >= 65):
        COP = -0.05575555555555556 * (temp - TREF) + 5.31175
    elif (temp < 65):
        COP = 0.03555111111111112 * (temp - TREF) + 4.4678666666666675
    EC = demand / COP
    return EC

def consumption_R32(temp, demand):
    if (temp >= 65):
        COP = -0.078 * (temp - TREF) + 6.0305
    elif (temp < 65):
        COP = 0.02245 * (temp - TREF) + 3.323625
    EC = demand / COP
    return EC

def consumption_DF(temp, demand):
    if (temp >= 65):
        COP = -0.034502276 * (temp - TREF) + 4.725396194
    elif (temp < 65):
        COP = 0.03932384 * (temp - TREF) + 4.2763154960000005
        NGC = 0.8 * demand
        ED = 0.2 * demand
        EC = ED / COP
        
        return NGC, EC
        
    EC = demand / COP
    
    return EC

