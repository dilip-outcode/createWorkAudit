from os import write
from pydriller import Repository
from datetime import datetime
import datetime
import pandas as pd

WRONG_FORMAT_ERROR_MESSAGE = "An error occured. Please check if you have provided the data in specified format: "
DATA_FRAME = { "S.N.": [], "Email": [], "Assigned Task": [], "Assigned Date": [], "Commit Messages": []}

def userInputToDateTimeObject(user_input): #accepted user input format to use this function for date is: YYYY-MM-DD
    today = datetime.datetime.today()
    try:
        updated_date = datetime.datetime.strptime(user_input + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        print(updated_date)
        if updated_date >= today:
            print("\nCan't track future haha. Please enter a past date.\n")
            return False, None
        return True, updated_date

    except ValueError as e:
        print(e)
        print(WRONG_FORMAT_ERROR_MESSAGE)
        return False, None

def getUserDetailsForAudit():
    project_name = input("Please enter the name of the project for audit: \n")
    total_devs_assigned = 0
    total_email_count = 0
    email_list = []
    task_assigned_list = {}
    task_assigned_date = datetime.datetime.today()
    is_date_updated = False

    while(total_devs_assigned <= 0):
        total_devs_assigned = int(input("\nPlease enter the number of developers whose audit you want to create: \n"))
        if total_devs_assigned <= 0:
            print("Oppssss, You must assign some devs here first. \n Accepted data: Positive Integer \n")

    while total_email_count != total_devs_assigned:
        dev_emails = input("\nPlease enter the emails of the developers assigned. Make sure to seperate the emails with comma (,) if they are multiple in number. [Eg: email1, email2, email3, ...]: \n")
        try:
            dev_emails = dev_emails.split(",")
            total_email_count = len(dev_emails)

            if total_email_count != total_devs_assigned:
                print("Oopss, the number of emails didn't match the number of devs assigned. Please make sure you included all the emails or check if you missed comma somewehre.") 
            else:
                email_list = dev_emails
        except Exception as e:
            print(WRONG_FORMAT_ERROR_MESSAGE + " :" + str(e))
    

    while not is_date_updated:
        updated_date = input("\nPlease enter a date (YYYY-MM-DD). The provided date filters the commit details for the report, including only commits made afterwards.\n" )
        is_date_updated, updated_date = userInputToDateTimeObject(updated_date)
        if(is_date_updated):
            task_assigned_date = updated_date
            print("\nDate to be used for data filter = ", task_assigned_date)

    project_repo_url = input("\nPlease enter the repo url of the project for audit: \n")
    for email in email_list:
        task_assigned_list[email] = input("\nPlease enter the task assigned to {}".format(email))
    print("tasks == ", task_assigned_list)

    return project_name, email_list, project_repo_url, task_assigned_list, task_assigned_date, is_date_updated

def generateWorkAuditBasedOnCommits(project_repo_url, email, index, assigned_task, task_assigned_date, include_remotes=True):
    print('\n project_repo_url = ', project_repo_url)
    print('\n email = ', email)
    print('\n index = ', index)
    print('\n assigned_task = ', assigned_task)
    print('\n task_assigned_date = ', task_assigned_date)

    for commit in Repository(project_repo_url, include_remotes=include_remotes).traverse_commits():
        if email == commit.committer.email:
            DATA_FRAME["S.N."].append(index + 1)
            DATA_FRAME["Email"].append(email)
            DATA_FRAME["Assigned Task"].append(assigned_task)
            DATA_FRAME["Assigned Date"].append(task_assigned_date)
            print(" Commit . message == ", commit.msg)
            DATA_FRAME["Commit Messages"].append(commit.msg if commit.msg else "no commit")

    # return DATA_FRAME
    # print(" data frameee === ", DATA_FRAME)
    # DATA_FRAME = { "S.N.": [], "Email": [], "Assigned Task": [], "Assigned Date": [], "Commit Messages": [], "Remarks": [] }

    
    # return


# git@github.outcode.com:OutCode-Software/dreamdesign-web.git
project_name, email_list, project_repo_url, task_assigned_list, task_assigned_date, is_date_updated  = getUserDetailsForAudit()
print("email list = ", email_list)
# DATA_FRAME = { "S.N.": [], "Email": [], "Assigned Task": [], "Assigned Date": [], "Total Commits": [], "Commit Messages": [], "Remarks": [] }

# get all commit data for all emails and export an excel file accordingly
for index, email in enumerate(email_list):
    index = 1
    generateWorkAuditBasedOnCommits(project_repo_url, email, index, task_assigned_list[email], task_assigned_date)


df = pd.DataFrame(DATA_FRAME, columns=["S.N.", "Email", "Assigned Task", "Assigned Date", "Commit Messages"])
df.to_excel(f'{project_name}_work_audit.xlsx', index=False, header=True)

# data = {"Author": [], "Message": [], "Date": [], "Branch": []}
# # for commit in Repository('https://github.com/OutCode-Software/longweekend-ftl.git', since=datetime.datetime(2021, 6, 16, 12, 0, 0), to=datetime.datetime(2021, 9, 17, 12, 0, 0), include_remotes=True).traverse_commits():

    # data["Author"].append(commit.author.name)
    # data["Message"].append(commit.msg)
    # data["Date"].append(commit.committer_date.strftime('%m/%d/%Y'))
    # data["Branch"].append(commit.branches)
    
# # data frame with column headers as columns here
# df = pd.DataFrame(data, columns=["Author", "Message", "Date", "Branch"])

# # test.xlsx is the file name. as there's no specific path provided, it will save the file in the current directory.
# df.to_excel('EACL_MOBILE.xlsx', index=False, header=True)  