import numpy as np
import geopandas as gpd
import model as md
import matplotlib.pyplot as plt

TREF = 18.3333

#2020
#total_gen = [89956915 * 1000, 102505381*1000 ,113459711*1000] #(kWh)
#total_CO2_em = [64775, 77844 ,91554] #(Thousand Metric Ton)

CO2_em_CA = [491 * 0.000453592 * 0.001,446 * 0.000453592 * 0.001,495 * 0.000453592 * 0.001] #Metric ton/kWh
CO2_em_WA = [201 * 0.000453592 * 0.001,302 * 0.000453592 * 0.001,227 * 0.000453592 * 0.001] #Metric ton/kWh
CO2_em_VM = [10 * 0.000453592 * 0.001,6 * 0.000453592 * 0.001,8 * 0.000453592 * 0.001]  #Metric ton/kWh
CO2_em_IN = [1775 * 0.000453592 * 0.001,1671 * 0.000453592 * 0.001,1584 * 0.000453592 * 0.001]  #Metric ton/kWh
#rate = total_CO2_em / total_gen #(Thousand Metric Ton / kWh)

#h_demand = np.loadtxt('house_ff_demand_18.csv', delimiter = ',')
#temps = np.loadtxt('house_temp_18.csv', delimiter = ',')
#
#h_demand = np.append(h_demand, np.loadtxt('house_ff_demand_19.csv', delimiter = ',')[1:],0)
#temps = np.append(temps, np.loadtxt('house_temp_19.csv', delimiter = ',')[1:], 0)
#
#h_demand = np.append(h_demand, np.loadtxt('house_ff_demand_20.csv', delimiter = ',')[1:],0)
#temps = np.append(temps, np.loadtxt('house_temp_20.csv', delimiter = ',')[1:], 0)

coeffs = md.get_coeffs(3)
e_demand = []
emissions_CA = []
emissions_WA = []
emissions_VM = []
emissions_CO2 = []
emissions_IN = []
heating_demand = []
s = coeffs[1][0]
i = coeffs[1][1]
conv_rate = 0.000293
comb_rate = 117


def c_to_f(t):
    return ((t * (9/5)) + 32)
    
for k in range(3):

    x = 18 + k
    h_demand = np.loadtxt('house_ff_demand_' + str(x) + '.csv', delimiter = ',')
    temps = np.loadtxt('house_temp_' + str(x) + '.csv', delimiter = ',')
    rate_CA = CO2_em_CA[k]
    rate_WA = CO2_em_WA[k]
    rate_VM = CO2_em_VM[k]
    rate_IN = CO2_em_IN[k]
    
#    plt.plot(h_demand)
#    plt.show()
    
    for (temp, demand) in zip(temps[1:], h_demand[1:]):
        COP = c_to_f(temp) * s + i
#        elec_demand = (demand * 0.19) / COP #(Dual Fuel)
        elec_demand = (demand) / COP
        e_demand.append(elec_demand * 1000000 * conv_rate) #kwh
        emissions_CA.append(elec_demand * 1000000 * conv_rate * rate_CA) #metric ton
        emissions_WA.append(elec_demand * 1000000 * conv_rate * rate_WA) #metric ton
        emissions_VM.append(elec_demand * 1000000 * conv_rate * rate_VM) #metric ton
        emissions_IN.append(elec_demand * 1000000 * conv_rate * rate_IN)
        heating_demand.append(demand)
#        emissions_CO2.append(demand * comb_rate * 0.000453592 * 0.81) # (Dual Fuel)
        emissions_CO2.append(demand * comb_rate * 0.000453592)
        
        
#        emissions.append(elec_demand * comb_rate * 0.81 * 0.000453592)


temps = np.loadtxt('house_temp_18.csv', delimiter = ',')[1:]
temps = np.append(temps, np.loadtxt('house_temp_19.csv', delimiter = ',')[1:], 0)
temps = np.append(temps, np.loadtxt('house_temp_20.csv', delimiter = ',')[1:], 0)

#print(emissions)

#print(emissions)

total_e_demand = sum(e_demand)
total_CA_emissions = sum(emissions_CA)
total_WA_emissions = sum(emissions_WA)
total_VM_emissions = sum(emissions_VM)
total_IN_emissions = sum(emissions_IN)
CO2_emissions = sum(emissions_CO2)
 
 
print("Electricity demand: " + str(total_e_demand) + " kWh")
print("CA Emissions: " + str(total_CA_emissions) + " metric tons")
print("WA Emissions: " + str(total_WA_emissions) + " metric tons")
print("IN Emissions: " + str(total_IN_emissions) + " metric tons")
print("VM Emissions: " + str(total_VM_emissions) + " metric tons")
print("CO2 Emissions: " + str(CO2_emissions) + " metric tons")


#for (temp, demand) in zip(temps[1:], h_demand[1:]):
#    COP = c_to_f(temp) * s + i
#    elec_demand = demand / COP
#    e_demand.append(elec_demand * 1000000 * conv_rate)
#    emissions.append(elec_demand * 1000000 * conv_rate * rate)

print(type(demand))
print(type(CO2_emissions))
#
fig,ax = plt.subplots()
# make a plot
#ax.plot(e_demand, color="red")
ax.plot(heating_demand, color="red")
# set y-axis label
#ax.set_ylabel("Heating Energy Demand (kWh)",color="red", fontsize=10)
ax.set_ylabel("Heating Energy Demand (MMBTU)",color="red", fontsize=10)
ax2=ax.twinx()
# make a plot with different y-axis using second axis object
ax2.plot(temps[1:],color="blue")

ax2.set_ylabel("Temperature (Celsius)",color="blue",fontsize=10)

#ax3=ax2.twinx()
## make a plot with different y-axis using second axis object
#ax3.plot(emissions,color="green")
#
#ax3.set_ylabel("CO2 emissions (Thousand Metric Ton)",color="green",fontsize=10)

#
#
ax.set_xticklabels(ax.get_xticks(), rotation = 45)
plt.xticks([0,5000,10000,15000,20000,25000], ['January 2018','July 2018','February 2019','August 2019','March 2020','September 2020'])
#

##
###
plt.title("Heating Energy Demand and Temperature vs Time")
##plt.title("Heating Demand and Temperature vs Time")
#fig.savefig('Demand_and_temp.jpg',format='jpg',dpi=600,bbox_inches='tight')
plt.show()
###
###plt.plot(e_demand,"b*")
##plt.plot(temps[1:],"r*")
###plt.ylim(0,15000)
##plt.show()
