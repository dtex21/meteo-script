# Script for processing meteorological data
This script processes meteorological data from https://meteosearch.meteo.gr text files(.txt) and calculates mean values of a 10 day period (3 periods for every month) for a number of years.
In particular the values which are calculated are mean, maximum and minimum tempratures, the average wind speeds and rainfall for a 10 day period. This period may have 8 or 9 days for the 3rd period of February (9 for leap years), 10 days for normal months and 11 days for months with 31 days, like January.
## Usage
- Use curl or wget to download the data of the station, for example
>curl https[]()://meteosearch.meteo.gr/"station name"/201[0-5]-12.txt -O
- Enter the command 
>python meteo_script.py -i "input files" -o "output file" -s "starting line" -e "ending line"

#### Flags
- -i : input files (default is 10)
- -o : output file
- -s : the data will be calculated after this line
- -e : the data will be calculated until this line
- -h : help

