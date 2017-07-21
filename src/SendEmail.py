import sys
if sys.version_info < (3, 0): # Python 2
	from Tkinter import *
	import tkMessageBox as messagebox
else: # Python 3
	from tkinter import *
	from tkinter import messagebox
	from tkinter import constants
	
from smtplib import *

class Application(Frame):

	senderLabel = Label
	senderEntry = Entry
	senderPasswordLabel = Label
	senderPasswordEntry = Entry
	SMTPServerLabel = Label
	SMTPServerEntry = Entry
	SMTPServerPortLabel = Label
	SMTPServerPortEntry = Entry
	subjectLabel = Label
	subjectEntry = Entry
	receiverLabel = Label
	receiverEntry = Entry

	savedSenderEmail = str()
	savedServerAddress = str()
	savedServerPort = str()

	emailContentLabel = Label
	emailContentBox = Text

	sendButton = Button

	def __init__(self, master = Tk):
		
		if sys.version_info < (3, 0): Frame.__init__(self, master, border = 12)
		else: super().__init__(master, border = 15)

		self.readSettings()
		self.pack(fill = BOTH, expand = True)
		self.create_widgets()

	def create_widgets(self):

		loginFrame = Frame(self)
		loginFrame.pack(side = TOP)

		userInfoLabelFrame = LabelFrame(loginFrame, text = "User info", pady = 4)
		userInfoLabelFrame.grid(row = 0, sticky = E+W)

		senderEmail = "" if not self.savedSenderEmail else self.savedSenderEmail
		defaultSenderEmail = StringVar(userInfoLabelFrame, value = senderEmail)
		self.senderLabel = Label(userInfoLabelFrame, text = "Sender Email:")
		self.senderLabel.grid(row = 0, column = 0)
		self.senderEntry = Entry(userInfoLabelFrame, textvariable = defaultSenderEmail)
		self.senderEntry.grid(row = 0, column = 1)

		self.senderPasswordLabel = Label(userInfoLabelFrame, text = "Password:")
		self.senderPasswordLabel.grid(row = 1, column = 0)
		self.senderPasswordEntry = Entry(userInfoLabelFrame, show = "*")
		self.senderPasswordEntry.grid(row = 1, column = 1)

		serverAddress = "smtp.EMAIL.com" if not self.savedServerAddress else self.savedServerAddress
		defaultServerAddress = StringVar(userInfoLabelFrame, value = serverAddress)
		self.SMTPServerLabel = Label(userInfoLabelFrame, text = "SMTP Server:")
		self.SMTPServerLabel.grid(row = 2, column = 0)
		self.SMTPServerEntry = Entry(userInfoLabelFrame, textvariable = defaultServerAddress)
		self.SMTPServerEntry.grid(row = 2, column = 1)

		serverPort = "587" if not self.savedServerPort else self.savedServerPort
		defaultServerPort = StringVar(userInfoLabelFrame, value = serverPort)
		self.SMTPServerLabel = Label(userInfoLabelFrame, text = "Server Port:")
		self.SMTPServerLabel.grid(row = 3, column = 0)
		self.SMTPServerPortEntry = Entry(userInfoLabelFrame, textvariable = defaultServerPort)
		self.SMTPServerPortEntry.grid(row = 3, column = 1)

		emailInfoLabelFrame = LabelFrame(loginFrame, text = "Email", pady = 4)
		emailInfoLabelFrame.grid(row = 1, sticky = E+W)

		self.subjectLabel = Label(emailInfoLabelFrame, text = "Subject:")
		self.subjectLabel.grid(row = 0, column = 0)
		self.subjectEntry = Entry(emailInfoLabelFrame)
		self.subjectEntry.grid(row = 0, column = 1)

		self.receiverLabel = Label(emailInfoLabelFrame, text = "Receiver:")
		self.receiverLabel.grid(row = 1, column = 0)
		self.receiverEntry = Entry(emailInfoLabelFrame)
		self.receiverEntry.grid(row = 1, column = 1)

		self.sendButton = Button(self, text ="Send", command = self.sendEmailAction, width = 10)
		self.sendButton.pack(side = BOTTOM, fill = Y, expand = True)

		self.emailContentBox = Text(self, width = 45, height = 8, borderwidth = 10, background = "#EEEEEE")
		self.emailContentBox.pack(side = BOTTOM, pady = 5, fill = BOTH, expand = True)

		self.emailContentLabel = Label(self, text = "Message:")
		self.emailContentLabel.pack(side = BOTTOM, pady = 5)

	def sendEmailAction(self):

		sender = str(self.senderEntry.get())
		password = str(self.senderPasswordEntry.get())
		subject = str(self.subjectEntry.get())
		receiver = str(self.receiverEntry.get())
		mailContent = str(self.emailContentBox.get("1.0",'end-1c'))
		serverAddress = str(self.SMTPServerEntry.get())
		serverPort = str(self.SMTPServerPortEntry.get())

		if not sender or not password or not subject or not receiver or not mailContent or not serverAddress or not serverPort:
			messagebox.showerror(title = "Error", message = "Some fields are empty")
		else:
			self.saveSettings(sender, serverAddress, serverPort)
			message = "To: {0}\nFrom: {1}\nSubject:{2}\n\n{3}".format(sender, receiver, subject, mailContent)

			try:
				smtpServer = SMTP(serverAddress, serverPort) # You need to change this address
				smtpServer.ehlo()
				smtpServer.starttls()
				smtpServer.ehlo()
				smtpServer.login(sender, password)
				smtpServer.sendmail(sender, receiver, message)
				smtpServer.close()
				messagebox.showinfo(message = "Successfully sent email")

			except SMTPException:
				messagebox.showerror(title = "Error", message = "Unable to send email")

	def readSettings(self):
		with open("settings", "a+") as file:
			file.seek(0)
			self.savedSenderEmail = file.readline().strip("\n")
			self.savedServerAddress = file.readline().strip("\n")
			self.savedServerPort = file.readline()
			file.truncate()
			file.close()

	def saveSettings(self, senderEmail, serverAddressToSave, serverPortToSave):
		with open("settings", "r+") as file:
			file.seek(0)
			file.write(senderEmail + "\n")
			file.write(serverAddressToSave + "\n")
			file.write(serverPortToSave)
			file.truncate()
			file.close()

if __name__ == '__main__':

	mainWindow = Tk()
	mainWindow.title("Send Email")
	mainWindow.config(background = "green")
	app = Application(master = mainWindow)
	mainWindow.update()
	mainWindow.minsize(mainWindow.winfo_width(), mainWindow.winfo_height())
	mainWindow.maxsize(int(mainWindow.winfo_width() * 1.3), int(mainWindow.winfo_height() * 1.4))
	app.mainloop()
