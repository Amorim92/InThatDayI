import imaplib, email, getpass, re, datetime
from email.header import decode_header

# Messages IDs, subjects, from, to and dates
# messages_IDs = []
subjects = []
_from = [] 
_to = []
_dates = []

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('joao.ricardo.amorim.ja@gmail.com', getpass.getpass())
mail.select('[Gmail]/All Mail')

dateb = datetime.date.today().strftime("%d-%b-%Y")
date = (datetime.date.today() - datetime.timedelta(30)).strftime("%d-%b-%Y")

result, data = mail.uid('search', None, '(SENTSINCE {date} SENTBEFORE {cena})'.format(date=date, cena=dateb))

ids = data[0]
id_list = ids.split()
for num in id_list:
    result, data = mail.uid('fetch', num, '(BODY.PEEK[HEADER.FIELDS (FROM TO SUBJECT DATE)])')
    raw_email = data[0][1]
    email_message = email.message_from_string(raw_email)
    
    # tuplo=email_message['To'].replace('"','').replace('\'','').split(' <')

    value = decode_header(email_message['SUBJECT'])

    print value
     
    #print email.utils.parseaddr(email_message['From']) # for parsing "Yuji Tomita" <yuji@grovemade.com>
     
    # print subj
    # print froma
    # print to
    # print date
    # print
    # date_tuple = email.utils.parsedate_tz(msg['Date'])
    # if date_tuple:
    #     local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
    #     print "Local Date:", \
    #         local_date.strftime('%d %b %Y %H:%M')

        #  SENTSINCE SENTBEFORE
