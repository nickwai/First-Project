# =====importing libraries===========
'''This is the section where you will import libraries'''
from datetime import datetime, date

# ====Login Section====
'''Here you will write code that will allow a user to login.
    - Your code must read usernames and password from the user.txt file
    - You can use a list or dictionary to store a list of usernames and passwords from the file.
    - Use a while loop to validate your user name and password.
'''


def user_dictionary():  # read the user information from user.txt and store it into user_dictionary
    with open('user.txt', 'r') as user_file:
        user_dict = {}
        for file_line in user_file:
            user_name, user_pw = file_line.split(",")
            user_dict[user_name] = user_pw.strip()
    return user_dict


def reg_user(user_id):  # function for register new user
    if user_id != 'admin':  # set a condition that only allow admin to register user
        print('Only "admin" is allowed to register user!\n')
    else:
        file = open('user.txt', 'a+')
        reg_name = input('Enter the username: ')
        while True:
            if reg_name == '':
                reg_name = input('Username cannot be empty! Enter the username again: ')
            else:
                if reg_name in user_dictionary():  # check is the reg_name a new username in a user.txt
                    reg_name = input('User already exit, please enter the username again: ')
                else:
                    break
        reg_password = input('Enter the password: ')
        while True:
            if reg_password == '':
                reg_password = input('Password cannot be empty! Enter the password again: ')
            else:
                break
        con_pass = input('Confirm your password: ')
        print('')
        while True:  # request user to enter the password again and verify it
            if con_pass != reg_password:
                reg_password2 = input('Password is not match! Enter the password again: ')
                con_pass = reg_password2
                print('')
            else:
                data = f'\n{reg_name}, {reg_password}'
                file.write(data)
                break
        file.close()


def add_task():  # function for add a new task and write it to tasks.txt
    file1 = open('tasks.txt', 'a+')
    person = input('\nEnter the username who you want to assign the task to:  ')
    while True:
        if person not in user_dictionary():
            person = input(f'"{person}" is not a registered user! Please enter the username again: ')
        else:
            title = input('Enter a title of a task: ')
            description = input('Enter a description of the task: ')

            while True:
                today = date.today()
                current_date = today.strftime('%d/%m/%Y')
                last_date = input('Enter the task due date (dd/mm/yyyy): ')
                due_date = datetime.strptime(last_date, '%d/%m/%Y')  # ask user enter the due date and convert the format
                print('')
                if due_date < datetime.today():
                    print('The date that you enter cannot be earlier than today!\n')
                else:
                    data2 = f'\n{person}, {title}, {description}, {current_date}, {last_date}, No'
                    file1.write(data2)
                    # print(data2)
                    break
            break
    file1.close()


def tasks_count(login_name):  # Count how many tasks for a particular user from tasks.txt
    with open('tasks.txt', 'r') as file1:
        tasks = file1.readlines()
        counter = 0
        for lines in tasks:
            task_index = lines.split(', ')
            if task_index[0] == login_name:
                counter += 1
    return counter


def check_overdue():  # function for check the total overdue tasks for every registered user
    od_tasks_dict = {}
    with open('tasks.txt', 'r') as file1:
        overdue_data = file1.readlines()
        for id_name in user_dictionary():  # initial all users overdue task as 0
            od_tasks_dict[id_name] = 0
        for id_name in user_dictionary():
            od_task = 0
            for od_line in overdue_data:
                od_item = od_line.split(', ')
                if id_name == od_item[0]:
                    if od_item[5].lower() == 'no\n' or od_item[5].lower() == 'no':
                        duedate = datetime.strptime(od_item[4], '%d/%m/%Y')  # covert the due date format
                        if duedate < datetime.today():  # compare the due date to today's date, if task is overdue,
                            od_task += 1                # user over due variable + 1
                            od_tasks_dict[id_name] = od_task
    return od_tasks_dict


'''task_overview.txt should contain:
▪ The total number of tasks that have been generated and tracked using the task_manager.py.
▪ The total number of completed tasks.
▪ The total number of uncompleted tasks.
▪ The total number of tasks that haven’t been completed and that are overdue.
▪ The percentage of tasks that are incomplete.
▪ The percentage of tasks that are overdue.'''


