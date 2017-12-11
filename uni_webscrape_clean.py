from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re

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

# loop through containers to extract
for container in containers:
	container_span = container.find_all('span') # degree programs can be found in span tag
	for program in container_span:
		program = program.string
		program_split = re.split(' - Ma| - B', program) # "|" mean OR. re.split splits on multiple patters. Can't use ' - M'... 
														# because there is several in some programs

		program_name = program_split[0]  # program name is first element in the split... 
										 #second element is education level, or there was no split at all


		# most programs have now been split into several elements so we loop through to clean the education levels
		for data in program_split:  
			category = None
			if 'ster' in data:
				category = "Master"
			elif 'achelor' in data:
				category = 'Bachelor'
			else:
				category = 'N/A'
		print("program: {} education, level: {}".format(program_name.replace(",", "|"), category))

		##### write loop results into csv. "," makes new columns so change these. Must add new line at the end to deliminate
		f.write(program_name.replace(",", "|") + "," + category + "\n")

# close file
f.close() 