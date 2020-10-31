from Deception import *
from Summarizing import *


def process(text):
    classifier_fake = Classification(None)
    classifier_us = Classification(None)
    summarizer = Summarizer(text)
    classifier_fake.load('../models/simple_70.pkl')
    classifier_us.load('../models/usability.pkl')
    fake_answer = classifier_fake.predict(text)
    if fake_answer != 'fake':
        usability =  classifier_us.predict(text)
        summary = summarizer.run()
        polarity = summarizer.polarity()
        subjectivity = summarizer.subjectivity()
        tag = summarizer.entities()
    else:
        usability = None
        summary = None
        polarity = None
        subjectivity = None
        tag = None
    return fake_answer,usability,polarity,subjectivity,summary,tag



if __name__ == '__main__':
    print(process("Version 1.x: supports version 1.x of the runtime. This version of the tools is only supported on Windows computers and is installed from an npm package. With this version, you can create functions in experimental languages that are not officially supported. For more information, see Supported languages in Azure Functions"))