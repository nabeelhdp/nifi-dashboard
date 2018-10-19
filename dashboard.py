import json
from bottle import route, run, template, static_file
from nifipoll import get_flow_status,get_system_diagnostics,get_processor_stats,get_pg_details
import socket


HOST = socket.getfqdn()

pgstats = {}
pgstats = get_pg_details()
name = {}
flowFilesQueued = {}
bytesQueued = {}
total_flowFilesQueued = 0

for key,value in pgstats.iteritems():

  name[key] = value['name']
  flowFilesQueued[key] = value['flowFilesQueued']
  total_flowFilesQueued += value['flowFilesQueued']
  bytesQueued[key] = value['bytesQueued']

print total_flowFilesQueued

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/table')
def serve_homepage():
    return template('disp_table',pgnames = name, dataparam = bytesQueued, cases = len(name))

@route('/pie')
def serve_pie():
    return template('pie', dataparam = json.dumps(flowFilesQueued), total = total_flowFilesQueued )

run(host=HOST, port=8080, debug=True)
