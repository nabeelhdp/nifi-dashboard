import json
from bottle import route, run, template, static_file, request
from nifipoll import get_flow_status,get_system_diagnostics,get_processor_stats,get_pg_details
import socket

def get_nifi_stats(pg="root"):

  nifi_pg_stats = {}
  nifi_pg_stats = get_pg_details(pg)
  nifi_system_stats = {}
  nifi_system_stats = get_system_diagnostics()

  return nifi_pg_stats,nifi_system_stats

def read_nifi_pg_stats(pg_stats):

  name = {}
  flowFilesQueued = {}
  bytesQueued = {}
  total_flowFilesQueued = 0
  total_bytesQueued = 0
  activeThreadCount = {}
  total_activeThreadCount = 426

  for key,value in pg_stats.iteritems():

    name[key] = value['name']
    flowFilesQueued[key] = int(value['flowFilesQueued'])
    total_flowFilesQueued += int(value['flowFilesQueued'])
    bytesQueued[key] = int(value['bytesQueued'])
    total_bytesQueued += int(value['bytesQueued'])
    activeThreadCount[key] = int(value['activeThreadCount'])

  return name,flowFilesQueued,total_flowFilesQueued,bytesQueued,total_bytesQueued,activeThreadCount,total_activeThreadCount

def read_nifi_system_stats(stats):
  system_stat = {}
  system_stat['usedHeap'] = stats['usedHeapBytes']
  system_stat['freeHeap'] = stats['freeHeapBytes']
  system_stat['totalHeap'] = stats['totalHeapBytes']
  system_stat['freeNonHeap']  = stats['freeNonHeapBytes']
  system_stat['usedNonHeap'] = stats['usedNonHeapBytes']
  system_stat['totalNonHeap'] = stats['totalNonHeapBytes']
  system_stat['loadAverage'] = stats['processorLoadAverage']
  system_stat['flowfileRepofree'] = stats['flowFileRepositoryStorageUsage']['freeSpaceBytes']
  system_stat['flowfileRepoUsed'] = stats['flowFileRepositoryStorageUsage']['usedSpaceBytes']
  system_stat['flowfileRepoTotal'] = stats['flowFileRepositoryStorageUsage']['totalSpaceBytes']

  return system_stat

@route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')

@route('/dashboard', method=['POST','GET'])
def serve_pie():
    nifi_pg_stats = {}
    nifi_system_stats = {}

    if (request.forms.get('pgid')) :
      nifi_pg_stats, nifi_system_stats = get_nifi_stats(request.forms.get('pgid'))
    else :
      nifi_pg_stats, nifi_system_stats = get_nifi_stats()

    name,flowFilesQueued,total_flowFilesQueued,bytesQueued,total_bytesQueued,activeThreadCount,total_activeThreadCount = read_nifi_pg_stats(nifi_pg_stats)
    system_stats = read_nifi_system_stats(nifi_system_stats)

    return template(
             'dashboard', system_stats = json.dumps(system_stats), pgnames = json.dumps(name) ,
             activeThreads = json.dumps(activeThreadCount), total_threads = int(total_activeThreadCount),
             flowfilesQueued = json.dumps(flowFilesQueued), total_flowqueue = int(total_flowFilesQueued),
             bytesQueued = json.dumps(bytesQueued), total_bytes = int(total_bytesQueued) )

run(host=socket.getfqdn(), port=8080, debug=True)
