import requests
import json
import time
from keys import MS_COGNITIVE_API_KEY

class SentimentAnalyzer:

    ENDPOINT = 'https://westus.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment'
    HEADERS = { 'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': MS_COGNITIVE_API_KEY }

    def buildData(self, sentences):
        data = {'documents':[]}
        for i in range(0, len(sentences)):
            data['documents'].append({'language':'en', 'id':'{}'.format(i), 'text':'{}'.format(sentences[i])})
        return data

    def analyze(self, sentences):
        sentiment = {}
        start = time.time()
        r = requests.post(SentimentAnalyzer.ENDPOINT, headers=SentimentAnalyzer.HEADERS, data=json.dumps(self.buildData(sentences)))

        print 'Microsoft Cognitive Services API Request -- Elapsed: {} Seconds \n'.format(round(time.time() - start,2))

        for i in json.loads(r.text)['documents']:
            sentiment[i['id']] = i['score']

        time.sleep(2)
        return sentiment
