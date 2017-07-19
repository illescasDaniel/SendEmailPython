from tkinter import *
from tkinter import messagebox
from smtplib import *

class Application(Frame):

	senderLabel = Label
	senderEntry = Entry
	senderPasswordLabel = Label
	senderPasswordEntry = Entry
	subjectLabel = Label
	subjectEntry = Entry
	receiverLabel = Label
	receiverEntry = Entry

	emailContentLabel = Label
	emailContentBox = Text

	sendButton = Button

	def __init__(self, master = Tk):
		super().__init__(master, border = 15)
		self.pack(fill = BOTH, expand = True)
		self.create_widgets()

	def create_widgets(self):

		loginFrame = Frame(self)
		loginFrame.pack(side = TOP)

		userInfoLabelFrame = LabelFrame(loginFrame, text = "User info", pady = 4)
		userInfoLabelFrame.grid(row = 0, sticky = E+W)

		self.senderLabel = Label(userInfoLabelFrame, text = "Sender:")
		self.senderLabel.grid(row = 0, column = 0)
		self.senderEntry = Entry(userInfoLabelFrame)
		self.senderEntry.grid(row = 0, column = 1)

		self.senderPasswordLabel = Label(userInfoLabelFrame, text = "Password:")
		self.senderPasswordLabel.grid(row = 1, column = 0)
		self.senderPasswordEntry = Entry(userInfoLabelFrame, show = "*")
		self.senderPasswordEntry.grid(row = 1, column = 1)

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

		if not sender or not password or not subject or not receiver or not mailContent:
			messagebox.showerror(title = "Error", message = "Some fields are empty")
		else:
			message = "To: {0}\nFrom: {1}\nSubject:{2}\n\n{3}".format(sender, receiver, subject, mailContent)

			try:
				smtpServer = SMTP("smtp.gmx.com", 587)
				smtpServer.ehlo()
				smtpServer.starttls()
				smtpServer.ehlo()
				smtpServer.login(sender, password)
				smtpServer.sendmail(sender, receiver, message)
				smtpServer.close()
				messagebox.showinfo(message = "Successfully sent email")

			except SMTPException:
				messagebox.showerror(title = "Error", message = "Unable to send email")

if __name__ == '__main__':

	mainWindow = Tk()
	mainWindow.title("Send Email")
	mainWindow.config(background = "green")
	#mainWindow.resizable(width = False, height = False)
	app = Application(master = mainWindow)
	mainWindow.update()
	mainWindow.minsize(mainWindow.winfo_width(), mainWindow.winfo_height())
	mainWindow.maxsize(int(mainWindow.winfo_width() * 1.3), int(mainWindow.winfo_height() * 1.4))
	app.mainloop()
