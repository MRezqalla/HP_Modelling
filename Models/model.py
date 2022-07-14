TREF = 65 #The temperature where heat pumps switch from heating/cooling to cooling/heating

#First three functions take the temperature in fahrenhiet and the demand in whatever units (consumption is retuned in a scaled unit of that)

def consumption_R410a(temp, demand):
    #Cooling
    if (temp >= 65):
        COP = -0.05575555555555556 * (temp - TREF) + 5.31175
    #Heating
    elif (temp < 65):
        COP = 0.03555111111111112 * (temp - TREF) + 4.4678666666666675
        
    #Energy demand scaled using COP to give consumption
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
    #In heating mode, furnace assumed to deal with 80% of demand (AFUE value)
    #NGC = Natural Gas Consumption
        COP = 0.03932384 * (temp - TREF) + 4.2763154960000005
        NGC = 0.8 * demand
        ED = 0.2 * demand
        EC = ED / COP
        
        return NGC, EC
        
    EC = demand / COP
    
    return EC



#Returns (cooling, heating) coeffs (slope, intercept at 65F) for each tech
#1 - R410a
#2 - R32
#3 - Dual Fuel

def get_coeffs(choice):
    if choice == 1:
        return [-0.05575555555555556,5.31175], [0.03555111111111112,4.4678666666666675]
    elif choice == 2:
        return [-0.078,6.0305], [0.02245,3.323625]
    elif choice == 3:
        return [-0.034502276,4.725396194], [0.03932384,4.2763154960000005]
