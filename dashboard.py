
from bottle import route, run, template
from nifi_poll import get_flow_status,get_system_diagnostics,get_processor_stats,get_pg_details
import socket


HOST = socket.getfqdn()

pgstats = {}
pgstats = get_pg_details()
name = {}
flow_files_queued = {}

for key,value in pgstats.iteritems():

  name[key] = value['name']
  flow_files_queued[key] = value['flow_files_queued']

@route('/page1')
def serve_homepage():
    return template('disp_table',pgnames = name, flowfilesqueued = flow_files_queued, cases = len(name))

run(host=HOST, port=8080, debug=True)
