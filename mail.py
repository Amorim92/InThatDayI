import imaplib, email, getpass, re, datetime


# Messages IDs, subjects, from, to and dates
# messages_IDs = []
subjects = []
_from = [] 
_to = []
_dates = []

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('joao.ricardo.amorim.ja@gmail.com', getpass.getpass())
print mail.select('[Gmail]/All Mail') 
result, data = mail.search(None, 'ALL')
ids = data[0]
id_list = ids.split()
for i in id_list:
    typ, data = mail.fetch(i,'(RFC822)')
    msg = email.message_from_string(data[0][1])
    print 'Message %s: %s' % (i, msg['Subject'].encode('utf-8'))
    # print 'Raw Date:', msg['Date']
    date_tuple = email.utils.parsedate_tz(msg['Date'])
    if date_tuple:
        local_date = datetime.datetime.fromtimestamp(
            email.utils.mktime_tz(date_tuple))
        print "Local Date:", \
            local_date.strftime('%d %b %Y %H:%M')