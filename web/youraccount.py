## $Id$
## CDSware User account information.

## This file is part of the CERN Document Server Software (CDSware).
## Copyright (C) 2002 CERN.
##
## The CDSware is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## The CDSware is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.  
##
## You should have received a copy of the GNU General Public License
## along with CDSware; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

## read config variables:
#include "config.wml"
#include "configbis.wml"

<protect>## $Id$ </protect>
<protect>## DO NOT EDIT THIS FILE!  IT WAS AUTOMATICALLY GENERATED FROM CDSware WML SOURCES.</protect>
"""CDSware ACCOUNT HANDLING"""

__lastupdated__ = """<: print `date +"%d %b %Y %H:%M:%S %Z"`; :>"""

## fill config variables:
pylibdir = "<LIBDIR>/python"

import sys
sys.path.append('%s' % pylibdir)
from cdsware import webuser
from cdsware.config import weburl,cdsname,cdslang,supportemail
from cdsware.webpage import page
from cdsware import webaccount
from cdsware import webbasket
from cdsware import webalert
from cdsware import webuser
from cdsware.access_control_config import *
from mod_python import apache    
import smtplib

def set(req, ln=cdslang):
    uid = webuser.getUid(req)

    if uid == -1:
        return webuser.page_not_authorized(req, "../youraccount.py/set")

    data = webuser.getDataUid(req,uid)
    email = data[0]
    passw = data[1]
    return page(title="Your Settings",
                body=webaccount.perform_set(email,passw),
                navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln),
                description="CDS Personalize, Your Settings",
                keywords="CDS, personalize",
                uid=uid,
                language=ln,
                lastupdated=__lastupdated__)

def change(req,email=None,password=None,ln=cdslang):
    uid = webuser.getUid(req)

    if uid == -1:
        return webuser.page_not_authorized(req, "../youraccount.py/change")

    if webuser.checkemail(email):
        
        change = webuser.updateDataUser(req,uid,email,password)
        return display(req, ln)
    else :
        return display(req, ln)

def lost(req, ln=cdslang):
    uid = webuser.getUid(req)

    if uid == -1:
        return webuser.page_not_authorized(req, "../youraccount.py/lost")

    return page(title="Login",
                body=webaccount.perform_lost(),
                navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln),
                description="CDS Personalize, Main page",
                keywords="CDS, personalize",
                uid=uid,
                language=ln,
                lastupdated=__lastupdated__)

def display(req, ln=cdslang):
    uid =  webuser.getUid(req)

    if uid == -1:
        return webuser.page_not_authorized(req, "../youraccount.py/display")

    if webuser.isGuestUser(uid):
		
	return page(title="Your Account",
                    body=webaccount.perform_info(req),
	            description="CDS Personalize, Main page",
	            keywords="CDS, personalize",
	            uid=uid,
                    language=ln,
                    lastupdated=__lastupdated__)

    data = webuser.getDataUid(req,uid)	
    bask = webbasket.account_list_baskets(uid)	  	  
    aler = webalert.account_list_alerts(uid)
    sear = webalert.account_list_searches(uid)	    	
    return page(title="Your Account",
                body=webaccount.perform_display_account(req,data,bask,aler,sear),
                description="CDS Personalize, Main page",
                keywords="CDS, personalize",
                uid=uid,
                language=ln,
                lastupdated=__lastupdated__)
    	
	
def send_email(req, p_email=None, ln=cdslang):
    
    uid = webuser.getUid(req)

    if uid == -1:
        return webuser.page_not_authorized(req, "../youraccount.py/send_email")

    passw = webuser.givePassword(p_email) 
    if passw == -999:
	eMsg = "The entered e-mail address doesn't exist in the database"
	return page(title="Your Account",
                    body=webaccount.perform_emailMessage(eMsg),
                    description="CDS Personalize, Main page",
                    keywords="CDS, personalize",
                    uid=uid,
                    language=ln,
                    lastupdated=__lastupdated__)
	
    fromaddr = "From: %s" % supportemail
    toaddrs  = "To: " + p_email
    to = toaddrs + "\n"
    sub = "Subject: Credentials for %s\n\n" % cdsname
    body = "Here are your user credentials for %s:\n\n" % cdsname
    body += "   username: %s\n   password: %s\n\n" % (p_email, passw)
    body += "You can login at %s/youraccount.py/login" % weburl
    msg = to + sub + body	

    server = smtplib.SMTP('localhost')
    server.set_debuglevel(1)
    
    try: 
	server.sendmail(fromaddr, toaddrs, msg)

    except smtplib.SMTPRecipientsRefused,e:
           eMsg = "The entered e-mail address is incorrect, please check that it is written correctly (e.g. johndoe@example.com)"
	   return page(title="Your Account",
                       body=webaccount.perform_emailMessage(eMsg),
                       description="CDS Personalize, Main page",
                       keywords="CDS, personalize",
                       uid=uid,
                       language=ln,
                       lastupdated=__lastupdated__)

    server.quit()
    return page(title="Your Account",
                body=webaccount.perform_emailSent(p_email),
                description="CDS Personalize, Main page",
                keywords="CDS, personalize",
                uid=uid,
                language=ln,
                lastupdated=__lastupdated__)

