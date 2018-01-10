from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
import itertools

my_url = "http://www.lunduniversity.lu.se/lubas/programs"


# open connection and downloading the web page
download = urlopen(my_url)
page_html = download.read() # dumping everything as HTML
download.close() # close the internet connection

# parse
page_soup = soup(page_html, "html.parser")

# university programs were grouped by letter so make containers based on 
# the program grouping
containers = page_soup.find_all("div", class_="program-group")


# make filename for csv file and open the file to start writing into
filename = "lund_university_programs.csv"
f = open(filename, "w")

headers = "international_degree_program" + "," + "education_level\n" # make headers and add new line because its a csv

f.write(headers) # writes the headers in your file. Start adding loop result


########### make 2 lists of program names and education levels so that they can be put together in 1 list
# get span tag in each container (17 containers total)
container_span = [container.find_all("span") for container in containers]

# flatten list of lists with itertools
span_list = list(itertools.chain.from_iterable(container_span))

# extract string from HTML span tag
programs_string = [item.string for item in span_list]

# list: re-assign, split, and clean education levels of each program
education_levels = ["Master" if "aster" in program else "Bachelor" if "achelor" in program else "N/A"
                    for program in programs_string]
programs_split = [re.split(" - Ma| - B", program) for program in programs_string]

# list: program names
# simultaneously keep only program name and avoid "," delimiter problems
programs_name = [program[0].replace(",", "|") for program in programs_split]

# merge lists
keys, values = programs_name, education_levels
final_list = list(zip(keys, values))

print([element for element in final_list])

# write to csv
[f.write(name[0] + " , " + name[1] + "\n") for name in final_list]

f.close() 