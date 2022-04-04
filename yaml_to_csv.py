
import sys
import re
import yaml
  
    

file_to_read = open('data1.yml', mode='r', encoding='latin_1')
file_to_write = open('output.csv', mode='w', encoding='latin_1')

file_to_write.write(f"assignment_id,highest_grade\n") # header of the output file

# =================== Variables ====================
path = 'data1.yml/' # path starts from the input file's name
substring = "assignment"   # key word to idetify assignment records
leader = ['', 0.0]  # initial name and score of leader student
flag = False
string_to_write = ''# string to write to the output file

# ==================== Start processing ====================
while True:

    # Read file by lines
    line = file_to_read.readline()

    # if line is empty, end of file is reached
    # so we write the last 'string_to_write' to the output file
    if not line:
        if string_to_write:
            file_to_write.write(f"\"{string_to_write}\",{leader[0]}\n")
        break

    # looking for and analyzing 'student_string' - lines with names and scores
    student_string = re.search("^.+\s\w.*\d$", line)
    if student_string:
        # memorize the path into the 'string_to_write'
        if flag:
            string_to_write = path

        # looking for a leader student
        possible_leader = line.strip().split(": ")
        if float(possible_leader[1]) > float(leader[1]):
            leader = possible_leader

        # move 'path' to the initial value for the next assignment record
        path = 'data1.yml/'
        flag = False

    # if not a 'student_string' - looking for an 'assignment' keyword
    # and write the path and a leader student name to the output file
    else:
        if substring in line:
            line = line.strip() [:-1]
            path = path + line
            if string_to_write:
                file_to_write.write(f"\"{string_to_write}\",{leader[0]}\n")
            leader = ['', 0.0]
            flag = True

        # this part forms nested path
        else:
            line = line.strip() [:-1]
            path = path + line + "/"

file_to_read.close()
file_to_write.close()