def youradminactivities(req, ln=cdslang):
    uid = webuser.getUid(req)	

    if uid == -1:
        return webuser.page_not_authorized(req, "../youraccount.py/youradminactivities")

    return page(title="Your Administrative Activities",
                body=webaccount.perform_youradminactivities(uid),
                navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln),
                description="CDS Personalize, Main page",
                keywords="CDS, personalize",
                uid=uid,
                language=ln,
                lastupdated=__lastupdated__)

def delete(req, ln=cdslang):
    uid = webuser.getUid(req)

    if uid == -1:
        return webuser.page_not_authorized(req, "../youraccount.py/delete")
	
    return page(title="Delete Account",
                body=webaccount.perform_delete(),
                navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln),
                description="CDS Personalize, Main page",
                keywords="CDS, personalize",
                uid=uid,
                language=ln,
                lastupdated=__lastupdated__)

def logout(req, ln=cdslang):
    
    uid = webuser.logoutUser(req)

    if uid == -1:
        return webuser.page_not_authorized(req, "../youraccount.py/logout")

    return page(title="Logout",
                body=webaccount.perform_logout(req),
                navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln),
                description="CDS Personalize, Main page",
                keywords="CDS, personalize",
                uid=uid,
                language=ln,
                lastupdated=__lastupdated__)
    
def login(req, p_email=None, p_pw=None, action='login', referer='', ln=cdslang):

    uid = webuser.getUid(req)

    if action =='login':
       if p_email==None:
           return  page(title="Login",
                        body=webaccount.create_login_page_box(referer),
                        navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln),
                        description="CDS Personalize, Main page",
                        keywords="CDS, personalize",
                        uid=uid,
                        language=ln,
                        lastupdated=__lastupdated__)
       iden = webuser.loginUser(p_email,p_pw)
    
       if len(iden)>0:
           uid = webuser.update_Uid(req,p_email,p_pw)
           uid2 = webuser.getUid(req)
           if uid2 == -1:
               webuser.logoutUser(req)
               return webuser.page_not_authorized(req, "../youraccount.py/login?ln=%s" % ln, uid=uid)

           # login successful!
           if referer:
               req.err_headers_out.add("Location", referer)
               raise apache.SERVER_RETURN, apache.HTTP_MOVED_PERMANENTLY               
           else:
               return display(req)
       else:
      	   if webuser.userNotExist(p_email,p_pw) or p_email=='' or p_email==' ':
               mess ="Your are not logged into the system, because this user is unknown."
           else:
               mess ="Your are not logged into the system, because you have introduced a wrong password."
           act = "login"    
	   return page(title="Login",
                       body=webaccount.perform_back(mess,act),
                       navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln), 
                       description="CDS Personalize, Main page",
                       keywords="CDS, personalize",
                       uid=uid,
                       language=ln,
                       lastupdated=__lastupdated__)

def register(req, p_email=None, p_pw=None, action='login', referer='', ln=cdslang):
    uid = webuser.getUid(req)

    if p_email==None:
        return  page(title="Register",
                     body=webaccount.create_register_page_box(referer),
                     navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln),
                     description="CDS Personalize, Main page",
                     keywords="CDS, personalize",
                     uid=uid,
                     language=ln,
                     lastupdated=__lastupdated__)
    
    mess=""
    act=""
    ruid=webuser.registerUser(req,p_email,p_pw)
    if ruid==1:
        uid=webuser.update_Uid(req,p_email,p_pw)
        mess = "Your account has been successfully created."
        title = "Account created"
        if CFG_ACCESS_CONTROL_NOTIFY_USER_ABOUT_NEW_ACCOUNT == 1:
            mess += " An email has been sent to the given address with the account information."
        if CFG_ACCESS_CONTROL_LEVEL_ACCOUNTS >= 1:
            mess += " A second email will be sent when the account has been activated and can be used."
        else:
            mess += """ To continue to your account, press <a href="%s/youraccount.py/display?ln=%s">here</a>""" % (weburl, ln)
    elif  ruid ==-1 :
        mess ="The user already exists in the database, please try again"
	act = "register"
        title = "Register failure"
    else:
        mess ="Your are not registered into the system please try again"
       	act = "register"
        title = "Register failure"

    return page(title=title,
 	        body=webaccount.perform_back(mess,act),
                navtrail="""<a class="navtrail" href="%s/youraccount.py/display?ln=%s">Your Account</a>""" % (weburl, ln),
                description="CDS Personalize, Main page",
                keywords="CDS, personalize",
                uid=uid,
                language=ln,
                lastupdated=__lastupdated__)
