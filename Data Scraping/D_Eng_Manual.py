# file name: R410A_FRXG_RXG_91215.pdf
    # First page - 10
    # Last Page - 15
    # Skip - 2

import sys
try:
    import tabula as tb
    import pandas as pd
    import numpy as np
    from PyPDF2 import PdfFileWriter, PdfFileReader
    import openpyxl
    import matplotlib.pyplot as plt
    from sklearn import datasets, linear_model
    from sklearn.metrics import mean_squared_error, r2_score
    import os
except:
    sys.exit("Missing Packages")

#Prints final results, prints the cooling and heating eqns
def print_results(coeff_c, intrcpt_c, coeff_h, intrcpt_h):
    for cc,ic,ch,ih in zip(coeff_c, intrcpt_c, coeff_h, intrcpt_h):
        print("COP = T * " + str(cc) + " + " + str(ic))
        print("COP = T * " + str(ch) + " + " + str(ih))
        print("\n")
    
#Uses the data to find the linear regression slopes and returns them
def get_coeffs(rows_to_study_c_heat,rows_to_study_c_cool,temps,temps_heat,plotting):
    i = 0
    regr_c = linear_model.LinearRegression()
    regr_h = linear_model.LinearRegression()
    
    coeff_c = []
    intrcpt_c = []
    coeff_h = []
    intrcpt_h = []
    COP_heating = []
    COP_cooling = []

    for row_h, row_c in zip(rows_to_study_c_heat, rows_to_study_c_cool):
        i = i + 1
        TC_h = row_h[2::3]
        PI_h = row_h[4::3]

        TC_c = row_c[1::2]
        PI_c = row_c[2::2]

        COP_h = np.array(TC_h) / np.array(PI_h)
        COP_c = np.array(TC_c) / np.array(PI_c)

        regr_c = linear_model.LinearRegression()
        regr_h = linear_model.LinearRegression()
        
        # print(COP_c)
        # print(COP_c[:,None])
        regr_c.fit(np.array(temps)[:,None], COP_c[:,None])
        regr_h.fit(np.array(temps_heat)[:,None], COP_h[:,None])

        coeff_c.append(regr_c.coef_)
        coeff_h.append(regr_h.coef_)
        intrcpt_c.append(regr_c.intercept_)
        intrcpt_h.append(regr_h.intercept_)
        COP_heating.append(COP_c)
        COP_cooling.append(COP_h)
        
        x_c = np.linspace(-20,80)
        y_c = x_c * regr_c.coef_[0] + regr_c.intercept_[0]
        y_cr = temps * regr_c.coef_[0] + regr_c.intercept_[0]
        
        x_h = np.linspace(50,130)
        y_h = x_h * regr_h.coef_[0] + regr_h.intercept_[0]
        y_hr = temps_heat * regr_h.coef_[0] + regr_h.intercept_[0]
        
        r2_c = r2_score(COP_c,y_cr)
        r2_h = r2_score(COP_h,y_hr)
        
        print(r2_c,r2_h)

        if plotting == True:
            plt.figure(i)
            plt.title("COP = T * " + str(regr_c.coef_[0][0]) + " + " + str(regr_c.intercept_[0]) + "\n" +"COP = T * " + str(regr_h.coef_[0][0]) + " + " + str(regr_h.intercept_[0]) )
            # plt.title("COP = T * " + str(regr_h.coef_[0][0]) + " + " + str(regr_h.intercept_[0]))
            plt.plot(x_h,y_h)
            plt.plot(x_c,y_c)
            plt.plot(temps, COP_c)
            plt.plot(temps_heat, COP_h)
            
    return coeff_c, intrcpt_c, coeff_h, intrcpt_h, COP_heating, COP_cooling

#Useful data is extracted
def filter_data(datasets):
    g = -1
    AFRs = []
    AFR = 0

    target_row = []
    rows_to_study = []
    for i in range(len(datasets)):
        h = -1
        wrbk = openpyxl.load_workbook("Pump"+str(i+1)+".xlsx")
        for sh in wrbk:
            row_num = 0
            target_row = []
            h = h + 1
            for row in sh.iter_rows():
                row_num = row_num + 1
                for cell in row:
                    if (h == 0 or h == 5):
                        if (g == 1):
                            AFR = cell.value
                            AFRs.append(AFR)
                            g = 0
                        if (cell.value == "AFR"):
                            g = 1
                    else:
                        if (row_num == 6 and cell.value != None):
                            try:
                                # print(cell.value)
                                target_row.append(float(cell.value))
                            except:
                                # print(cell.value)
                                target_row.extend(list(map(float, cell.value.split())))
                        if (cell.value == 4 and row_num != 1):
                            g = 2

            if (len(target_row) != 0):              
                rows_to_study.append(target_row[1:])
                        

    rows_to_study_c = rows_to_study[::2]
    rows_to_study_f = rows_to_study[1::2]

    rows_to_study_c_heat = rows_to_study_c[::2]
    rows_to_study_c_cool = rows_to_study_c[1::2]

    rows_to_study_f_heat = rows_to_study_f[::2]
    rows_to_study_f_cool = rows_to_study_f[1::2]
    
    return AFRs, rows_to_study_c_heat, rows_to_study_c_cool, rows_to_study_f_heat, rows_to_study_f_cool

#Reads the pdf and generates the dataframes
def get_datasets(file):
    datasets = []
    s = int(input("First Page: "))
    e = int(input("Last Page: ")) + 1
    skip = int(input("Skip: ")) 
    
    for i in range(s,e,skip):
        start = i
        end = i + 1
        # # print(start,end)
        data = tb.read_pdf(file, pages=start,lattice=False,pandas_options={'header': None},stream=True)
        datasets.append(data)
    return datasets


#Transforms the dataframes to excel sheets
def generate_excel_files(datasets):
    k = 1
    for dataset in datasets:
        i = 1
        for table in dataset:
            try: 
                with pd.ExcelWriter('Pump' + str(k) + '.xlsx',mode='a') as writer:
                    table.to_excel(writer, sheet_name='Sheet'+str(i))
            except:
                with pd.ExcelWriter('Pump' + str(k) + '.xlsx') as writer:
                    table.to_excel(writer, sheet_name='Sheet'+str(i))
            i = i + 1
        k = k + 1


def main():
    #Must be changed to match specific heat pump
    temps_heat = [50, 68, 86, 95, 104, 115] # is actually for cooling mode...
    temps = [-13, -4, 5, 14, 23, 32, 43, 60] # is actually for heating mode...
    #Make false if you dont like pictures
    plot = True
    
    file = input("ENTER FILE NAME WITH EXTENTION .pdf: ")
    datasets = get_datasets(file)
    generate_excel_files(datasets)
    AFRs, rtsch, rtscc, rtsfh, rtsfc = filter_data(datasets)
    coeff_c, intrcpt_c, coeff_h, intrcpt_h, COP_heating, COP_cooling = get_coeffs(rtsch, rtscc, temps,temps_heat, plot)
    print_results(coeff_c, intrcpt_c, coeff_h, intrcpt_h)
    return COP_heating, COP_cooling, temps, temps_heat # these are ACTUALLY for heating and cooling
    
    
if __name__ == '__main__':
    main()