def task_overview():  # function for print out all tasks overview
    total_comp = 0
    total_uncomp = 0
    total_od = 0
    with open('tasks.txt', 'r') as file1:
        tasks_data = file1.readlines()
        for num in tasks_data:
            task_comp = num.split(', ')
            if task_comp[5].lower() == 'yes\n' or task_comp[5].lower() == 'yes':
                total_comp += 1
            elif task_comp[5].lower() == 'no\n' or task_comp[5].lower() == 'no':
                total_uncomp += 1
        for overdue_count in check_overdue():
            total_od += check_overdue()[overdue_count]
    with open('task_overview.txt', 'w') as file2:
        file2.write("========== Task Overview Report ========== \n\n")
        file2.write(f'The total number of tasks:                                          {len(tasks_data)}\n')
        file2.write(f'The total number of completed tasks:                                {total_comp}\n')
        file2.write(f'The total number of uncompleted tasks:                              {total_uncomp}\n')
        file2.write(f'The total number of tasks that have not been completed and overdue: {check_overdue()}\n')
        file2.write(
            f'The percentage of tasks that are incomplete:                        '
            f'{total_uncomp / (len(tasks_data)) * 100}%\n')
        file2.write(
            f'The percentage of tasks that are overdue:                           '
            f'{(total_od / total_uncomp) * 100}%\n\n')


def tasks_assigned_dictionary(task_list_line):  # function for counting how many tasks assigned to each user
    task_dict = {}
    for user_key in user_dictionary():
        task_dict[user_key] = 0
        task_assigned = 0
        for usertask_line in task_list_line:
            login_user = usertask_line.split(', ')
            if user_key == login_user[0]:
                task_assigned += 1
                task_dict[user_key] = task_assigned
    return task_dict


'''user_overview.txt should contain:
▪ The total number of users registered with task_manager.py.
▪ The total number of tasks that have been generated and
tracked using task_manager.py.
▪ For each user also describe:
▪ The total number of tasks assigned to that user.
▪ The percentage of the total number of tasks that have
been assigned to that user
▪ The percentage of the tasks assigned to that user that
have been completed
▪ The percentage of the tasks assigned to that user that
must still be completed
▪ The percentage of the tasks assigned to that user that
have not yet been completed and are overdue'''


def user_overview():
    file1 = open('tasks.txt', 'r')
    user_task = file1.readlines()
    file1.close()
    comp_task_dict = {}
    incomp_task_dict = {}
    total_users = 0
    for loginID in user_dictionary():  # initial complete and incomplete task list for all users and set it set 0
        comp_task_dict[loginID] = 0
        incomp_task_dict[loginID] = 0
        total_users += 1
    for name_id in user_dictionary():
        total_task_comp = 0
        total_task_incomp = 0
        for user_task_line in user_task:  # check if the task is completed or incomplete
            task_obj = user_task_line.split(', ')
            if name_id == task_obj[0]:
                if task_obj[5].lower() == 'yes\n' or task_obj[5].lower() == 'yes':
                    total_task_comp += 1
                    comp_task_dict[name_id] = total_task_comp
                elif task_obj[5].lower() == 'no\n' or task_obj[5].lower() == 'no':
                    total_task_incomp += 1
                    incomp_task_dict[name_id] = total_task_incomp
    # use loop to write all the user overview report to user_overview.txt
    with open('user_overview.txt', 'w') as file3:
        file3.write("========== User Overview Report ========== \n\n")
        file3.write(f'The total number of users registered in a Task Manager System is: {total_users}\n\n')
        for key, value in tasks_assigned_dictionary(user_task).items():
            file3.write(f'"{key}": The total number of tasks assigned to is {value}\n')
        file3.write('\n')
        for key1, value1 in tasks_assigned_dictionary(user_task).items():
            file3.write(
                f'"{key1}": The percentage of the total number of tasks that have been assigned to is '
                f'{(int(value1) / len(user_task)) * 100}%\n')  # tasks assigned / total tasks * 100
        file3.write('\n')
        for key2, value2 in comp_task_dict.items():
            if tasks_assigned_dictionary(user_task)[key2] == 0:
                file3.write(f'"{key2}": Not being assigned a task\n')  # if no task being assigned, print this message
            else:
                file3.write(
                    f'"{key2}": The percentage of the tasks assigned to that have been completed is '
                    # completed tasks / assigned tasks * 100
                    f'{(int(value2) / tasks_assigned_dictionary(user_task)[key2]) * 100}%\n')
        file3.write('\n')
        for key3, value3 in incomp_task_dict.items():
            if tasks_assigned_dictionary(user_task)[key3] == 0:
                file3.write(f'"{key3}": Not being assigned a task\n')  # if no task being assigned, print this message
            else:
                file3.write(
                    f'"{key3}": The percentage of the tasks assigned to that must still be completed is '
                    # incomplete tasks / assigned tasks * 100
                    f'{(int(value3) / tasks_assigned_dictionary(user_task)[key3]) * 100}%\n')
        file3.write('\n')
        for key4, value4 in check_overdue().items():
            if tasks_assigned_dictionary(user_task)[key4] == 0:
                file3.write(f'"{key4}": The percentage of the tasks assigned to that have not yet been completed '
                            f'and overdue is 0%\n')
            else:
                file3.write(
                    f'"{key4}": The percentage of the tasks assigned to that have not yet been completed '
                    f'and overdue is '
                    # overdue tasks / assigned tasks * 100
                    f'{(int(value4) / tasks_assigned_dictionary(user_task)[key4]) * 100}%\n')


