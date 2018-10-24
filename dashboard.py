
import json
from bottle import route, run, template, static_file, request
from nifipoll import get_flow_status,get_system_diagnostics,get_processor_stats,get_pg_details
import socket

def get_nifi_stats(pg="root"):

  nifi_response = {}
  nifi_response = get_pg_details(pg)
  return nifi_response

def read_nifi_stats(stats):
  name = {}
  flowFilesQueued = {}
  bytesQueued = {}
  total_flowFilesQueued = 0
  total_bytesQueued = 0
  activeThreadCount = {}
  total_activeThreadCount = 426

  for key,value in stats.iteritems():

      name[key] = value['name']
      print value['name']

      flowFilesQueued[key] = int(value['flowFilesQueued'])
      total_flowFilesQueued += int(value['flowFilesQueued'])

      bytesQueued[key] = int(value['bytesQueued'])
      total_bytesQueued += int(value['bytesQueued'])

      activeThreadCount[key] = int(value['activeThreadCount'])

  return name,flowFilesQueued,total_flowFilesQueued,bytesQueued,total_bytesQueued,activeThreadCount,total_activeThreadCount


@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/table')
def serve_homepage():
    return template('disp_table',pgnames = name, dataparam = bytesQueued, cases = len(name))

@route('/pie', method=['POST','GET'])
def serve_pie():
    nifi_response = {}
    if (request.forms.get('pgid')) :
      print('pgid = ' + request.forms.get('pgid'))
      nifi_response = get_nifi_stats(request.forms.get('pgid'))
    else :
      nifi_response = get_nifi_stats()
    name,flowFilesQueued,total_flowFilesQueued,bytesQueued,total_bytesQueued,activeThreadCount,total_activeThreadCount = read_nifi_stats(nifi_response)
    return template(
             'pie', pgnames = json.dumps(name) ,
             flowfilesQueued = json.dumps(flowFilesQueued), total = total_flowFilesQueued )

@route('/donut')
def serve_donut():
    nifi_response = {}
    nifi_response = get_nifi_stats()
    name,flowFilesQueued,total_flowFilesQueued,bytesQueued,total_bytesQueued,activeThreadCount,total_activeThreadCount = read_nifi_stats(nifi_response)
    return template('donut', pgnames = json.dumps(name) , flowfilesQueued = json.dumps(flowFilesQueued), total = total_flowFilesQueued )


run(host=socket.getfqdn(), port=8080, debug=True)
