import sys, os, re
import imaplib

class Gmail(object):
	def __init__(self, email_address, password=''):
		self.m = imaplib.IMAP4_SSL('imap.gmail.com', 993)
		self.m.login(email_address,password)
		self.m.select()

	def list_folders(self):
		"""
		list_folders: lists all folders in the e-mail account
		"""
		(status, folder_list) = self.m.list()

		folder_names = []
		for f in folder_list:
			label = f.split('"')[-2] # HACKY: parsing this can get messy
			folder_names.append(label)

		return folder_names

	def select_folder(self, folder_name=None):
		"""
		select_folder: sets a particular folder as the current working folder. None=inbox
		"""
		self.m.select(folder_name)

	def get_message_ids(self, folder_name=None):
		"""
		get_message_ids: get the list of message ids in the folder
		"""
		if folder_name:
			self.select_folder(folder_name)

		try:
			response, items = self.m.search(None, "ALL")		
			items = items[0].split() 
			return items
		except imaplib.IMAP4.error:
			return []

	def get_message(self, message_id):
		"""
		get_message: retrieve a message from a folder by id
		"""
		(resp, data) = self.m.fetch(message_id, "(RFC822)") # fetching the mail, "`(RFC822)`" means "get the whole stuff", but you can ask for headers only, etc
		return data[0][1]

	def get_all_messages_from_folder(self, folder_name=None):
		"""
		get_all_messages_from_folder: convenience method to loop through and return all messages in a folder
		"""
		message_data = []
		for message_id in self.get_message_ids(folder_name):
			message_data.append(self.get_message(message_id))

		return message_data

	def create_message(self, to_addr, from_addr, subject='', text=''):
		"""
		create_message: create a new e-mail message
		"""
		msg = email.Message.Message()
		msg['To'] = to_addr
		msg['From'] = from_addr
		msg['Subject'] = subject

		print email.message_from_string(msg)

class MineGmail(object):

	def __init__(self, username, password, folders=['Inbox']):
		self.g = Gmail(username, password)
		self.folders = folders
		print username
		print password
		print folders

	def get_messages(self):
		# gather data from our e-mail
		msg_data = {}
		for folder_name in self.folders:
			print "pulling shit from list serve ..."
			msg_data[folder_name] = self.g.get_all_messages_from_folder(folder_name)

		print msg_data

	def get_message_ids(self):
		emails = {}
		ids = self.g.get_message_ids()
		return ids

	def dump(self):
		ids = self.get_message_ids()

		indx = 0
		for theid in ids:
			
			if indx > 1: continue
			
			fout = open('emails.txt','a')
			email = self.g.get_message(theid)
			fout.write(email)
			fout.close()
			indx += 1
	
		data = open('email.txt').read()
		urls = re.findall(r">http:\/\/(.*)<",data,re.MULTILINE) #
		for url in urls:
			print url
		
if __name__ == "__main__":
	myaccount = MineGmail(sys.argv[1], sys.argv[2])
	myaccount.dump()
