TREF_F = 65 #The temperature where heat pumps switch from heating/cooling to cooling/heating
TREF_C = 18.333 #In Celsius
 
#First three functions take the temperature (if not specified otherwise )in fahrenhiet and the demand in whatever units (consumption is retuned in a scaled unit of that)

def consumption_R410a(temp, demand, unit='f'):

    if (unit == 'c'):
        if (temp >= 18):
            COP = -0.10036 * (temp - TREF_C) + 5.3120812
   
        elif (temp < 18):
            COP = 0.063992 * (temp - TREF_C) + 4.46765336
        EC = demand / COP
        return EC
    
    #Cooling
    if (temp >= 65):
        COP = -0.05575555555555556 * (temp - TREF_F) + 5.31175
    #Heating
    elif (temp < 65):
        COP = 0.03555111111111112 * (temp - TREF_F) + 4.4678666666666675
        
    #Energy demand scaled using COP to give consumption
    EC = demand / COP
    return EC

def consumption_R32(temp, demand, unit='f'):

    if (unit == 'c'):
        if (temp >= 18):
            COP = -0.1404 * (temp) + 8.6045
   
        elif (temp < 18):
            COP = 0.04041 * (temp) + 2.582775
        EC = demand / COP
        return EC
        
    if (temp >= 65):
        COP = -0.078 * (temp - TREF_F) + 6.0305
    elif (temp < 65):
        COP = 0.02245 * (temp - TREF_F) + 3.323625
    EC = demand / COP
    return EC

def consumption_DF(temp, demand, unit='f'):

    if (unit == 'c'):
        if (temp >= 18):
            COP = -0.0621040968 * (temp) + 5.863971302
   
        elif (temp < 18):
            COP = 0.070782912 * (temp) + 2.9786287760000005
        EC = demand / COP
        return EC
        
    if (temp >= 65):
        COP = -0.034502276 * (temp - TREF_F) + 4.725396194
    elif (temp < 65):
    #In heating mode, furnace assumed to deal with 80% of demand (AFUE value)
    #NGC = Natural Gas Consumption
        COP = 0.03932384 * (temp - TREF_F) + 4.2763154960000005
        NGC = 0.81 * demand
        ED = 0.19 * demand
        EC = ED / COP
        
        return NGC, EC
        
    EC = demand / COP
    
    return EC



#Returns (cooling, heating) coeffs (slope, intercept at 65F) for each tech
#1 - R410a
#2 - R32
#3 - Dual Fuel

def get_coeffs_f(choice):
    if choice == 1:
        return [-0.05575555555555556,5.31175], [0.03555111111111112,4.4678666666666675]
    elif choice == 2:
        return [-0.078,6.0305], [0.02245,3.323625]
    elif choice == 3:
        return [-0.034502276,4.725396194], [0.03932384,4.2763154960000005]

def get_coeffs_c(choice):
    if choice == 1:
        return [-0.10036,7.15168], [0.063992,3.29468]
    elif choice == 2:
        return [-0.1404,8.6045], [0.04041,2.582775]
    elif choice == 3:
        return [-0.0621040968,5.863971302], [0.070782912,2.9786287760000005]
