from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

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


for container in containers:
	container_programs = container.find_all('a')
	# f.write("\n"+ container.h3.text)  # better to have no letter labeling just in case csv is turned into a dictionary
	print("\n" + container.h3.text)
	for program in container_programs:
		major = program.text

		print(major)

		##### write loop results into csv. "," makes new columns so change these. Must add new line at the end to deliminate
		f.write(major.replace(",", "|") + "\n" )

# close file
f.close() 