import sys
T_ref = 65


try:
    import tabula as tb
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
except:
    sys.exit("Missing Packages")

##Funcrion returns energy consumption
##Parameters:
##temp - Outdoor temperature
##demand - Energy demand
##cooling - cooling coefficients (slope, intercept)
##heating - heating coefficients (slope, intercept)
##x - 2 only for Dual Fuel
def energy_consumption(temp, demand, cooling, heating, x=1):
    
    #Calculates COP based on the given parameters
    if (temp >= T_ref):
        COP = (temp-T_ref) * cooling[0] + cooling[1]
    else:
        COP = (temp-T_ref) * heating[0] + heating[1]
    
    #DF Pumps have special consideration due to natural gas heating
    if (x == 2 and temp < T_ref):
        NG = demand * 0.81
        demand = 0.19 * demand
        EC = demand / COP
        return COP, EC, NG
        
    elif (x == 2 and temp >= T_ref):
        NG = 0
        EC = demand / COP
        return COP, EC, NG
        

    EG = demand / COP
    
    return COP, EG

##Finds average line at T_ref from a bunch of coeffs and y-axis intercepts
##Parameters:
##coeffs - array of slopes
##intrcpts - array of y-axis intrcpts

def find_avg_line(coeffs, intrcpts):
    coef_np = np.array(coeffs)
    intrcpt_np = np.array(intrcpts)
    
    intrcpt_mod = coef_np * T_ref + intrcpt_np
    
    coef_avg = np.mean(coef_np)
    intrcpt_avg = np.mean(intrcpt_mod)
    
    return [coef_avg, intrcpt_avg]

#Plots a line or a point (func name misleading haha)
def plot_line(coeffs,temps,name,color = "r"):
    
    #So if it's not a singular number aka a point use this
    if(type(coeffs) != float):
        valz = (temps - T_ref) * coeffs[0] + coeffs[1]
        plt.plot(temps, valz,color,label=name)

    else:
        plt.plot(coeffs,temps.item(),"*y",markersize=10,label=name)

    #Formatting
    plt.title("")
    plt.xlabel("Temperature (F)")
    plt.ylabel("COP")
    plt.legend(loc='upper left', fancybox=True, shadow=True)