def view_all():  # read all the tasks from tasks.txt and print it out
    file1 = open('tasks.txt', 'r')
    task_list = file1.readlines()
    for list_data in task_list:
        line2 = str(list_data)
        new_line = line2.strip('\n').split(', ')
        print(f'Assigned to:            {new_line[0]}\n'
              f'Task:                   {new_line[1]}\n'
              f'Task description:       {new_line[2]}\n'
              f'Date assigned:          {new_line[3]}\n'
              f'Due date:               {new_line[4]}\n'
              f'Task complete:          {new_line[5]}\n')
    file1.close()


def view_mine(vm_name):  # print all the tasks for the current login user
    job_counter = 0
    for list_content in replace_lines(vm_name):
        user_alltask = str(list_content)
        user_alltask2 = user_alltask.strip('\n').split(', ')
        if user_alltask2[1] == vm_name:
            job_counter += 1
            print(f'Task number:            {user_alltask2[0]}\n'
                  f'Assigned to:            {user_alltask2[1]}\n'
                  f'Task:                   {user_alltask2[2]}\n'
                  f'Task description:       {user_alltask2[3]}\n'
                  f'Date assigned:          {user_alltask2[4]}\n'
                  f'Due date:               {user_alltask2[5]}\n'
                  f'Task complete:          {user_alltask2[6]}\n')


def replace_lines(login_id):  # add a task number for every registered user and store it into a variable 'list_lines'
    task_number = 1
    lines_index = 0
    file1 = open('tasks.txt', 'r')
    list_lines = file1.readlines()
    file1.close()
    for task_line in list_lines:
        task_line = task_line.split(', ')
        if task_line[0] == login_id:
            task_line = list(str(task_number)) + task_line
            text = ', '.join(task_line)
            list_lines[lines_index] = text
            task_number += 1
            lines_index += 1
        else:
            task_line = list('1') + task_line
            text = ', '.join(task_line)
            list_lines[lines_index] = text
            lines_index += 1
    return list_lines


