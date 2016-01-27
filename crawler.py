from selenium import webdriver
import getpass
from bs4 import BeautifulSoup
import smtplib
import os
import time
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
#from pyvirtualdisplay import Display

URLLOGIN = "https://css.adminapps.cornell.edu"
URLSEARCH = "https://css.adminapps.cornell.edu/psc/cuselfservice/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None"

def send_msg(user, pwd, recipient, subject, body):
    gmail_user = user
    gmail_pwd = pwd
    FROM = user
    TO = recipient if type(recipient) is list else [recipient]
    SUBJECT = subject
    TEXT = body

    # Prepare actual message
    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

def login(netid, netid_pwd):
    browser.get(URLSEARCH)

    username = browser.find_element_by_id("netid")
    password = browser.find_element_by_id("password")

    username.send_keys(netid)
    password.send_keys(netid_pwd)

    browser.find_element_by_name("Submit").click()

def craper(phone_number, email_recv):

    browser.get(URLSEARCH)
    
    try:
        # we have to wait for the page to refresh, the last thing that seems to be updated is the title
        WebDriverWait(browser, 10).until(EC.title_contains("Enrollment Shopping Cart"))

        print '+++++++++++++++++++++++++++++++'
        print 'Webpage Titile:', browser.title
        print '+++++++++++++++++++++++++++++++'


        soup = BeautifulSoup(browser.page_source, "html.parser")
        #print soup

        for i in range (1,9):
            id = 'trSSR_REGFORM_VW$0_row' + str(i)
            class_info = soup.find_all('tr', {'id': id})
            try:
                class_info_pro = class_info[0].contents
                #print class_info_pro
                print '++++++++++++++'
                class_name_pre = class_info_pro[3]
                class_name = [text for text in class_name_pre.stripped_strings][0]
                print class_name
                class_status = class_info_pro[13].find_all('img')[0].get('alt')
                print class_status
                print '++++++++++++++'
                if class_status == 'Open':
                    
                    browser.find_element_by_id("DERIVED_REGFRM1_LINK_ADD_ENRL$82$").click()
                    
                    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
                    WebDriverWait(browser, 10).until(EC.title_contains("Student Enrollment-Add"))

                    # You should see "cheese! - Google Search"
                    print '+++++++++++++++++++++++++++++++'
                    print 'Webpage Titile:', browser.title
                    print '+++++++++++++++++++++++++++++++'
                   
                    browser.find_element_by_id("DERIVED_REGFRM1_SSR_PB_SUBMIT").click()
                    print 'wait 10 sec for webpage loading...'
                    time.sleep(10)

                    html_file = open('%s/final.html'%(os.path.dirname(os.path.abspath(__file__))),'w')
                    html_file.write(browser.page_source.encode('utf-8'))

                    print '+++++++++++++++++++++++++++++++'
                    print 'Webpage Titile:', browser.title
                    print '+++++++++++++++++++++++++++++++'

                    msg_div = browser.find_element_by_id("win0divDERIVED_REGFRM1_SS_MESSAGE_LONG$0")
                    msg_text = msg_div.text
                    status_div = browser.find_element_by_id("win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0")
                    status_text = status_div.find_element_by_tag_name("img").get_attribute('alt')
                    print 'message:', msg_text
                    print 'status:', status_text

                    print "Sending text message now..."
                    send_msg('xyg125@gmail.com', 'GXYgxy125', '%s@txt.att.net'%(phone_number), 'Class Info Reminder', "%s's status now is %s !"%(class_name, class_status))
                    print "Sending text message now..."
                    send_msg('xyg125@gmail.com', 'GXYgxy125', '%s@txt.att.net'%('6073799117'), 'Class Info Reminder', "%s's status now is %s !"%(class_name, class_status))
                    print "Sending email now..."
                    send_msg('xyg125@gmail.com', 'GXYgxy125', email_recv, 'Class Info Reminder', "%s's status now is %s !"%(class_name, class_status))

                    print "Sending text message now..."
                    send_msg('xyg125@gmail.com', 'GXYgxy125', '%s@txt.att.net'%(phone_number), 'Class Info Reminder', "You have '%s' enrolled in '%s' AND msg status is '%s'!!!"%(status_text, class_name, msg_text))
                    print "Sending email now..."
                    send_msg('xyg125@gmail.com', 'GXYgxy125', email_recv, 'Class Info Reminder', "You have '%s' enrolled in '%s' AND msg status is '%s'!!!"%(status_text, class_name, msg_text))
                    
                    browser.quit()
            except:
                pass

    finally:
        print "End"
        #browser.quit()
        #display.stop()
        




# main:
print "+++++++++++++++++++++++++++++++++++++++++"
print "    Welcome to class picking helper"
print "       Please follow the steps"
print "         entering what needed"
print "+++++++++++++++++++++++++++++++++++++++++"
flag = raw_input('Would you like to read your personal info from "login.txt" ? (yes/no): ')
if flag == 'yes':

    try:
        login_file = open('%s/login.txt'%(os.path.dirname(os.path.abspath(__file__))),'r')
        infos = login_file.read().split('\n')
        login_file.close()

        netid = infos[0]
        netid_pwd = infos[1]
        phone_number = infos[2]
        email_recv = infos[3]
    except:
        print 'Failed to open "login.txt", file may not exist !!!'
        flag = 'no'

if flag == 'no':

    netid = raw_input('Enter your netid: ')
    netid_pwd = getpass.getpass('Enter your netid password: ')
    phone_number = raw_input('Enter your phone number(Only supports AT&T): ')
    email_recv = raw_input('Enter your email used to receive msg: ')

    is_save = raw_input('Would you like to save your personal info in "login.txt" ? (yes/no): ')

    if is_save == 'yes':
        login_file = open('%s/login.txt'%(os.path.dirname(os.path.abspath(__file__))), 'w')
        login_file.write(netid+'\n')
        login_file.write(netid_pwd+'\n')
        login_file.write(phone_number+'\n')
        login_file.write(email_recv)
        login_file.close()
        print 'Successfully saved "login.txt" !!!'

# Display:
# display = Display(visible=0, size=(800, 600))
# display.start()
# Browser:
browser = webdriver.Firefox()
# Login:
login(netid, netid_pwd)
# Loop:
count = 0
while(True):
    print "+++++++++++++++++++++++++++++++++++++++++"
    print "         The", str(count), "time run this file !"
    print "               CLASS   INFO"
    print "+++++++++++++++++++++++++++++++++++++++++"
    print "                waiting..."
    craper(phone_number, email_recv)
    count += 1
    print "rest for 5 sec..."
    time.sleep(5)
