# Need to be executed from salt master with root privileges

import json
import sys

import salt.client as client
from netaddr import IPNetwork, IPAddress

# ==========CONFIGURATION PART==========#
# Define network types and their CIDRs to be tested
nets = {
    "management": "192.168.2.0/23",
    "storage": "192.168.4.0/23",
    "storage_replication": "192.168.6.0/23",
    "deploy": "10.110.25.0/24"
}

# Define CIDR for pxe/default/ssh network
pxe_net = '10.110.25.0/24'

# Define nodes to be tested (all pairs will be calculated)
# you can specify node types like this
# target_nodes=['ctl*','des*','asc*']
# you can choose some particular nodes (pay attention to format)
target_nodes = ['.*']

# target_nodes=['cpu-003.*','cpu-004.*']
# you can even skip nodes from the list (not implemented yet)
skipped_nodes = ['osd005.inspurcloud.com']
# you can define regex by your own (perl-type regex, -E option in salt)
nodes_regex = ''
# tbd maybe define networks for each node
# groups = {'ctl*': ['public'],'asc*': ['public','private']}

# ==========CONFIGURATION PART==========#

roles_map = {
    "apt": "repository",
    "bmk": "validation",
    "cfg": "master",
    "cid": "cicd",
    "cmn": "storage_monitor",
    "cmp": "compute",
    "ctl": "openstack_controller",
    "dbs": "database",
    "gtw": "openstack_gateway",
    "kvm": "foundation",
    "log": "stacklight_logger",
    "mon": "monitoring",
    "msg": "messaging",
    "mtr": "stacklight_metering",
    "osd": "storage_node",
    "prx": "proxy",
    "rgw": "storage_rados"
}

if not nodes_regex:
    nodes_regex += '('
    for node in target_nodes:
        nodes_regex += node + '|'
    nodes_regex = nodes_regex[:-1]
    nodes_regex += ')'

master_client = client.LocalClient()
nodes = master_client.cmd(
    expr_form='pcre',
    tgt=nodes_regex,
    fun='network.interfaces'
)

# TODO implement skip nodes and check if we have dead ones
# import pdb;pdb.set_trace()
# active_nodes = [
#    node_name for node_name in nodes
#    if nodes[node_name] and
#       node_name not in skipped_nodes and
#       "[Not connected]" not in nodes[node_name]
# ]

result = []
counter = 1
for node in nodes:
    the_node = {}
    print node
    the_node["network_data"] = []
    for net in nets:
        for interf in nodes[node]:
            # maybe need to handle vips here
            # non_vip = nodes[pair[0]][interf]['inet'][0]['broadcast']
            if nodes[node][interf].get('inet') is None:
                continue
            ip = nodes[node][interf]['inet'][0]['address']
            if IPAddress(ip) in IPNetwork(nets[net]):
                the_network = {'name': net,
                               'ip': ip + '/' + nets[net].split('/')[1]}
                the_node["network_data"].append(the_network)
            if IPAddress(ip) in IPNetwork(pxe_net):
                the_node["ip"] = ip
    the_node["name"] = node

    if node[0:3] in roles_map:
        the_node["roles"] = roles_map[node[0:3]]
    else:
        the_node["roles"] = "not_available"

    the_node["id"] = counter
    counter += 1
    result.append(the_node)

# Generating
if len(result):
    print("Generated dict:{}".format(result))
    json_filename = "_nodes.json"
    with open(json_filename, 'w') as fp:
        json.dump(result, fp, sort_keys=True, indent=4)
    print("Saved to {}".format(json_filename))