def main():
    #Ask if want plots
    plotting = input("Want to see plots? (Y/N): ")
    
    #Set axes
    x = np.linspace(T_ref,120)
    x_heating = np.linspace(-20,T_ref)

    #Can add to these coeffs later for better data
    coeff_c_R410a = [-0.0335,-0.0372,-0.0343,-0.0559,-0.0631,-0.0531,-0.0610,-0.0528,-0.0528,-0.0451,-0.0567,-0.0683,-0.0639,-0.0639,-0.0667,-0.0729,-0.0641,-0.0583]
    names_c_R410a = ["D1","D2","D3","D4","D2_1","D2_2","D2_3","D2_4","D2_5","HL","D3_1","D3_2","D4_1","D4_2","D4_3","D5_1","D5_2","D5_3"]
    intrcpts_c_R410a = [6.638,7.446,6.886,8.532,10.298,8.661,9.865,8.598,8.538,7.313,8.558,9.753,9.662,9.667,10.083,11.2865,9.9430,9.118]
    coeff_h_R410a = [0.0378, 0.0513, 0.0418,0.0397, 0.0354,0.0348,0.0323, 0.0295,0.0273,0.0427,0.0387,0.0343,0.0228,0.03442,0.0270,0.0396,0.0355,0.0350]
    names_h_R410a = ["D1_h","D2_h","D3_h","D4_h","D2_1_h","D2_2_h","D2_3_h","D2_4_h","D2_5_h","HL","D3_1_h","D3_2_h","D4_1_h","D4_2_h","D4_3_h","D5_1_h","D5_2_h","D5_3_h"]
    intrcpts_h_R410a = [1.886,1.526,1.703,1.725,2.953,2.879,2.638,2.445,2.214,1.0896,2.2404,2.0080,1.7482,1.9978,1.9857,2.7962,2.5103,2.4816]

    coeff_c_R32 = [-0.0922,-0.0718,-0.0736,-0.0744]
    names_c_R32 = ["ATMO_1","ATMO_2","ATMO_3","ATMO_4"]
    intrcpts_c_R32 = [13.224,10.490,10.323,10.365]
    coeff_h_R32 = [0.0263,0.0218,0.0210,0.0207]
    names_h_R32 = ["ATMO_1_h","ATMO_2_h","ATMO_3_h","ATMO_4_h"]
    intrcpts_h_R32 = [2.0219,1.9564,1.7460,1.7332]

    coeff_c_DF = [-0.03587224,-0.03438607,-0.03449955,-0.03480641,-0.03294711]
    names_c_DF = ["DF1","DF2","DF3","DF4","DF5"]
    intrcpts_c_DF = [7.14939359,6.92641333,6.90018524,7.10030725,6.76392126]
    coeff_h_DF = [0.04563655,0.03822836,0.0339339,0.04007679,0.0387436]
    names_h_DF = ["DF1_h","DF2_h","DF3_h","DF4_h","DF5_h"]
    intrcpts_h_DF = [1.44828783,1.76293939,1.82040643,1.79173888,1.77795695]


    #Which tech they want
    choice = int(input("Please specify your choice: \n1 - Average R410a Model\n2 - Average R32 Model\n3 - Average Dual Fuel Model\n4 - All averages together\n"))
    
    #Outdoor temp (F) and energy demand
    temp = float(input("Enter Outdoor Temperature (F): "))
    demand = float(input("Enter Energy Demand (Answer returned in this unit): "))

    
    #R410a
    if choice == 1:
        cooling = find_avg_line(coeff_c_R410a, intrcpts_c_R410a)
        heating = find_avg_line(coeff_h_R410a, intrcpts_h_R410a)
        COP, demand = energy_consumption(temp,demand, cooling, heating)
        
        print("Energy Demand = " + str(round(demand,2)))
        
        if plotting == "Y" or plotting == "y":
            plot_line(cooling,x,"R410 Avg Cooling")
            plot_line(heating,x_heating,"R410 Avg Heating")
            plot_line(temp, COP,"Chosen Point","y")

            plt.title("Average R410 Model")
            plt.show()
    
    #R32
    elif choice == 2:
        cooling = find_avg_line(coeff_c_R32, intrcpts_c_R32)
        heating = find_avg_line(coeff_h_R32, intrcpts_h_R32)
        COP, demand = energy_consumption(temp,demand, cooling, heating)
        
        print("Energy Demand = " + str(round(demand,2)))
        
        if plotting == "Y" or plotting == "y":
            plot_line(cooling,x,"R32 Avg Cooling")
            plot_line(heating,x_heating,"R32 Avg Heating")
            plot_line(temp, COP,"Chosen Point","y")
            
            plt.title("Average R32 Model")
            plt.show()
    
    #Dual Fuel
    elif choice == 3:
        cooling = find_avg_line(coeff_c_DF, intrcpts_c_DF)
        heating = find_avg_line(coeff_h_DF, intrcpts_h_DF)
        COP, demand, ng = energy_consumption(temp,demand, cooling, heating, 2)
        
        print("Energy Demand = " + str(round(demand,2)))
        print("Natural Gas Demand = " + str(round(ng,2)))

        if plotting == "Y" or plotting == "y":
            plot_line(cooling,x,"DF Avg Cooling")
            plot_line(heating,x_heating,"DF Avg Heating")
            plot_line(temp, COP,"Chosen Point","y")

            plt.title("Average DF Model")
            plt.show()

    
    #All together
    elif choice == 4:
        ##MAKE EACH OF THESE BLOCKS 1 FUNCTION
        cooling_4 = find_avg_line(coeff_c_R410a, intrcpts_c_R410a)
        heating_4 = find_avg_line(coeff_h_R410a, intrcpts_h_R410a)

        cooling_3 = find_avg_line(coeff_c_R32, intrcpts_c_R32)
        heating_3 = find_avg_line(coeff_h_R32, intrcpts_h_R32)

        cooling_d = find_avg_line(coeff_c_DF, intrcpts_c_DF)
        heating_d = find_avg_line(coeff_h_DF, intrcpts_h_DF)
        
        COP1, demand1 = energy_consumption(temp,demand, cooling_4, heating_4)
        COP2, demand2 = energy_consumption(temp,demand, cooling_3, heating_3)
        COP3, demand3, NG = energy_consumption(temp,demand, cooling_d, heating_d,2)
        
        print("Energy Demand R410a = " + str(round(demand1,2)))
        print("Energy Demand R32 = " + str(round(demand2,2)))
        print("Energy Demand Dual Fuel = " + str(round(demand3,2)))
        print("Natural Gas Demand Dual Fuel = " + str(round(NG,2)))

        if plotting == "Y" or plotting == "y":
            plot_line(cooling_4,x,"R410 Avg Cooling")
            plot_line(heating_4,x_heating,"R410 Avg Heating")
            plot_line(cooling_3,x,"R32 Avg Cooling","g")
            plot_line(heating_3,x_heating,"R32 Avg Heating","g")
            plot_line(cooling_d,x,"DF Avg Cooling","b")
            plot_line(heating_d,x_heating,"DF Avg Heating","b")
            
            plot_line(temp, COP1,"Chosen Point R410a","y")
            plot_line(temp, COP2,"Chosen Point R32" ,"y")
            plot_line(temp, COP3,"Chosen Point Dual Fuel","y")

            plt.title("Models")
            
            plt.grid(alpha=0.15)
            plt.show()
    
if __name__ == "__main__":
    main()
    

