#!/usr/bin/python

import urllib2
import getpass
import optparse
import json
import string
import sys
import os
import urllib
import ssl
import ConfigParser
from ConfigParser import SafeConfigParser

def get_config_params(config_file):
  try:
    with open(config_file) as f:
      try:
        parser = SafeConfigParser()
        parser.readfp(f)
      except ConfigParser.Error, err:
        print 'Could not parse: %s Exiting', err
        sys.exit(1)
  except IOError as e:
    print "Unable to access %s. Error %s \nExiting" % (config_file, e)
    sys.exit(1)

  # Prepare dictionary object with config variables populated
  config_dict = {}
  config_dict['host'] = parser.get('nifi_config','host')
  config_dict['port'] = int(parser.get('nifi_config','port'))
  config_dict["user"] = parser.get('nifi_config','user')
  config_dict["processor_id"] = parser.get('nifi_config', 'processor_id')

  return config_dict

def get_token():
  pass

def get_system_diagnostics():
  pass

def get_processor_stats():
  pass

def main():

  # If config file explicitly passed, use it. Else fall back to config.ini as default filename
  config_file = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(os.path.dirname(__file__),"config.ini")
  config_dict = {}
  config_dict = get_config_params(config_file)

  # Ignore SSL - equivalent to cancelling
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE

  data = {}
  data['username'] = config_dict['user']
  data['password'] = getpass.getpass()
  url_values = urllib.urlencode(data)
  token_url = "https://%s:%d/nifi-api/access/token" % (config_dict['host'], config_dict['port'])
  headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

  req = urllib2.Request(token_url,url_values,headers=headers)
  # Debug friendly approach
  httpHandler = urllib2.HTTPSHandler(context=ctx)
  #httpHandler.set_http_debuglevel(1)
  opener = urllib2.build_opener(httpHandler)

  try:
    resp = opener.open(req)
    tdata = resp.read()
    token = 'Bearer ' + tdata

    headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Authorization': token }
    diagnostic_url = 'https://%s:%d/nifi-api/system-diagnostics' % (config_dict['host'], config_dict['port'])
    req = urllib2.Request(diagnostic_url,headers=headers)
    diag = urllib2.urlopen(req,context=ctx)
    diagnostics = json.loads(diag.read())
    print json.dumps(diagnostics,indent =2)

    processor_url = 'https://%s:%d/nifi-api/processors/%s' % (config_dict['host'], config_dict['port'] ,config_dict['processor_id'])
    req = urllib2.Request(processor_url,headers=headers)
    processor_req = urllib2.urlopen(req,context=ctx)
    processor_stats = json.loads(processor_req.read())
    print "Processor ID: ", processor_stats['component']['id']
    print "State", processor_stats['component']['state']
    print "Stats : ",json.dumps(processor_stats['status']['aggregateSnapshot'],indent =2 )

  except (urllib2.URLError, urllib2.HTTPError) as err:
    print 'NiFi authentication failed with error:', err

if __name__ == "__main__":
  main()
