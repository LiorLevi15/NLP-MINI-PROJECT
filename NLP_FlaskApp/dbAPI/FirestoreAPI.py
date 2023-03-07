import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from NLP_FlaskApp.Paragraph import Paragraph
import os


home_directory = os.path.expanduser( '~' )
cred = credentials.Certificate(os.path.join(home_directory, ".fireBase/creds"))
firebase_admin.initialize_app(cred)


class Database:
	def __init__(self):
		self.db = firestore.client()
		self.collection_ref = self.db.collection('paragraphs')

	def uploadData(self, paragraph, result):
		dontCare, ref = self.db.collection("paragraphs").add({"Text": f"{paragraph}", "Summary": f"{result}"})
		return ref.id

	def updateRecord(self, recordId, data):
		self.db.collection("paragraphs").document(recordId).update(data)

	def getData(self):
		# Retrieve all documents from the collection
		docs = self.collection_ref.get()

		paragraphs = []
		# Iterate over the documents and print them
		for doc in docs:
			paragraphDict = doc.to_dict()
			paragraphs.append(Paragraph(paragraphDict["Text"], paragraphDict["Summary"]))
			return paragraphs

if __name__=="__main__":
	print("in the db")