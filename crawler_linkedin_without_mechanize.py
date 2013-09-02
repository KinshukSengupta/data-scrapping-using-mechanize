import MySQLdb
import urllib, json
from math import ceil
import urllib
import StringIO
from datetime import datetime
import re
from bs4 import BeautifulSoup

###########################
# Fuction to execute mysql/sql queries for better db performance #

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

###########################
#  Generic Function to create database connectivity with mysql remote server #

def dbconnection():
    try:
        return MySQLdb.connect(host = '127.0.0.1' , user = 'root',passwd = '123456', db = 'linkedin_crawler')
    except Exception, e:
        return 'Error Unable to connect to MySQL Server'

###########################
# Main Function Call #

def main_method():
    '''
        Final main method is called for result processing.
    '''
    import logging
    logging.basicConfig(filename='/var/log/linkedin.log',level=logging.INFO)

    db = dbconnection()
    cur = db.cursor()

    #url  = 'http://uk.linkedin.com/pub/lucy-crawford/8/35/780'
    #url  = 'http://uk.linkedin.com/pub/christophe-le-caillec/11/414/379?trk=pub-pbmap'
    url = 'http://www.linkedin.com/in/olivierlefevre'
    data = urllib.urlopen(url)
    dataresp = data.read()
    #....Using beautiful soup class to parse HTML
    ulist = []    
    parsed_html = BeautifulSoup(dataresp) 
    name = parsed_html.body.find('span', attrs={'class':'full-name'})
    name = str(name)
    name = name.replace('</span> <span class="family-name">',' ').split('>')[2].replace('</span','')

    headline = parsed_html.body.find('p', attrs={'class':'title'})
    headline = str(headline)
    headline = headline.split("\n")[3].replace(" ","")
    industry = parsed_html.body.find('dd', attrs={'class':'industry'})

    industry = str(industry)
    industry = industry.split("\n")[2].replace(" ","")

    current_company = parsed_html.body.find('span', attrs={'class':'org summary'})
    current_company = str(current_company)
    current_company = current_company.split(">")[1].replace("</span"," ")

    designation = parsed_html.body.find('span', attrs={'class':'title'})

    designation = str(designation)
    designation = designation.split(">")[1].replace("</span"," ")

    locality = parsed_html.body.find('span', attrs={'class':'locality'})
    locality = str(locality)
    locality = locality.split("\n")[4].replace(" ","")

    dbquery = "insert into fin_heads(name,headline,locality,industry,present_company,designation) values('%s','%s','%s','%s','%s','%s')"%(name,headline,locality,industry,current_company,designation)
    execute(dbquery)
    print 'Found 1st profile and inserted data with name %s'%(name)
  

    #........Above logic is to find first profile and parse data out of it and below loop is for traversing all the profiles.

    titlelist = ['chieffinancialofficer','cfp','evp','executive vice president','chief executive officer','Chief Executive Officer','CFO','EVP Finance','EVP-Finance','Executive Vice President Finance','vice president (finance)','vice president - finance']
    for a in parsed_html.findAll('a',href=True):	        
	    if re.findall('linkedin.com/pub', a['href']):
	        ulist.append(a['href']) #...Got list of public profile url
    
    logging.info('....................................logger started............................................')
    logging.info(datetime.now())
    #....Get unique list from ulist and then convert it into list after operation.
    ulist = set(ulist)
    ulist = list(ulist)   
    print '.........................1nd ulist.......................'
    print ulist
    for i in xrange(10000):
	ulist =  set(ulist)
        ulist = list(ulist)
	print '......New List created for iteration...........'
	print ulist
 	logging.info(str(ulist))

        for j in xrange(len(ulist)):
                try:  
            	    data = urllib.urlopen(ulist[j])
    		    print ulist[j]
		
    		    dataresp = data.read()
    		    parsed_html = BeautifulSoup(dataresp)
		    for b in parsed_html.findAll('a',href=True):
                        if re.findall('linkedin.com/pub', b['href']):
                            ulist.append(b['href'])
		    #ulist = set(ulist) 
		    #ulist = list(ulist)
		    #logging.info(str(ulist))
    		    name = parsed_html.body.find('span', attrs={'class':'full-name'})
    		    name = str(name)
    		    name = name.replace('</span> <span class="family-name">',' ').split('>')[2].replace('</span','')
    		    headline = parsed_html.body.find('p', attrs={'class':'title'})
    		    headline = str(headline)
    		    headline = headline.split("\n")[3].replace(" ","")
    		    industry = parsed_html.body.find('dd', attrs={'class':'industry'})
    		    industry = str(industry)
    		    industry = industry.split("\n")[2].replace(" ","")
    		    current_company = parsed_html.body.find('span', attrs={'class':'org summary'})
    		    current_company = str(current_company)
    		    current_company = current_company.split(">")[1].replace("</span"," ")
    		    designation = parsed_html.body.find('span', attrs={'class':'title'})
    		    designation = str(designation)
    		    designation = designation.split(">")[1].replace("</span"," ")
    		    locality = parsed_html.body.find('span', attrs={'class':'locality'})
    		    locality = str(locality)
    		    locality = locality.split('\t')[1].split('\n')[0].replace(' ','')
    		    parsed_data = name+" | "+headline+" | "+industry+" | "+current_company+" | "+designation+" | "+locality
	 	    print parsed_data
		    logging.info(str(parsed_data))
    		    logging.info(str(ulist[j]))    
		    #if designation =='chieffinancialofficer' or designation == 'cfo' or designation == 'evp' or designation == 'executivevicepresident' or designation == 'chiefexecutiveofficer' or designation == 'ChiefExecutiveOfficer' or designation == 'CFO' or designation == 'EVPFinance' or designation == 'EVP-Finance' or designation == 'ExecutiveVicePresidentFinance'or designation == 'vicepresident(finance)' or designation == 'vicepresident-finance' or designation == 'vp-finance' or designation =='seniorvicepresident' or designation =='groupchieffinancialofficer' or designation =='svp&chieffinancialofficer' or designation=='vicepresident,chieffinancialofficer' or designation=='vp, finance' or designation=='chief financial officer, open' or designation=='senior vice president':  
   		    designation =  designation.lower()
		    designation = designation.replace(' ','')

		    headline = headline.lower()
		    headline = headline.replace(' ','')
    		    if designation.find('finance')>=0 or designation.find('financial')>=0 or headline.find('finance')>=0 or headline.find('bank')>=0 or headline.find('fin')>=0 or designation.find('cfo')>=0 or headline.find('cfo')>=0:
		        dbquery = "insert into fin_heads(name,headline,locality,industry,present_company,designation,profileurl) values('%s','%s','%s','%s','%s','%s','%s')"%(name,headline,locality,industry,current_company,designation,ulist[j])
			execute(dbquery)
			print dbquery
                        print 'Success !!!!!'
			logging.info('Sucess !!!!')
                           
    	 	    else:
		        print 'Failed Profile MisMatch...... '
		        logging.info('Failed Profile MisMatch.....')
       
                except Exception ,e:
	            pass
 
if __name__ == "__main__":
    main_method()
