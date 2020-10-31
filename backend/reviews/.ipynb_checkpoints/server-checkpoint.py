from flask import Flask,jsonify,request 
import random 
import pyodbc
from Deception import *
from Summarizing import *
from hashlib import md5
from Crypto.PublicKey import DSA
from Crypto import Random
import uuid
app = Flask(__name__)
nltk.download('stopwords') 
     
def add_to_db_review(review):
    conn_dict ={}
    "conn_string = Driver={ODBC Driver 13 for SQL Server};Server=tcp:bazara.database.windows.net,1433;Database=user-db;Uid=ryabuily;Pwd={your_password_here};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
    conn_dict = {}
    for line in conn_string.split(';'):
        if line:
            var, val = line.strip(' ').split('=')
            conn_dict.update({var : val})

    server = conn_dict['Server']
    database = conn_dict['Initial Catalog']
    username = conn_dict['User ID']
    password = conn_dict['Password']
    driver = conn_dict['Driver']

    database = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = database.cursor()
    id_ = uuid.uuid1()
    print(id_,review['uid'],review['prodId'],review['review'],review['summary'],review['polarity'],review['subjectivity'])
    request = "INSERT INTO Review (id,uid,prodId,review,summary,positiveness,targetness) VALUES ('{}','{}','{}','{}','{}',{},{})".format(id_,review['uid'],review['prodId'],review['review'],''.join(review['summary']),review['polarity'],review['subjectivity'])
    print(request)
    cursor.execute(request)
    cursor.commit()
    
    
def add_to_bd(sql_request):
    onn_dict ={}
    conn_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:user-table-server.database.windows.net,1433;Initial Catalog=userTable;Persist Security Info=False;User ID=userTableAdmin;Password=XiaomiRedmiNote7;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;\
        Connection Timeout=30;'
    conn_dict = {}
    for line in conn_string.split(';'):
        if line:
            var, val = line.strip(' ').split('=')
            conn_dict.update({var : val})

    server = conn_dict['Server']
    database = conn_dict['Initial Catalog']
    username = conn_dict['User ID']
    password = conn_dict['Password']
    driver = conn_dict['Driver']

    database = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = database.cursor()
    cursor.execute(sql_request)
    cursor.commit()
 
def sql_request(req: str) -> str:
    conn_string = 'Driver={ODBC Driver 17 for SQL Server};Server=tcp:user-table-server.database.windows.net,1433;Initial Catalog=userTable;Persist Security Info=False;User ID=userTableAdmin;Password=XiaomiRedmiNote7;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;\
        Connection Timeout=30;'
    conn_dict = {}
    for line in conn_string.split(';'):
        if line:
            var, val = line.strip(' ').split('=')
            conn_dict.update({var : val})
    server = conn_dict['Server']
    database = conn_dict['Initial Catalog']
    username = conn_dict['User ID']
    password = conn_dict['Password']
    driver = conn_dict['Driver']
    database = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = database.cursor()
    cursor.execute(req)
    if "SELECT" in req:
        row = str(cursor.fetchone()) + '\n'
        resp = row
        while True:
            row = str(cursor.fetchone())
            if (row != 'None'):
                resp += row + '\n'
            else:
                break
            print(row)
        database.commit()
        return resp
    database.commit()
    return ""

@app.route('/api/v1/addReview',methods = ['POST'])
def post_review():
    str(request)
    text = request.json['text']
    summarizer = Summarizer(text)
    classifier_fake = Classification(None)
    classifier_usability = Classification(None)
    classifier_fake.load('models/simple_70.pkl')
    classifier_usability.load('models/usability.pkl')
    is_fake = classifier_fake.predict(text)
    if is_fake != 'fake':
        usability = classifier_usability.predict(text)
        summary = summarizer.run()
        polarity = summarizer.polarity()
        subjectivity = summarizer.subjectivity()
        tag = summarizer.entities()
        add_to_db_review({'uid':request.json['uid'],'prodId':request.json['prodId'],'review':text,'summary':summary,'polarity':polarity,'subjectivity':subjectivity})
    else:
        usability = -1
        summary = ""
        polarity = -2
        subjectivity = -2
        tag = ""
    is_fake = True if is_fake == 'fake' else False
    return jsonify({'is_fake':is_fake,'usability':str(usability),'subjectivity':str(subjectivity),'polarity':str(polarity),'summary':summary,'tags':tag})


@app.route('/api/v1/addApp',methods=['POST'])
def add_app():
    id_ = uuid.uuid1()
    devId = request.json['devId']
    name = request.json['name']
    exe_path = request.json['exePath']
    screenshot_path = request.json['screenshotPath']
    descript = request.json['descript']
    pending = 1
    request_ = "INSERT INTO Product VALUES ('{}', '{}', '{}', '{}', '{}', '{}', {})".format(
        id_, devId, name, exe_path, screenshot_path, descript, pending
    )
    add_to_bd(request_)
    return jsonify({'status':'OK'})

@app.route('/api/v1/addPurchase')
def add_purchase():
    id_ = uuid.uuid1()
    uid = request.json['uid']
    prodId = request.json['prodId']
    lim = request.json['lim']
    date_time = request.json['date_time']
    publKey = request.json['publKey']
    digSign = req.json['digSign']
    contractPath = req.json['contractPath']
    add_to_bd("INSERT INTO Purchase VALUES ('{}', '{}', '{}', {}, CONVERT(datetime, '{}', 120), '{}', '{}', '{}')".format(
        id, uid, prodId, lim, date_time, publKey, digSign, contractPath
    ))
    add_to_bd(request)
    return jsonify({'status':'OK'})

@app.route('/api/v1/addUserCompany',methods=['POST'])
def add_user_company():
    email = request.json['chiefsEmail']
    number = sql_request("SELECT SUM(count1) FROM \
            (SELECT COUNT(userEmail) AS count1 FROM UserHuman WHERE userEmail = '{0}'\
            UNION \
            SELECT COUNT(chiefsEmail) AS count1 FROM UserCompany WHERE chiefsEmail = '{0}') a".format(email))
    if number[1] == '0':
        privKey = None
        try:
            privKey = DSA.importKey(request.json['privateKey'])
        except KeyError:
            privKey = DSA.generate(1024, Random.new().read) 
        pubKey = privKey.publickey()
        passHash = md5(request.json['passwd'].encode('utf-8')).hexdigest()
        request_ = "INSERT INTO UserCompany\
        VALUES \
        ('{0}', {1}, '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', {9}, '{10}')".format(uuid.uuid1(), 
            request.json['inn'], passHash, request.json['chiefsRealName'], 
            request.json['chiefsIdNumber'], request.json['chiefsEmail'], request.json['payAccount'],
            pubKey.exportKey('PEM').decode(), privKey.exportKey('PEM').decode(), request.json['isSeller'], request.json['name'])
        add_to_bd(request_)
    else:
        return jsonify(
        {
            'Error': "Email %s already registered" % email
        },
            status_code=400
        )
    return jsonify({'Status':'OK'})

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')
