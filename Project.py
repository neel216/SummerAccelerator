from matplotlib import pyplot as plt #imports pyplot for plotting data
from matplotlib import style #imports matplotlib styles for graph aesthetics
from scipy.stats.stats import pearsonr #imports scipy function for correlation coefficient calculation
import csv #imports module to read csv files

style.use("ggplot") #Sets style of all graphs as ggplot

#Will hold data directly from csv file
SAT_scores = []
AP_tests = []
graduation_rate = []

#Read csv to obtain SAT statistics and schools
def get_SAT_scores():
    SATscores = open("2010_SAT__College_Board__School_Level_Results.csv", "r")
    read = csv.reader(SATscores)
    for row in read:
        SAT_scores.append(row)

#Read csv to obtain AP statistics and schools
def get_AP_tests():
    APtests = open("2010__AP__College_Board__School_Level_Results.csv", "r")
    read = csv.reader(APtests)
    for row in read:
        AP_tests.append(row)

#Read csv to obtain graudation statistics and schools
def get_graduation_rates():
    Graduation = open("2005-2010_Graduation_Outcomes_-_School_Level.csv", "r")
    read = csv.reader(Graduation)
    for row in read:
        graduation_rate.append(row)

#Calls functions to obtain statistics and schools
get_SAT_scores(), get_AP_tests(), get_graduation_rates()

#Deletes the first row of all statistics (first row is only headers/column titles)
def del_headers(lst1, lst2, lst3):
    del lst1[0]
    del lst2[0]
    del lst3[0]

#Calls function to delete column titles
del_headers(SAT_scores, AP_tests, graduation_rate)

#Filters out all data from graduation rates except data concerning the year 2006
graduation_percent = []
def filter_twentyOsix(lst_of_graduation_rates):
    for school in lst_of_graduation_rates:
        if school[2] == "2006":
            graduation_percent.append(school)

filter_twentyOsix(graduation_rate) #Calls function

#Will hold the schools found in all data sets
AP_schools = []
SAT_schools = []
graduation_schools = []

#Writes the schools in each data set to its respective list
def add_schools(reading_lst, writing_lst):
    for data in reading_lst:
        writing_lst.append(data[0])

#Calls function to write schools of data set to lists
add_schools(AP_tests, AP_schools)
add_schools(SAT_scores, SAT_schools)
add_schools(graduation_percent, graduation_schools)

#Puts the schools each data set has in common into a list
common_AP_SAT_schools = list(set(AP_schools).intersection(SAT_schools))
all_common_schools = list(set(common_AP_SAT_schools).intersection(graduation_schools))

#Will hold statistics after filtering out uncommon schools
updated_SAT_scores = []
updated_AP_tests = []
updated_graduation_rate = []

#Filters data sets to only include schools that each data set has
def add_common_values(lst, updated_lst):
    for school in lst:
        unfiltered_school = school[0]
        for common_school in all_common_schools:
            if unfiltered_school == common_school:
                updated_lst.append(school)

#Calls function to filter out data from schools that is not common
add_common_values(SAT_scores, updated_SAT_scores)
add_common_values(AP_tests, updated_AP_tests)
add_common_values(graduation_percent, updated_graduation_rate)

#Will hold graduation rates after filtration
second_graduation_percent = []
final_graduation_percent = []

#Filters all 2006 statistics that are suppressed
def filter_suppressed_graduation():
    for school in updated_graduation_rate:
        if school[5] != "s":
            second_graduation_percent.append(school)

#Calls function to filter suppressed statistics
filter_suppressed_graduation()

#Converts string from csv to usuable float and remove '%'
def change_percentage():
    for school in second_graduation_percent:
        percent = school[5]
        final_percent = percent.replace("%", "")
        actual_final_percent = float(final_percent)
        final_graduation_percent.append(actual_final_percent)

change_percentage()

#Calculates average SAT scores for every school in filtered data set
avg_SAT_scores = []

def add_SAT_scores(lst_of_scores):
    for school in lst_of_scores:
        score = int(school[3]) + int(school[4]) + int(school[5])
        avg_SAT_scores.append(score)

