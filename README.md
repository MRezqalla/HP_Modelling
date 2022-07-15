
# HP Models Guide

## To use final models:
- Go to Models Folder
- Choose Model_Visualization.py to see performance graphs
- Choose m.py for use in projects 
    - m.py can either return consumption if energy demand and temperature were given 
    - or it can return regression coeffecients (Recommended method)

## To data scrape:
- Current files can scrape data from either: DAIKIN Engineering Manuals, DAIKIN (idk what it's called) other format seen below
<img width="696" alt="Screen Shot 2022-07-12 at 2 30 26 PM" src="https://user-images.githubusercontent.com/67717667/178568153-a6a10e7a-e557-4120-900b-d6c384f3ecbd.png">

### For Engineering Manuals
- The following steps must be completed before running the file
- Inside main() in the code change the following:
    - temps_heat to the temperature range in the manual for heating 
    - temps to the temperature range in the manual for cooling
- After running the file:
    - Write the name of the file
    - The program will then ask for the start, end, and "skip"
    - This depends on which of the models you would like to model
    - START - Number of FIRST page of heat pump model
    - END - Number of FIRST page of last heat pump model you want to analyze
    - SKIP - The number of pages between the STARTs of one heat pump and the one after it

### For Other Format (See Pic Above)
- The following steps must be completed before running the file
    - At the TOP of the code, change START, END, and HEAT
        - START - The page number of the beginning of the data for cooling
        - END - The page number of the end of the data for cooling 
        - HEAT - The page number for the heating data
- After running the file:
    - Enter file name
    
    
 For any specific data files reach out to:
 mrezqall@purdue.edu
