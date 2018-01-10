# FEATURES TO ADD #
'''
* FTP configuration
  * radiobuttons to choose which connection to use
* queued/played checkboxes
* automatically check boxes with value of '1'
* remove entire line from requests.csv
'''

# IMPORTS #
from tkinter import *
import csv
import ftplib
import os


def default_ftp():
    with open('passwords.csv', 'r') as read:
        reader = csv.reader(read)
        ftp_list = list(reader)
        ftp_credentials = {'Name': ftp_list[1][0], 'Domain': ftp_list[1][1], 'Username': ftp_list[1][2],
                           'Password': ftp_list[1][3], 'Path': ftp_list[1][4]}
        return ftp_credentials


def ftp_menu():
    ftpmenu = Tk()
    ftpmenu.title('FTP')

    # FRAMES #
    frameZero = Frame(ftpmenu)
    frameOne = Frame(ftpmenu)
    frameTwo = Frame(ftpmenu)

    # LABELS #
    labelTitleFTP = Label(frameZero, text='FTP Configuration', font=largeFont)

    # GRID #
    labelTitleFTP.grid()
    frameZero.grid(row='0')
    frameOne.grid(row='1')
    frameTwo.grid(row='2')

    with open('passwords.csv', 'r') as read:
        cells = []
        connections = {}
        password_reader = csv.reader(read)
        titles = next(password_reader)
        Label(frameOne, text="Connection Name").grid(row="0", column="0")
        Label(frameOne, text="Domain").grid(row="0", column="1")
        Label(frameOne, text="Username").grid(row="0", column="2")
        Label(frameOne, text="Password").grid(row="0", column="3")
        Label(frameOne, text="Path").grid(row="0", column="4")
        row_num = 0
        intvars = {}
        for row in password_reader:
            row_num += 1
            col_num = 97  # the letter 'a'
            for index in row:
                char = chr(col_num)  # converts col_num to its associated letter
                newCell = (
                        'cell' + str(row_num) + char)  # creates new cell name (e.g. 'cell8c' in eighth row, third col)
                cells.append(newCell)  # adds new cell name to list
                col_num -= 97  # changes col_num to corresponding number value (for grid placement)

                '''
                # WIP to use checkbuttons for queued and played as opposed to entries
                if col_num == 2 or col_num == 3:  # queued or played
                    intvars[newCell] = IntVar()
                    newCheckbutton = Checkbutton(frameMiddle, variable=intvars[newCell].get())
                    if index == '1':
                        print(index)
                        newCheckbutton.select()
                    newCheckbutton.grid(row=row_num, column=col_num)  # adds newCheckbutton to grid
                    entry[newCell] = newCheckbutton  # adds new Checkbutton reference to dictionary
                    print(intvars[newCell].get())
                else:
                    newEntry = Entry(frameMiddle,
                                     justify='center')  # creates new Entry associated with variable 'newEntry'
                    newEntry.grid(row=row_num, column=col_num)  # adds newEntry to grid
                    entry[newCell] = newEntry  # adds new Entry reference to dictionary
                    newEntry.insert(0, index)  # inserts request value (song, artist, etc.) into empty Entry in GUI
                '''

                newEntry = Entry(frameOne, justify='center', font=medFont)  # creates new Entry associated with variable 'newEntry'
                newEntry.grid(row=row_num, column=col_num, padx=5, pady=5)  # adds newEntry to grid
                connections[newCell] = newEntry  # adds new Entry reference to dictionary
                newEntry.insert(0, index)  # inserts request value (song, artist, etc.) into empty Entry in GUI
                col_num += 98  # increments col_num and makes it ready to convert to corresponding letter value

        row_num += 1
        newNameFTP = Entry(frameOne, justify='center', font=medFont)
        newDomainFTP = Entry(frameOne, justify='center', font=medFont)
        newUsernameFTP = Entry(frameOne, justify='center', font=medFont)
        newPasswordFTP = Entry(frameOne, justify='center', font=medFont)
        newPathFTP = Entry(frameOne, justify='center', font=medFont)

        buttonSubmit = Button(frameTwo, text="Save and close", font=medFont)
        buttonClose = Button(frameTwo, text="Close without saving", font=medFont, command=ftpmenu.destroy)

        newNameFTP.grid(row=row_num, column="0")
        newDomainFTP.grid(row=row_num, column="1")
        newUsernameFTP.grid(row=row_num, column="2")
        newPasswordFTP.grid(row=row_num, column="3")
        newPathFTP.grid(row=row_num, column="4")

        buttonSubmit.grid(row=0, column=0)
        buttonClose.grid(row=0, column=1)

        newNameFTP.insert(0, "New connection")

    ftpmenu.mainloop()


def sign_into_ftp(credentials):
    ftp = ftplib.FTP(credentials.get('Domain'))
    ftp.login(credentials.get('Username'), credentials.get('Password'))
    ftp.cwd(credentials.get('Path'))
    print('\nSigning into %s...' % credentials.get('Name'))
    # DO NOT FORGET TO ftp.quit() AFTER FUNCTION CALL
    return ftp