#Pulls number of AP tests taken per school in filtered data set
AP_tests_taken = []

def add_AP_tests(lst_of_tests_taken):
    for school in lst_of_tests_taken:
        attempts = int(school[3])
        AP_tests_taken.append(attempts)

#Pulls number of AP tests passed per school in filtered data set
AP_tests_passed = []

def add_AP_passed(lst_of_tests_taken):
    for school in lst_of_tests_taken:
        passed = int(school[4])
        AP_tests_passed.append(passed)

#Calls functions to calculate/populate lists to use
add_SAT_scores(updated_SAT_scores)
add_AP_tests(updated_AP_tests)
add_AP_passed(updated_AP_tests)

#Defines x tick space for graphs
xtick = list(range(len(updated_SAT_scores)))

#Graphs SAT scores (bar graph)
def graph_SAT_scores():
    y = avg_SAT_scores
    x = range(len(avg_SAT_scores))
    plt.bar(x , y , color = "blue")
    plt.xlabel("NYC High Schools")
    plt.ylabel("Average SAT Score")
    plt.xticks(xtick[::10])
    plt.xlim(0 , 216)
    plt.title("Average SAT Scores for NYC High Schools")
    plt.show()

#Graphs AP tests taken (bar graph)
def graph_AP_tests():
    y = AP_tests_taken
    x = range(len(AP_tests_taken))
    plt.bar(x , y , color = "blue")
    plt.xlabel("NYC High Schools")
    plt.ylabel("Number of AP Tests Taken")
    plt.xticks(xtick[::10])
    plt.xlim(0 , 216)
    plt.title("Number of AP Tests Taken for NYC High Schools")
    plt.show()

#Graphs AP tests passed (bar graph)
def graph_AP_passed():
    y = AP_tests_passed
    x = range(len(AP_tests_passed))
    plt.bar(x , y , color = "blue")
    plt.xlabel("NYC High Schools")
    plt.ylabel("Number of AP Tests Passed")
    plt.xticks(xtick[::10])
    plt.xlim(0 , 216)
    plt.title("Number of AP Tests Passed for NYC High Schools")
    plt.show()

#Graphs graduation rates (bar graph)
def graph_graduation_percent():
    y = final_graduation_percent
    x = range(len(final_graduation_percent))
    plt.bar(x , y , color = "blue")
    plt.xlabel("NYC High Schools")
    plt.ylabel("Graduation Percentages")
    plt.xticks(xtick[::10])
    plt.xlim(0 , 216)
    plt.title("Graduation Percentages for NYC High Schools")
    plt.show()

#Calls functions to graph *individual* data
graph_SAT_scores(), graph_AP_tests(), graph_AP_passed(), graph_graduation_percent()

#Graphs graduation rates with respect to SAT scores (scatter plot)
def compare_SAT_and_graduation():
    y = final_graduation_percent
    x = avg_SAT_scores
    plt.scatter(x , y , color = "blue", s = 15)
    plt.xlabel("Average SAT Score")
    plt.ylabel("Graduation Percentage")
    plt.title("Graduation Percentage with Respect to Average SAT Score for NYC High Schools")
    plt.show()

#Graphs graduation rates with respect to AP tests passed (scatter plot)
def compare_AP_and_graduation():
    y = final_graduation_percent
    x = AP_tests_passed
    plt.scatter(x , y , color = "blue", s = 15)
    plt.xlabel("Number of AP Tests Passed")
    plt.ylabel("Graduation Percentage")
    plt.title("Graduation Percentage with Respect to Number of AP Tests Passed for NYC High Schools")
    plt.show()

#Graphs correlation graphs
compare_SAT_and_graduation(), compare_AP_and_graduation()

#Calculates and prints Pearson Coefficient / Correlation Coefficient of the scatter plots
SAT_corr = pearsonr(avg_SAT_scores , final_graduation_percent)
AP_corr = pearsonr(AP_tests_passed , final_graduation_percent)

print(SAT_corr)
print(AP_corr)
