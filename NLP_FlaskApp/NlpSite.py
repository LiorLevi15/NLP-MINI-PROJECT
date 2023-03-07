
from flask import Flask, redirect, request, render_template, url_for

from dbAPI.FirestoreAPI import Database
from huggingFaceApi import query

app = Flask(__name__)
db = Database()
q1 = "text for q1"
q2 = "text for q2"
q3 = "text for q3"
q4 = "text for q4"
q5 = "text for q5"

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/query", methods=['POST', 'GET'])
def posted():
    queryText = request.form.get("paragraphInput")
    userQuery = query(queryText)
    try:
        response = userQuery.query()
        resultText = response[0]['generated_text']
        new_text = ''.join([char for char in resultText if char in "אבגדהוזחטיכלמנסעפצקרשתץםןף.,\"!:; ()'"])
        print(f"this is new text {new_text}")
        recordIdNum = db.uploadData(queryText, new_text)
        print("This is the record number we got from the db-----",recordIdNum)
        return redirect(url_for(".getResult", result=new_text, recordId=recordIdNum))
    except:
        resultText = "Sorry we didn't found an answer :("
        recordIdNum="0"
        return redirect(url_for(".getResult", result=resultText, recordId=recordIdNum))
@app.route("/survey/<string:result>/<string:recordId>")
def getResult(result, recordId):
    print(result)
    if result == "Sorry we didn't found an answer :(":
        return redirect(url_for(".thanks", text=result))
    print("this is the record Id---------", recordId)
    return render_template("survey.html", q1=q1, q2=q2, q3=q3, q4=q4, q5=q5, content=result, ID=recordId)
@app.route("/thanks/<string:text>", methods=['POST', 'GET'])
def thanks(text):
    return render_template("thanks.html", content=text)
@app.route("/submitForm", methods=['POST', 'GET'])
def submitSurvey():
    name = request.form.get("name")
    email = request.form.get("email")
    occ = request.form.get("occ")
    a1 = request.form.get("q1")
    a2 = request.form.get("q2")
    a3 = request.form.get("q3")
    a4 = request.form.get("q4")
    a5 = request.form.get("q5")
    avg = (int(a1) + int(a2) + int(a3) + int(a4) + int(a5)) / 5
    recordId = request.form.get("recordId")
    print(name, email, occ, a1,a2,a3,a4,a5,avg, recordId)
    data = {'name':name, 'email':email, 'q1':a1, 'q2':a2, 'q3':a3, 'q4':a4, 'q5':a5, 'occupation':occ, 'avg':avg}
    #Store the response in db
    db.updateRecord(recordId, data)
    return redirect(url_for(".thanks", text="Thanks For Helping Us"))
@app.route("/backHome", methods=['POST', 'GET'])
def backHome():
    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run()