import mechanize
import StringIO
from datetime import datetime
import re
from bs4 import BeautifulSoup
import MySQLdb

def execute(dbquery):
    try:
        db = dbconnection()
        cur = db.cursor()
        cur.execute(dbquery)
    except Exception,e:
        raise e
    finally:
        cur.close()
        db.commit()
        db.close()
    return 'Successfully Inserted Data'

def dbconnection():
    try:
        return MySQLdb.connect(host = '127.0.0.1' , user = 'root',passwd = '1234', db = 'linkedin_data')
    except Exception, e:
        return 'Error Unable to connect to MySQL Server'
#####################################################main#############################################################
def main():


  br = mechanize.Browser()
  br.set_handle_robots(False)
  br.set_handle_refresh(False)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
  response = br.open('https://www.linkedin.com/uas/login?goback=.nmp_*1_*1_*1_*1_*1_*1_*1_*1_*1_*1&trk=hb_signin')
  response1 = br.response()
  br.select_form("login")
  control = br.form.find_control("session_key")  # session_password is name of input element in html
  control = br.form.find_control("session_password") # session_password is name of input element in html
  br["session_key"] = 'provide_username_here'  # Assigned  username to input type 
  br["session_password"] = 'provide_your_password'
  response = br.submit() # submit the form 
  dataresp =  response.read()
  print "............................................Login successfull ! .................................................."
  



if __name__ == "__main__":
    main()


