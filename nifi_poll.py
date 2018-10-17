
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

def get_config_params():
  # If config file explicitly passed, use it. Else fall back to config.ini as default filename
  config_file = sys.argv[1] if len(sys.argv) >= 2 else os.path.join(os.path.dirname(__file__),"config.ini")
  config_dict = {}
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

def get_auth_request():
  config_dict = get_config_params()
  data = {}
  data['username'] = config_dict['user']
  data['password'] = getpass.getpass()
  url_values = urllib.urlencode(data)
  token_url = "https://%s:%d/nifi-api/access/token" % (config_dict['host'], config_dict['port'])
  headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
  req = urllib2.Request(token_url,url_values,headers=headers)
  return req

def get_auth_token():

  httpHandler = urllib2.HTTPSHandler(context=set_ssl())
  # Set debug levels if needed
  #httpHandler.set_http_debuglevel(1)
  opener = urllib2.build_opener(httpHandler)
  req = get_auth_request()
  try:
    resp = opener.open(req)
    tdata = resp.read()
    token = 'Bearer ' + tdata
    return token
  except (urllib2.URLError, urllib2.HTTPError) as err:
    return 'NiFi authentication failed with error: %s' % err

def get_stats(headers,url,ctx):
  req = urllib2.Request(url,headers=headers)
  resp = urllib2.urlopen(req,context=ctx)
  stats = json.loads(resp.read())
  return stats

def set_ssl():
  # BAD CODE : Ignores SSL - equivalent to cancelling cert prompt.
  context = ssl.create_default_context()
  context.check_hostname = False
  context.verify_mode = ssl.CERT_NONE
  return context


def get_flow_status():
  token = get_auth_token()
  config_dict = get_config_params()
  if token.startswith('Bearer'):
    headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Authorization': token }
    flow_status_url = 'https://%s:%d/nifi-api/flow/status' % (config_dict['host'], config_dict['port'])
    flow_status = get_stats(headers, flow_status_url, set_ssl())
    #print json.dumps(flow_status,indent =2)
    return flow_status['controllerStatus']['flowFilesQueued']
  else:
    return token

def get_system_diagnostics():
  token = get_auth_token()
  config_dict = get_config_params()
  if token.startswith('Bearer'):
    headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Authorization': token }
    diagnostic_url = 'https://%s:%d/nifi-api/system-diagnostics' % (config_dict['host'], config_dict['port'])
    system_diagnostics = get_stats(headers, diagnostic_url, set_ssl())
    #print json.dumps(diagnostics,indent =2)
    return system_diagnostics
  else:
    return token


def get_processor_stats():
  token = get_auth_token()
  config_dict = get_config_params()
  if token.startswith('Bearer'):
    headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Authorization': token }
    processor_url = 'https://%s:%d/nifi-api/processors/%s' % (config_dict['host'], config_dict['port'] ,config_dict['processor_id'])
    processor_stats = get_stats(headers,processor_url,set_ssl())
    #print "Processor ID: ", processor_stats['component']['id']
    #print "State", processor_stats['component']['state']
    #print "Stats : ",json.dumps(processor_stats['status']['aggregateSnapshot'],indent =2 )
    return processor_stats
  else:
    return token

def get_pg_details():

  token = get_auth_token()
  config_dict = get_config_params()
  if token.startswith('Bearer'):
    headers = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8','Authorization': token }
    list_url = 'https://%s:%d/nifi-api/process-groups/root/process-groups' % (config_dict['host'], config_dict['port'])
    list_pgs = get_stats(headers, list_url, set_ssl())
    pgstats = {}
    for p in list_pgs['processGroups'] :
      pgstats[p['id']] = {}
      pgstats[p['id']]['name'] = p['status']['aggregateSnapshot']['name']
      pgstats[p['id']]['flow_files_queued'] = p['status']['aggregateSnapshot']['flowFilesQueued']
      # print p['id'] + " " + str(p['status']['aggregateSnapshot']['name']) +  " " + str(p['status']['aggregateSnapshot']['flowFilesQueued'])
      # if(p['status']['aggregateSnapshot']['flowFilesQueued'] > 0):
      #  print "{y:%.2f %s %s %s" % (float(p['status']['aggregateSnapshot']['flowFilesQueued'])*100.0/(flow_status['controllerStatus']['flowFilesQueued'] * 1.0) , ", label:\"" , str(p['status']['aggregateSnapshot']['id']),"\"},")

    return pgstats
  else:
    return token

def main():
  print json.dumps(get_system_diagnostics(),indent=2)

if __name__ == "__main__":
  main()
