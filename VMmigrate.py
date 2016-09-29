import os
import time
import novaclient.client as novaClient
import ceilometerclient.client as ceilClient

os.environ["OS_AUTH_URL"] = "http://controller:5000/v2.0"
os.environ["OS_TENANT_ID"] = "79d68664d0244f9a34c202498f1e839"
os.environ["OS_TENANT_NAME"] = "admin"
os.environ["OS_USERNAME"] = "admin"
os.environ["OS_PASSWORD"] = "123456"

HOST_DIRS = {'192.168.0.116': 'compute1',
             '192.168.0.122': 'compute2'}
THRESHOLD = 20
METER_CPU = 'hardware.system_stats.cpu.idle'
METER_MEMORY_TOTAL = 'hardware.memory.total'
METER_MEMORY_USED = 'hardware.memory.used'


def get_nova_credentials_v2():
    d = {}
    d['version'] = '2'
    d['username'] = os.environ['OS_USERNAME']
    d['api_key'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_id'] = os.environ['OS_TENANT_NAME']
    return d


def get_ceil_credentials_v2():
    d = {}
    d['os_username'] = os.environ['OS_USERNAME']
    d['os_password'] = os.environ['OS_PASSWORD']
    d['os_auth_url'] = os.environ['OS_AUTH_URL']
    d['os_tenant_name'] = os.environ['OS_TENANT_NAME']
    return d


def get_migrate_dest(sample_list, instance_memory):
    resource_id_list = []
    load_list = []
    host_migrate = ''
    resource_id = ''
    for sam in sample_list:
        if sam.counter_volume < THRESHOLD:
            continue
        resource_id_list.append(sam.resource_id)
        load_list.append(sam.counter_volume)
    if not load_list:
        return None
    print(resource_id_list)
    print(load_list)
    while True:
        if not load_list:
            resource_id = ''
            break
        index = load_list.index(max(load_list))
        resource_id = resource_id_list[index]
        query = [{'field': 'resource_id', 'op': 'eq', 'value': resource_id}]
        memory_total = ceilometer_client.samples.list(
            meter_name=METER_MEMORY_TOTAL, q=query, limit=1)[0].counter_volume
        memory_used = ceilometer_client.samples.list(
            meter_name=METER_MEMORY_USED, q=query, limit=1)[0].counter_volume
        print("memory_total:" + memory_total + " memory_used:" + memory_used)
        memory_unused = (memory_total - memory_used) / 1024
        print(memory_unused)
        if memory_unused > instance_memory:
            break
        else:
            load_list.pop(index)
            resource_id_list.pop(index)
    if not resource_id:
        return None
    host_migrate = HOST_DIRS[resource_id]
    print('dest:' + host_migrate)
    return host_migrate


def get_computeNode_num():
    numOfHost = 0
    host_list = nova_client.hosts.list()
    for h in host_list:
        if h.service == 'compute':
            numOfHost = numOfHost + 1
    print(numOfHost)
    return numOfHost


def MaxMinNormalization(cpu_util_list, Min, Max):
    k = []
    for x in cpu_util_list:
        x = (x - Min) / (Max - Min)
        k.append(x)
    return k


def allcountofinstance():
    allserver_list = nova_client.servers.list(search_opts={'all_tenants': '1'})
    serverallcount = 0
    for k in allserver_list:
        serverallcount = serverallcount + 1
    return serverallcount


def search_memory(rid):
    query = [{'field': 'resource_id', 'op': 'eq', 'value': rid}]
    sample_memory_list = ceilometer_client.samples.list(
        meter_name='memory', q=query, limit=1)
    return sample_memory_list[0].counter_volume


def choose_instance(compute):
    server_all_count = allcountofinstance()
    sample_list = ceilometer_client.samples.list(
        meter_name='cpu_util', limit='%s' % server_all_count)
    server_list = nova_client.servers.list(
        search_opts={'host': compute, 'all_tenants': '1'})

    cpu_util_list = []
    resource_id_list = []
    # print sample_list[0]
    for f in sample_list:
        for s in server_list:
            if f.resource_id == s.id:
                print(f.resource_id + " " + str(f.counter_volume))
                cpu_util_list.append(str(f.counter_volume))
                resource_id_list.append(f.resource_id)
    print(cpu_util_list)
    cpu_util_list = map(float, cpu_util_list)
    minimum = min(cpu_util_list)
    maxmum = max(cpu_util_list)
    if minimum > 0 or maxmum > 0:
        if len(cpu_util_list) > 1:
            after_normalize_list = MaxMinNormalization(
                cpu_util_list, minimum, maxmum)
            indextomax = [i for i, x in enumerate(
                after_normalize_list) if x == max(after_normalize_list)]
            itm = int(indextomax[0])
            return resource_id_list[itm]
        elif len(cpu_util_list) == 1:
            itm = 0
            return resource_id_list[itm]
        else:
            return None
    else:
        return None


def ceilometer_migrate():

    numOfHost = get_computeNode_num() - 1

    sample_list_load = ceilometer_client.samples.list(
        meter_name=METER_CPU, limit=numOfHost)

    isOverLoad = False
    host_overhost = ''
    host_migrate = ''
    for sam in sample_list_load:
        if sam.counter_volume < THRESHOLD:
            host_overhost = sam.resource_id
            isOverLoad = True
            host_overhost = HOST_DIRS[host_overhost]
            print('source:' + host_overhost)
            break
    if isOverLoad:
        instanceID = choose_instance(host_overhost)
        instance_memory = search_memory(instanceID)
        if instanceID:
            host_migrate = get_migrate_dest(sample_list_load, instance_memory)
            if host_migrate:
                try:
                    server = nova_client.servers.get(server=instanceID)
                    server.live_migrate(host=host_migrate)
                except Exception as e:
                    print(e)
                print("migrate")
            else:
                print("all compute node over load")
        else:
            print("no instance")
    else:
        print("System not over load")


nova_creds = get_nova_credentials_v2()
nova_client = novaClient.Client(**nova_creds)

ceil_creds = get_ceil_credentials_v2()
ceilometer_client = ceilClient.get_client('2', **ceil_creds)

#while True:
ceilometer_migrate()
    #time.sleep(600)