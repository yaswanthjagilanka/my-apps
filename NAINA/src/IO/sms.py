import requests


class TextSMS:

    def __init__(self):
        self.url = 'https://www.sms4india.com/api/v1/sendCampaign'
        self.apiKey = "V9JWLUORM8DWLELB1UBWYPT106564U92"
        self.seretKey = "QRKACDE2PN6K1EMP"
        self.useType = "stage"
        self.senderId = "SMSIND"

    def sendPostRequest(self,phoneNo, txtMessage):
        status = []
        for phone in phoneNo :
          req_params = {
          'apikey': self.apiKey,
          'secret':self.secretKey,
          'usetype':self.useType,
          'phone': phone,
          'message':txtMessage,
          'senderid':self.senderId
          }
          response = requests.post(self.url, req_params)
          status.append(response['status'])
        return ((status.count("success")/len(phoneNo))*100)