# function for letting user choose a particular incomplete task and mark as complete
def mark_task_complete(comp_name):
    file1 = open('tasks.txt', 'r')
    mc_tasklist = file1.readlines()
    file1.close()
    mc_line_num = 0
    user_input = input('\nEnter the task number you want to mark the task as complete: ')
    if not user_input.isdigit():  # check is the user input a digit
        print('\nInvalid input. It must be a number!')
    elif int(user_input) > tasks_count(comp_name) or int(user_input) <= 0:  # set a condition only allow user to enter
        print(f'\nThere has no task number "{user_input}"')             # the tasks number that assigned to user
    else:
        for mc_task_item in replace_lines(comp_name):
            mc_task_item = mc_task_item.split(', ')
            if comp_name == mc_task_item[1] and user_input == mc_task_item[0]:
                if mc_task_item[6].lower() == 'yes\n' or mc_task_item[6].lower() == 'yes':  # check is the task complete
                    print(f'\nTask "{user_input}" is completed, you cannot edit it.')
                    mc_line_num += 1
                elif mc_task_item[6].lower() == 'no\n' or mc_task_item[6].lower() == 'no':  # change 'No' to 'Yes'
                    mc_task_item[6] = 'Yes\n'
                    mc_tasklist[mc_line_num] = ', '.join(mc_task_item[1:7])
                    mc_line_num += 1
                    with open('tasks.txt', 'w') as new_text:  # update and replace the task, write it to tasks.txt
                        new_text.writelines(mc_tasklist)
            else:
                mc_line_num += 1


def edit_task(edit_name):  # function for edit the task
    file1 = open('tasks.txt', 'r')
    new_tasklist = file1.readlines()
    file1.close()
    line_num = 0
    selection = input('\nEnter the task number you want to edit: ')
    if not selection.isdigit():  # check is the user input a digit
        print('\nInvalid input. It must be a number!')
    elif int(selection) > tasks_count(edit_name) or int(selection) <= 0:  # set a condition only allow user to enter
        print(f'\nThere has no task number "{selection}"')            # the tasks number that assigned to user
    else:
        for task_item in replace_lines(edit_name):
            task_item = task_item.split(', ')
            if edit_name == task_item[1] and selection == task_item[0]:
                if task_item[6].lower() == 'yes\n' or task_item[6].lower() == 'yes':  # check is the task complete
                    print(f'\nTask "{selection}" has been done, you cannot edit it.')
                    break
                elif task_item[6].lower() == 'no\n' or task_item[6].lower() == 'no':
                    menu = input('''\nSelect one of the following Options below:
a - Edit the username to whom the task is assigned
d - Edit the task due date
: ''').lower()
                    if menu == 'a':
                        assignee = input('\nEnter the username who you want to assign the task to: ')
                        if assignee not in user_dictionary():  # check is a registered user
                            print('The username is not a registered user!\n')
                        elif assignee in user_dictionary():
                            task_item[1] = assignee
                            new_tasklist[line_num] = ', '.join(task_item[1:7])
                        line_num += 1
                    elif menu == 'd':
                        while True:
                            task_item[5] = input('Enter the task due date (dd/mm/yyyy):  ')
                            # covert the task creation date format
                            date_create = datetime.strptime(task_item[4], '%d/%m/%Y')
                            # convert the new due date format
                            new_duedate = datetime.strptime(task_item[5], '%d/%m/%Y')
                            if new_duedate < date_create:
                                # check is the new due date < task creation date
                                print('The due date cannot be earlier than the task creation date!\n')
                            else:
                                print(', '.join(task_item))
                                new_tasklist[line_num] = ', '.join(task_item[1:7])
                                line_num += 1
                                break
                    else:
                        print('\nYou have made a wrong choice! Please choose option "a" or "d".')
            else:
                line_num += 1
            new_text = open('tasks.txt', 'w')
            new_text.writelines(new_tasklist)  # update and replace the task, write it to tasks.txt
            new_text.close()


def sub_vm(login_username):  # function for view mine task
    while True:
        menu = input('''\nSelect one of the following Options below:
 s - Select a specific task to edit
-1 - Return to the main menu
: ''').lower()
        if menu == '-1':
            break
        elif menu == 's':
            menu = input('''\nSelect one of the following Options below:
mc - Mark the task as complete
et - Edit the task
: ''').lower()
            while True:
                if menu == 'mc':  # if menu = mc, call the mark_task_complete function
                    mark_task_complete(login_username)
                    break
                elif menu == 'et':  # if menu = et, call the edit_task function
                    edit_task(login_username)
                    break
                else:  # if input not equal to 'mc' or 'et', print error message
                    print('\nYou have made a wrong choice! Please choose option "mc" or "et".')
                    break
        else:  # if input not equal to 's' or '-1', print error message
            print('\nYou have made a wrong choice! Please choose option "s" or "-1".')