def pull_file(credentials, filename):
    ftp = sign_into_ftp(credentials)
    print('Downloading %s...' % filename)
    ftp.retrbinary('RETR %s' % filename, open(filename, 'wb').write)
    ftp.quit()
    print(filename, 'downloaded\n')


def push_file(credentials, filename):
    ftp = sign_into_ftp(credentials)
    print('Uploading %s...' % filename)
    ftp.storbinary('STOR %s' % filename, open(filename, 'rb'))
    ftp.quit()
    print(filename, 'uploaded\n')


def display_csv():
    pull_file(ftp_credentials, 'requests.csv')
    with open('requests.csv', 'r') as read:
        request_reader = csv.reader(read)
        titles = next(request_reader)
        Label(frameMiddle, text="Song title").grid(row="0", column="0")
        Label(frameMiddle, text="Artist name").grid(row="0", column="1")
        Label(frameMiddle, text="Queued").grid(row="0", column="2")
        Label(frameMiddle, text="Played").grid(row="0", column="3")
        Label(frameMiddle, text="Notes").grid(row="0", column="4")
        clear_names()  # redundant? delete?
        row_num = 0
        intvars = {}
        for row in request_reader:
            row_num += 1
            col_num = 97  # the letter 'a'
            for index in row:
                char = chr(col_num)  # converts col_num to its associated letter
                newCell = (
                        'cell' + str(row_num) + char)  # creates new cell name (e.g. 'cell8c' in eighth row, third col)
                names.append(newCell)  # adds new cell name to list
                col_num -= 97  # changes col_num to corresponding number value (for grid placement)

                '''
                # WIP to use checkbuttons for queued and played as opposed to entries
                if col_num == 2 or col_num == 3:  # queued or played
                    intvars[newCell] = IntVar()
                    newCheckbutton = Checkbutton(frameMiddle, variable=intvars[newCell].get())
                    if index == '1':
                        print(index)
                        newCheckbutton.select()
                    newCheckbutton.grid(row=row_num, column=col_num)  # adds newCheckbutton to grid
                    entry[newCell] = newCheckbutton  # adds new Checkbutton reference to dictionary
                    print(intvars[newCell].get())
                else:
                    newEntry = Entry(frameMiddle,
                                     justify='center')  # creates new Entry associated with variable 'newEntry'
                    newEntry.grid(row=row_num, column=col_num)  # adds newEntry to grid
                    entry[newCell] = newEntry  # adds new Entry reference to dictionary
                    newEntry.insert(0, index)  # inserts request value (song, artist, etc.) into empty Entry in GUI
                '''

                newEntry = Entry(frameMiddle, justify='center', font=medFont)  # creates new Entry associated with variable 'newEntry'
                newEntry.grid(row=row_num, column=col_num, padx=5, pady=5)  # adds newEntry to grid
                entry[newCell] = newEntry  # adds new Entry reference to dictionary
                newEntry.insert(0, index)  # inserts request value (song, artist, etc.) into empty Entry in GUI
                col_num += 98  # increments col_num and makes it ready to convert to corresponding letter value


def write_to_csv():
    pull_file(ftp_credentials, 'requests.csv')
    with open('requests.csv', 'r', newline='') as temp:
        # reader = csv.reader(temp)
        # requestsRows = sum(1 for row in reader)
        with open('temp.csv', 'a', newline='') as temp:
            writer = csv.writer(temp)
            writer.writerow(['Song', 'Artist', 'Queued', 'Played', 'Notes'])
            values = []
            i = 0
            for cell in names:
                values.append(entry[cell].get())
                if i == 4:
                    writer.writerow(values)
                    values = []
                    i = 0
                else:
                    i += 1
            '''
            tempRows = sum(1 for row in writer)
            if requestsRows > tempRows:
                i = 0
                for row in reader:
                    i += 1
                    if i >= requestsRows:
                        writer.writerow(row)
             '''
    clear_names()
    os.remove('requests.csv')
    os.rename('temp.csv', 'requests.csv')
    push_file(ftp_credentials, 'requests.csv')
    display_csv()


def clear_names():
    global names
    names = []


largeFont = ('Century Gothic', 30)
medFont = ('Century Gothic', 15)
smallFont = ('Century Gothic', 10)
root = Tk()
root.title('DJ Mode')

# FRAMES #
frameTop = Frame(root)
frameMiddle = Frame(root)
frameBottom = Frame(root)

# LABELS #
title = Label(frameTop, text='DJ Mode', font=largeFont)

# BUTTONS #
submit = Button(frameBottom, text='Submit', font=medFont, command=write_to_csv)
refresh = Button(frameBottom, text='Refresh', font=medFont, command=display_csv)
FTPconfig = Button(frameTop, text='FTP', font=smallFont, command=ftp_menu)

# GRID #
frameTop.grid(row=0)
frameMiddle.grid(row=1)
frameBottom.grid(row=2)

FTPconfig.grid(row=0, column=0)
title.grid(row=0, column=1, padx=465)
submit.grid(row=0, column=0)
refresh.grid(row=0, column=1)

# MAIN CODE #
names = []
entry = {}
ftp_credentials = default_ftp()
default_ftp()
display_csv()


# root.bind('<Return>', write_to_csv)  # Makes the Enter key write to csv

mainloop()
