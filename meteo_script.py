import sys
import codecs
import math
from optparse import OptionParser

input_file_normal = []  #array of normal year files to be used for rain_calculation
input_file_leap = []    #array of leap year files to be used for rain_calculation
data = []               #generic array to store data

mean_temp = []          #mean tempratures
max_temp = []           #maximum tempratures
min_temp = []           #minimum tempratures
mean_wind_speed = []    #mean wind speeds
sum_of_sums = []       #a summary of 10day mean values for rainfall

def main():
    inputfile = ""
    outputfile = ""
    parser = OptionParser()
    
    start_line = 0          #1st 10d -> 10, 2nd 10d -> 20, 3rd 10d ->30
    end_line = 0            #1st 10d -> 21, 2nd 10d -> 31, 3rd 10d ->if 10: 41, elif 11: 42 else: 40
    days_interval = 10      #either 8, 9, 10 or 11 days, default is 10
    n = 10                  #number of arguments, default is 10
    
    parser.add_option("-i", "--input", dest = "inputfile", action = "append", nargs = n,
                      help = "Input files", metavar = "FILE")
    parser.add_option("-o", "--output", dest = "outputfile", 
                      help = "Output file", metavar = "FILE")
    parser.add_option("-s", "--startline", type = "int", dest = "start_line", 
                      help = "The line where the calculation will start")
    parser.add_option("-e", "--endline", type = "int", dest = "end_line",
                      help = "The line where the calculation will end")
    
    (options, args) = parser.parse_args()
    
    days_interval = (options.end_line - 1) - options.start_line
    
    if options.start_line < 10 or options.end_line > 42:
        parser.error("Lines out of bounds")
    elif days_interval < 8 or days_interval > 11:
        parser.error("Interval of days must be between 8 and 11 days")
        
    get_rain_data(options, days_interval)

    get_data(options)

    output_file = open(options.outputfile, "a")
    output_file.write("____---~~ ~~---____\n")      #a simple border between 10day period values
   
    output_to_file(1, mean_temp, options)
    output_to_file(2, max_temp, options)
    output_to_file(4, min_temp, options)
    output_to_file(9, mean_wind_speed, options)
    
    if days_interval == 9:                                              #for 3rd 10day period of feb
        rain_calculation(input_file_leap, options, days_interval)       #for leap years
        rain_calculation(input_file_normal, options, days_interval - 1) #for normal years
        rain_to_file(options)
    else:                                                               #for everything else
        rain_calculation(input_file_normal, options, days_interval)
        rain_to_file(options)

def get_rain_data(options, days_interval):
    year_strings = []               #an array of years, in order to get the leap years
    
    for file in options.inputfile:
        for f in file:
            year_strings.append(f[:4])
        
    if days_interval == 9:
        for year in year_strings:
            index = int(year) - int(year_strings[0])
            if float(year) % 4 == 0:
                input_file_leap.append(file[index])
            else:
                input_file_normal.append(file[index])
    else:
        for file in options.inputfile:
            for f in file:
                input_file_normal.append(f)

def get_data(options):
    temp = []
    
    for in_file in options.inputfile:
        for i in in_file:
            file = codecs.open(i, "r", "iso-8859-15")
            with file as f:
                for i, line in enumerate(f):
                    if i > options.start_line and i < options.end_line:
                        temp.append(line.split())

    for row in temp:                #for cleaning empty entries, because of missing data
        if len(row) == 1:
            row.clear()

    for row in temp:
        for cell in row:
            data.append(cell)
        
def get_array_name(array):
    return next(x for x in globals() if globals()[x] is array)

def output_to_file(x, array, options):
    sum = 0.0
    mean = 0.0
    
    array_name = get_array_name(array)
    
    for i in  range(x, len(data), 13):      #x is the column, because the files have 13 columns each
        array.append(data[i])
    
    for element in array:
        if element == "---":                #missing values in the files may be displayed as ---
            array.remove(element)
        else:
            sum += float(element)
        
    mean = round(sum / len(array), 2)
    
    output_file = open(options.outputfile, "a")
    output_file.write(f"{array_name} : ")
    output_file.write(str(mean))
    output_file.write("\n")
    output_file.close()

def rain_calculation(input_file, options, days_interval):
    temp = []
    rain_calculation = []
    rain = []               #rainfall
    rain_temp = []
    
    sum = 0.0
    
    weight = get_weight(days_interval)
    
    for in_file in input_file:
        file = codecs.open(in_file, "r", "iso-8859-15")
        with file as f:
            for i, line in enumerate(f):
                if i > options.start_line and i < options.end_line:
                    temp.append(line.split())
                        
    for row in temp:
        if len(row) == 1:
            row.clear()
            
    for row in temp:
        for cell in row:
            rain_calculation.append(cell)
            
    for i in range(8, len(rain_calculation), 13):
        rain.append(rain_calculation[i])
        
    for i in range(0, len(rain), days_interval):
        rain_temp.append(rain[i:i + days_interval])
       
    for row in rain_temp:
        sum = 0.0
        for cell in row:
            sum += float(cell)
        sum_of_sums.append(sum * weight)

def rain_to_file(options):
    total_sum = 0.0
    total_mean = 0.0
    
    for i in sum_of_sums:
        total_sum += i
    
    total_mean = round(total_sum / len(sum_of_sums), 2)
    
    output_file = open(options.outputfile, "a")
    output_file.write("rain : ")
    output_file.write(str(total_mean))
    output_file.write("\n")
    output_file.close()

def get_weight(days_interval):  #either 1, 10/11, 10/9 or 10/8, depends on number of days, default is 1
    if days_interval == 8:
        weight = 10/8
    elif days_interval == 9:
        weight = 10/9
    elif days_interval == 11:
        weight = 10/11
    else:
        weight = 1
    return weight

if __name__ == "__main__":
    main()
