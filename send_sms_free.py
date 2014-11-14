#!/usr/bin/env python2

#
# imports
import httplib, urllib, os, sys
from optparse import OptionParser

#
# variables
host = "smsapi.free-mobile.fr"
user = "0000000"
password = "XXXXXXXXX"

#
# functions

def argCommandline():
        """ command line arguments """
        dicArg = {}
        parser = OptionParser()
        parser.add_option("-m", "--message", dest="message", default=False, help=u"message a envoyer par SMS")
        parser.add_option("-f", "--file", dest="file", help=u"fichier a envoyer par SMS")
        parser.add_option("-c", "--command", dest="command", help=u"commande a envoyer par SMS")
        parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="mode verbeux")
        (options, args) = parser.parse_args()
        # traitements des arguments
        # message
        if options.message:
                dicArg['message'] = options.message.replace('\n', ' - ')
        # fichier
        if options.file:
                if os.path.isfile(options.file):
                        with open(options.file) as f:
                                dicArg['message'] = f.read().replace('\n', ' - ')
                        dicArg['file'] = options.file
                else:
                        print "file %s does not exist" % (options.file)
                        sys.exit()
        # commande
        if options.command:
                dicArg['command'] = options.command
                dicArg['message'] = os.popen(options.command).read().replace('\n', ' - ')
        if not options.message and not options.file and not options.command:
                parser.error("/!\ l'option -m ou -f est obligatoire")
                sys.exit()
        # mode verbeux
        if options.verbose:
                dicArg['verbose'] = True
        else:
                dicArg['verbose'] = False

        # on renvoie le dico
        return dicArg

def debug(msg):
        """print debug"""
        if dicArg['verbose']:
                print(msg)

def sendSMS(host, user, password, msg):
        '''Send SMS to phone'''
        params = urllib.urlencode({"user": user, "pass": password, "msg": msg})
        conn = httplib.HTTPSConnection(host)
        conn.request("GET", "/sendmsg?" + params)
        r1 = conn.getresponse()
        data1 = r1.read()
        status1 = r1.status
        debug(data1 + str(status1))
        conn.close()
        if status1 > 200:
                print "Error code : %s\n\t%s" % (str(status1), data1)

#
# main prgm

dicArg = argCommandline()
debug(dicArg)

sendSMS(host, user, password, dicArg['message'])