# main program
name = input('Enter your username: ')
password = input('Enter your password: ')
while True:
    if name in user_dictionary():  # check login username/ password is same as the information in user.txt
        while True:
            if password != user_dictionary()[name]:
                password = input('Password is invalid! Please enter it again: ')
            elif password == user_dictionary()[name]:
                print('\n===== Welcome to the Task Manager System =====')
                break
        break
    else:
        name = input('Username is invalid! Please enter it again: ')

while True:
    # presenting the menu to the user and
    # making sure that the user input is convert to lower case.
    menu = input('''\nSelect one of the following Options below:
r - register user
a - adding a task
va - view all tasks
vm - view my task
gr - generate reports ('admin' option)
ds - display statistics ('admin' option)
e - exit
: ''').lower()

    if menu == 'r':
        '''In this block you will write code to add a new user to the user.txt file
        - You can follow the following steps:
            - Request input of a new username
            - Request input of a new password
            - Request input of password confirmation.
            - Check if the new password and confirmed password are the same.
            - If they are the same, add them to the user.txt file,
            - Otherwise you present a relevant message.'''
        reg_user(name)

    elif menu == 'a':
        '''In this block you will put code that will allow a user to add a new task to task.txt file
        - You can follow these steps:
            - Prompt a user for the following:
                - A username of the person whom the task is assigned to,
                - A title of a task,
                - A description of the task and
                - the due date of the task.
            - Then get the current date.
            - Add the data to the file task.txt and
            - You must remember to include the 'No' to indicate if the task is complete.'''
        add_task()

    elif menu == 'va':
        '''In this block you will put code so that the program will read the task from task.txt file and
         print to the console in the format of Output 2 in the task PDF(i.e. include spacing and labelling)
         You can do it in this way:
            - Read a line from the file.
            - Split that line where there is comma and space.
            - Then print the results in the format shown in the Output 2
            - It is much easier to read a file using a for loop.'''
        view_all()

    elif menu == 'vm':
        '''In this block you will put code the that will read the task from task.txt file and
         print to the console in the format of Output 2 in the task PDF(i.e. include spacing and labelling)
         You can do it in this way:
            - Read a line from the file
            - Split the line where there is comma and space.
            - Check if the username of the person logged in is the same as the username you have
            read from the file.
            - If they are the same print it in the format of Output 2 in the task PDF'''
        if tasks_count(name) == 0:  # call the function tasks_count to check is any task being assigned to the user
            print('\nNo task has been assigned to you!')
        else:
            view_mine(name)
            sub_vm(name)

    elif menu == 'gr':
        if name != 'admin':
            print('Only "admin" is allow to generate a statistics report!\n')
        else:  # call the functions to generate a "task_overview" and "user_overview" report
            task_overview()
            user_overview()
            print(f'"task_overview" and "user_overview" report generated successfully!')

    elif menu == 'ds':
        if name != 'admin':
            print('Only "admin" is allow to view the statistics report!\n')
        else:
            try:  # if reports already generated, read it and print it to the display
                with open('task_overview.txt', 'r') as file4:
                    for task_ov in file4:
                        task_ov = task_ov.strip('\n')
                        print(task_ov)
                with open('user_overview.txt', 'r') as file5:
                    for user_ov in file5:
                        user_ov = user_ov.strip('\n')
                        print(user_ov)
            except FileNotFoundError:  # if reports are not there, generate it,  read and print to the display
                task_overview()
                with open('task_overview.txt', 'r') as file4:
                    for task_ov in file4:
                        task_ov = task_ov.strip('\n')
                        print(task_ov)
                user_overview()
                with open('user_overview.txt', 'r') as file5:
                    for user_ov in file5:
                        user_ov = user_ov.strip('\n')
                        print(user_ov)

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
