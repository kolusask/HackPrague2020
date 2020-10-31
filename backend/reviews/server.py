from flask import Flask,jsonify,request 
import random 
from Deception import *
from Summarizing import *
app = Flask(__name__)
nltk.download('stopwords') 
     

@app.route('/api/addReview',methods = ['POST'])
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
    else:
        usability = -1
        summary = ""
        polarity = -2
        subjectivity = -2
        tag = ""
    is_fake = True if is_fake == 'fake' else False
    return jsonify({'is_fake':is_fake,'usability':str(usability),'subjectivity':str(subjectivity),'polarity':str(polarity),'summary':summary,'tags':tag})

if __name__ == '__main__':
    app.debug = True
    app.run('0.0.0.0')
