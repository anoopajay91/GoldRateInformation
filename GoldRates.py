import requests
from bs4 import BeautifulSoup
import smtplib
import datetime
import time
import os

##############################################################################
# Enter BIOS settings on system, on my system it was DEL while booting.     ##
# Enter Power Management.                                                   ##
# Resume Alarm option, enter the time.                                      ##
# System will wake up at the set time everyday.                             ##
# Go to task scheduler, schedule a task a minute after the system wakes up. ##
# Code to shut down the system once the job is done in the same py file.    ##
##############################################################################

def sendMail(message):
    fromaddr = '' #useraddress@gmail.com
    toaddrs  = [] #'useraddress1@gmail.com', 'useraddress2@gmail.com',
    username = '' #useraddress@gmail.com
    password = '' #password
    subject = 'Gold rates in Bangalore'
    server = smtplib.SMTP('smtp.gmail.com:587')
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username,password)
        message = "Subject: Gold rates in Bangalore\n\n"+message
        server.sendmail(fromaddr,toaddrs,message)
        server.close()     
    
    except Exception as e:
        with open('C:\goldrateError.txt','a+') as f:
            f.write(str(e)+":"+str(datetime.datetime.now())+'\n')


def sendSms(sms):
    s = requests.Session()
    r = s.post('http://site24.way2sms.com/Login1.action',data={'username':'Your mobile Number','password':'Your Password'})
    uid =  r.url[r.url.find('?id')+4:]
    numbers=[] #provide all the numbers separated by comma to whom you want to send the message
    for number in numbers:
        z = s.post('http://site24.way2sms.com/smstoss.action',cookies = r.cookies,params={'ssaction':'ss',
                                                                                      'Token':uid,
                                                                                      'mobile':number,
                                                                                          'message':sms,
                                                                                      'msgLen':str(140 - len(sms))})
        soup = BeautifulSoup(z.content)
        element  = soup.find('div',{'class':'stat'}).select('div p span')[0].text
        #or q = soup.select('div[class="stat"] div p span')
        print element
        time.sleep(5)
    
    
r = requests.get('http://www.indiagoldrate.com/gold-rate-in-bangalore-today.htm')
soup = BeautifulSoup(r.text)

ratesMail = soup.select('table[class="innerTable"]')
ratesMsg = soup.select('table[class="innerTable"] tr')
tableHeaders = soup.select('table th')
tableHeadersText =map(lambda x: x.encode('ascii','ignore'), map(lambda x:x.text,tableHeaders))

x=0
if tableHeadersText.index('22 Karat') < tableHeadersText.index('24 Karat'):
    x = 1


sms = "\nx="+str(x)+"\nGold Rate\n22 Karat"+ratesMsg[0].text.encode('ascii','ignore') +"24 Karat"+ ratesMsg[5].text.encode('ascii','ignore')
ratesMail = map(lambda x:x.text.encode('ascii','ignore'),ratesMail)
ratesMail = map(lambda x: x.replace('\n\n\n','\n'),ratesMail)
message = '\nx='+str(x)+'\n22 Karat:'+ratesMail[0]+'24 Karat:'+ratesMail[1]
#print message
sendMail(message)
sendSms(sms)
os.system('shutdown /s /t 0') #shutdown system after sending mail and message


