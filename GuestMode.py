# FEATURES TO ADD #
'''
* choose FTP connection


'''

# IMPORTS #
from tkinter import *
from tkinter import messagebox
import csv
import ftplib


# FUNCTIONS #
def ftp_menu():
    ftpmenu = Tk()
    ftpmenu.title('FTP')

    # FRAMES #
    frameZero = Frame(ftpmenu)
    frameOne = Frame(ftpmenu)

    # LABELS #
    labelTitleFTP = Label(frameZero, text='FTP Configuration', font=largeFont)

    # GRID #
    labelTitleFTP.grid()
    frameZero.grid(row='0')
    frameOne.grid(row='1')

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

                newEntry = Entry(frameOne, justify='center')  # creates new Entry associated with variable 'newEntry'
                newEntry.grid(row=row_num, column=col_num, padx=5, pady=5)  # adds newEntry to grid
                connections[newCell] = newEntry  # adds new Entry reference to dictionary
                newEntry.insert(0, index)  # inserts request value (song, artist, etc.) into empty Entry in GUI
                col_num += 98  # increments col_num and makes it ready to convert to corresponding letter value

    ftpmenu.mainloop()


def sign_into_ftp(credentials):
    ftp = ftplib.FTP(credentials.get('Domain'))
    ftp.login(credentials.get('Username'), credentials.get('Password'))
    ftp.cwd(credentials.get('Path'))
    print('Signing into %s...' % credentials.get('Name'))
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


def view_requests():
    pull_file(ftp_credentials, 'requests.csv')
    requests_list = []
    with open('requests.csv', 'r') as read:
        request_reader = csv.reader(read)
        row_num = 1
        titles = next(request_reader)
        for row in request_reader:
            if row[2] == '1':
                row[2] = 'YES'
            else:
                row[2] = 'NO'
            if row[3] == '1':
                row[3] = 'YES'
            else:
                row[3] = 'NO'
            if row[4] == '0':
                row[4] = 'NONE'
            requests_list.append('%3s  "%s" by %s' % ((str(row_num) + '.'), row[0], row[1]))
            row_num += 1
    messagebox.showinfo('Request list', '\n'.join(requests_list))


def add_to_file():
    if entrySong.get() == '' and entryArtist.get() == '' and entryNotes.get() == '':
        pass
    else:
        track_info = [entrySong.get(), entryArtist.get(), 0, 0, entryNotes.get()]
        if entryNotes.get() == '':
            track_info[4] = 0

        with open('requests.csv', 'a', newline='') as requests:
            requests_writer = csv.writer(requests)
            requests_writer.writerow(track_info)


def submit_request(*args):
    if entrySong.get() == '' and entryArtist.get() == '' and entryNotes.get() == '':
        pass
    else:
        pull_file(ftp_credentials, 'requests.csv')
        add_to_file()
        push_file(ftp_credentials, 'requests.csv')
        message = (entrySong.get() + ' by ' + entryArtist.get() + ' added to requests!')
        clear_field()
        messagebox.showinfo('Request sent', message)


def clear_field():
    entrySong.delete(0, END)
    entryArtist.delete(0, END)
    entryNotes.delete(0, END)


largeFont = ('Century Gothic', 30)
medFont = ('Century Gothic', 20)
smallFont = ('Century Gothic', 10)
root = Tk()
root.title('Guest Mode')

# FRAMES #
master = Frame(root, bg="black")
frameTop = Frame(master, width="1000", height="400", bg="black")
frameMedium = Frame(master, width="1000", height="400", bg="black")
frameBottom = Frame(master, width="400", height="400", bg="black")

# WIDGETS #
labelTitle = Label(frameTop, text='Request a song', fg="white", bg="black", font=largeFont)
labelFTP = Label(frameTop, text='FTP', fg="white", bg="black", font=largeFont)
labelSong = Label(frameMedium, text="Song title", fg="white", bg="black", font=largeFont)
labelArtist = Label(frameMedium, text="Artist name", fg="white", bg="black", font=largeFont)
labelNotes = Label(frameMedium, text="Notes", fg="white", bg="black", font=largeFont)
labelDetails = Label(frameMedium,
                     text='Give it your best guess, otherwise leave the field blank.', fg="white", bg="black")

entrySong = Entry(frameMedium, font=largeFont)
entryArtist = Entry(frameMedium, font=largeFont)
entryNotes = Entry(frameMedium, font=largeFont)

buttonFTP = Button(frameTop, text='FTP', fg="white", bg="black", font=smallFont, command=ftp_menu)
buttonSubmit = Button(frameBottom, text="Submit", fg="white", bg="black", font=largeFont, command=submit_request)
buttonClear = Button(frameBottom, text="Clear", fg="white", bg="black", font=largeFont, command=clear_field)
buttonView = Button(frameBottom, text="View Requests", fg="white", bg="black", font=largeFont, command=view_requests)

# GRID #
master.grid()
frameTop.grid(row=0)
frameMedium.grid(row=1, padx=20)
frameBottom.grid(row=2, padx=20, pady=10)

labelTitle.grid(row=0, column=2, padx=175, pady=10, columnspan=2)
labelSong.grid(row=0, column=0, sticky="E")
labelArtist.grid(row=1, column=0, pady=5, sticky="E")
labelNotes.grid(row=2, column=0, sticky="E")
labelDetails.grid(row=3, padx=75, columnspan=2)

entrySong.grid(row=0, column=1)
entryArtist.grid(row=1, column=1)
entryNotes.grid(row=2, column=1)

buttonFTP.grid(row=0, column=0)
buttonSubmit.grid(row=0, column=0, padx=5, pady=10)
buttonClear.grid(row=0, column=1, padx=5, pady=10)
buttonView.grid(row=1, column=0, columnspan=2, ipadx=3)

with open('passwords.csv', 'r') as read:
    # Uses the first set of FTP credentials from passwords.csv
    reader = csv.reader(read)
    ftp_list = list(reader)
    ftp_credentials = {'Name': ftp_list[1][0], 'Domain': ftp_list[1][1], 'Username': ftp_list[1][2],
                       'Password': ftp_list[1][3], 'Path': ftp_list[1][4]}

root.bind('<Return>', submit_request)  # Makes the Enter key submit request

root.mainloop()
