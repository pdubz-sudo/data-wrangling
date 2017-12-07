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

headers = "international_degree_programs\n" # make headers and add new line because its a csv

f.write(headers) # writes the headers in your file. Start adding loop result

# loop through containers to extract
for container in containers:
	container_span = container.find_all('span')
	for program in container_span:
		program = program.string
		program_split = re.split(' - M| - B', program) # "|" mean OR. re.split finds multiple patters

		program_name = program_split[0]
		print(program_name.replace(",", "|"))

		##### write loop results into csv. "," makes new columns so change these. Must add new line at the end to deliminate
		f.write(program_name.replace(",", "|") + "\n")

# close file
f.close() 