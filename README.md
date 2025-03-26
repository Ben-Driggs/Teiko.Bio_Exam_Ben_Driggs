# Teiko.Bio_Exam_Ben_Driggs
Technical Exam for an Engineering Internship at Teiko.Bio.


# Instructions

Download the Teiko.Bio_Exam.zip folder in the releases section and extract to any location. Using a Unix based system (I used git bash), you can run it by simply running the executable and entering a path for your desired output directory. The program will then output the required outputs. You can create a shortcut to the executable, but it will need to stay in its original folder to work. Source code is also available, and can be run in a similar way (python main.py), but you'll need to make sure you have the right modules installed (pandas, matplotlib, scipy, etc.). Here is a summary of what each file/directory contains:

exam_info.txt -> the exam requirements given by Teiko.Bio

questions.txt -> my responses to each of the exam questions

main.py -> Python code written for the cell count analysis for the coding portion of the exam.

data -> a directory containing cell-count.csv (the input file provided) and each of the following outputs of main.py

Relative_Frequency_Comparisons.png -> A boxplot figure showing the responder and non-responder comparisons for each population
    
sample_cell_data.csv -> A .csv made to store information used for boxplot and statistical analyses
    
significance_tests.txt -> Results of the Mann-Whitney U Test for each population.
