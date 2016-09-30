# needs:fix_opt_description
# needs:check_deprecation_status
# needs:check_opt_group_and_type
# needs:fix_opt_description_indentation
# needs:fix_opt_registration_consistency


# Copyright 2016 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from oslo_config import cfg

from nova.conf import paths

NOVA_NET_API = 'nova.network.api.API'

network_opts = [
    cfg.StrOpt("flat_network_bridge",
            help="""
This option determines the bridge used for simple network interfaces when no
bridge is specified in the VM creation request.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Possible values:

    Any string representing a valid network bridge, such as 'br100'

Related options:

    ``use_neutron``
"""),
    cfg.StrOpt("flat_network_dns",
            default="8.8.4.4",
            help="""
This is the address of the DNS server for a simple network. If this option is
not specified, the default of '8.8.4.4' is used.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Possible values:

    Any valid IP address.

Related options:

    ``use_neutron``
"""),
    cfg.BoolOpt("flat_injected",
            default=False,
            help="""
This option determines whether the network setup information is injected into
the VM before it is booted.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Related options:

    ``use_neutron``
"""),
    cfg.StrOpt("flat_interface",
            help="""
This option is the name of the virtual interface of the VM on which the bridge
will be built.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Possible values:

    Any valid virtual interface name, such as 'eth0'

Related options:

    ``use_neutron``
"""),
    cfg.IntOpt("vlan_start",
            default=100,
            min=1,
            max=4094,
            help="""
This is the VLAN number used for private networks. Note that the when creating
the networks, if the specified number has already been assigned, nova-network
will increment this number until it finds an available VLAN.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment. It also will be ignored if the configuration option
for `network_manager` is not set to the default of
'nova.network.manager.VlanManager'.

Possible values:

    Any integer between 1 and 4094. Values outside of that range will raise a
    ValueError exception. Default = 100.

Related options:

    ``network_manager``, ``use_neutron``
"""),
    cfg.StrOpt("vlan_interface",
            help="""
This option is the name of the virtual interface of the VM on which the VLAN
bridge will be built.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment. It also will be ignored if the configuration option
for `network_manager` is not set to the default of
'nova.network.manager.VlanManager'.

Possible values:

    Any valid virtual interface name, such as 'eth0'

Related options:

    ``use_neutron``
"""),
    cfg.IntOpt("num_networks",
            default=1,
            help="""
This option represents the number of networks to create if not explicitly
specified when the network is created. The only time this is used is if a CIDR
is specified, but an explicit network_size is not. In that case, the subnets
are created by diving the IP address space of the CIDR by num_networks. The
resulting subnet sizes cannot be larger than the configuration option
`network_size`; in that event, they are reduced to `network_size`, and a
warning is logged.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Possible values:

    Any positive integer is technically valid, although there are practical
    limits based upon available IP address space and virtual interfaces. The
    default is 1.

Related options:

    ``use_neutron``, ``network_size``
"""),
    cfg.StrOpt("vpn_ip",
            default="$my_ip",
            help="""
This is the public IP address for the cloudpipe VPN servers. It defaults to the
IP address of the host.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment. It also will be ignored if the configuration option
for `network_manager` is not set to the default of
'nova.network.manager.VlanManager'.

Possible values:

    Any valid IP address. The default is $my_ip, the IP address of the VM.

Related options:

    ``network_manager``, ``use_neutron``, ``vpn_start``
"""),
    cfg.IntOpt("vpn_start",
            default=1000,
            help="""
This is the port number to use as the first VPN port for private networks.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment. It also will be ignored if the configuration option
for `network_manager` is not set to the default of
'nova.network.manager.VlanManager', or if you specify a value the 'vpn_start'
parameter when creating a network.

Possible values:

    Any integer representing a valid port number. The default is 1000.

Related options:

    ``use_neutron``, ``vpn_ip``, ``network_manager``
"""),
    cfg.IntOpt("network_size",
            default=256,
            help="""
This option determines the number of addresses in each private subnet.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Possible values:

    Any positive integer that is less than or equal to the available network
    size. Note that if you are creating multiple networks, they must all fit in
    the available IP address space. The default is 256.

Related options:

    ``use_neutron``, ``num_networks``
"""),
    cfg.StrOpt("fixed_range_v6",
            default="fd00::/48",
            help="""
This option determines the fixed IPv6 address block when creating a network.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Possible values:

    Any valid IPv6 CIDR. The default value is "fd00::/48".

Related options:

    ``use_neutron``
"""),
    cfg.StrOpt("gateway",
            help="""
This is the default IPv4 gateway. It is used only in the testing suite.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Possible values:

    Any valid IP address.

Related options:

    ``use_neutron``, ``gateway_v6``
"""),
    cfg.StrOpt("gateway_v6",
            help="""
This is the default IPv6 gateway. It is used only in the testing suite.

Please note that this option is only used when using nova-network instead of
Neutron in your deployment.

Possible values:

    Any valid IP address.

Related options:

    ``use_neutron``, ``gateway``
"""),
    cfg.IntOpt("cnt_vpn_clients",
            default=0,
            help="""
This option represents the number of IP addresses to reserve at the top of the
address range for VPN clients. It also will be ignored if the configuration
option for `network_manager` is not set to the default of
'nova.network.manager.VlanManager'.

Possible values:

    Any integer, 0 or greater. The default is 0.

Related options:

    ``use_neutron``, ``network_manager``
"""),
    cfg.IntOpt("fixed_ip_disassociate_timeout",
            default=600,
            help="""
This is the number of seconds to wait before disassociating a deallocated fixed
IP address. This is only used with the nova-network service, and has no effect
when using neutron for networking.

Possible values:

    Any integer, zero or greater. The default is 600 (10 minutes).

Related options:

    ``use_neutron``
"""),
    cfg.IntOpt("create_unique_mac_address_attempts",
            default=5,
            help="""
This option determines how many times nova-network will attempt to create a
unique MAC address before giving up and raising a
`VirtualInterfaceMacAddressException` error.

Possible values:

    Any positive integer. The default is 5.

Related options:

    ``use_neutron``
"""),
    cfg.BoolOpt("fake_call",
            default=False,
            help="""
When this option is True, calls are made locally instead of being placed in the
queue. However, all usage of this config option have been removed, so it
currently has no effect at all.

Related options:

    ``use_neutron``
"""),
    cfg.BoolOpt("teardown_unused_network_gateway",
            default=False,
            help="""
Determines whether unused gateway devices, both VLAN and bridge, are deleted if
the network is in nova-network VLAN mode and is multi-hosted.

Related options:

    ``use_neutron``, ``vpn_ip``, ``fake_network``
"""),
    cfg.BoolOpt("force_dhcp_release",
            default=True,
            help="""
When this option is True, a call is made to release the DHCP for the instance
when that instance is terminated.

Related options:

    ``use_neutron``
"""),
    cfg.BoolOpt("update_dns_entries",
            default=False,
            help="""
When this option is True, whenever a DNS entry must be updated, a fanout cast
message is sent to all network hosts to update their DNS entries in multi-host
mode.

Related options:

    ``use_neutron``
"""),
    cfg.IntOpt("dns_update_periodic_interval",
            default=-1,
            help="""
This option determines the time, in seconds, to wait between refreshing DNS
entries for the network.

Possible values:

    Either -1 (default), or any positive integer. A negative value will disable
    the updates.

Related options:

    ``use_neutron``
"""),
    cfg.StrOpt("dhcp_domain",
            default="novalocal",
            help="""
This option allows you to specify the domain for the DHCP server.

Possible values:

    Any string that is a valid domain name.

Related options:

    ``use_neutron``
"""),
    cfg.StrOpt("l3_lib",
            default="nova.network.l3.LinuxNetL3",
            help="""
This option allows you to specify the L3 management library to be used.

Possible values:

    Any dot-separated string that represents the import path to an L3
    networking library.

Related options:

    ``use_neutron``
"""),
    cfg.BoolOpt("share_dhcp_address",
            default=False,
            deprecated_for_removal=True,
            help="""
DEPRECATED: THIS VALUE SHOULD BE SET WHEN CREATING THE NETWORK.

If True in multi_host mode, all compute hosts share the same dhcp address. The
same IP address used for DHCP will be added on each nova-network node which is
only visible to the VMs on the same host.

The use of this configuration has been deprecated and may be removed in any
release after Mitaka. It is recommended that instead of relying on this option,
an explicit value should be passed to 'create_networks()' as a keyword argument
with the name 'share_address'.
"""),

    # NOTE(mriedem): Remove network_device_mtu in Newton.
    cfg.IntOpt("network_device_mtu",
            deprecated_for_removal=True,
            help="""
DEPRECATED: THIS VALUE SHOULD BE SET WHEN CREATING THE NETWORK.

MTU (Maximum Transmission Unit) setting for a network interface.

The use of this configuration has been deprecated and may be removed in any
release after Mitaka. It is recommended that instead of relying on this option,
an explicit value should be passed to 'create_networks()' as a keyword argument
with the name 'mtu'.
"""),
    cfg.BoolOpt('use_neutron',
                default=False,
                help="Whether to use Neutron or Nova Network as the back end "
                     "for networking. Defaults to False (indicating Nova "
                     "network).Set to True to use neutron.")
]

linux_net_opts = [
    cfg.MultiStrOpt('dhcpbridge_flagfile',
            default=['/etc/nova/nova-dhcpbridge.conf'],
            help="""
This option is a list of full paths to one or more configuration files for
dhcpbridge. In most cases the default path of '/etc/nova/nova-dhcpbridge.conf'
should be sufficient, but if you have special needs for configuring dhcpbridge,
you can change or add to this list.

Possible values

    A list of strings, where each string is the full path to a dhcpbridge
    configuration file.
"""),
    cfg.StrOpt('networks_path',
            default=paths.state_path_def('networks'),
            help="""
The location where the network configuration files will be kept. The default is
the 'networks' directory off of the location where nova's Python module is
installed.

Possible values

    A string containing the full path to the desired configuration directory
"""),
    cfg.StrOpt('public_interface',
            default='eth0',
            help="""
This is the name of the network interface for public IP addresses. The default
is 'eth0'.

Possible values:

    Any string representing a network interface name
"""),
    cfg.StrOpt('dhcpbridge',
            default=paths.bindir_def('nova-dhcpbridge'),
            help="""
The location of the binary nova-dhcpbridge. By default it is the binary named
'nova-dhcpbridge' that is installed with all the other nova binaries.

Possible values:

    Any string representing the full path to the binary for dhcpbridge
"""),
    cfg.StrOpt('routing_source_ip',
            default='$my_ip',
            help="""
This is the public IP address of the network host. It is used when creating a
SNAT rule.

Possible values:

    Any valid IP address

Related options:

    force_snat_range
"""),
    cfg.IntOpt('dhcp_lease_time',
            default=86400,
            help="""
The lifetime of a DHCP lease, in seconds. The default is 86400 (one day).

Possible values:

    Any positive integer value.
"""),
    cfg.MultiStrOpt("dns_server",
            default=[],
            help="""
Despite the singular form of the name of this option, it is actually a list of
zero or more server addresses that dnsmasq will use for DNS nameservers. If
this is not empty, dnsmasq will not read /etc/resolv.conf, but will only use
the servers specified in this option. If the option use_network_dns_servers is
True, the dns1 and dns2 servers from the network will be appended to this list,
and will be used as DNS servers, too.

Possible values:

    A list of strings, where each string is etiher an IP address or a FQDN.

Related options:

    use_network_dns_servers
"""),
    cfg.BoolOpt("use_network_dns_servers",
            default=False,
            help="""
When this option is set to True, the dns1 and dns2 servers for the network
specified by the user on boot will be used for DNS, as well as any specified in
the `dns_server` option.

Related options:

    dns_server
"""),
    cfg.ListOpt("dmz_cidr",
            default=[],
            help="""
This option is a list of zero or more IP address ranges in your network's DMZ
that should be accepted.

Possible values:

    A list of strings, each of which should be a valid CIDR.
"""),
    cfg.MultiStrOpt("force_snat_range",
            default=[],
            help="""
This is a list of zero or more IP ranges that traffic from the
`routing_source_ip` will be SNATted to. If the list is empty, then no SNAT
rules are created.

Possible values:

    A list of strings, each of which should be a valid CIDR.

Related options:

    routing_source_ip
"""),
    cfg.StrOpt("dnsmasq_config_file",
            default="",
            help="""
The path to the custom dnsmasq configuration file, if any.

Possible values:

    The full path to the configuration file, or an empty string if there is no
    custom dnsmasq configuration file.
"""),
    cfg.StrOpt("linuxnet_interface_driver",
            default="nova.network.linux_net.LinuxBridgeInterfaceDriver",
            help="""
This is the class used as the ethernet device driver for linuxnet bridge
operations. The default value should be all you need for most cases, but if you
wish to use a customized class, set this option to the full dot-separated
import path for that class.

Possible values:

    Any string representing a dot-separated class path that Nova can import.
"""),
    cfg.StrOpt("linuxnet_ovs_integration_bridge",
            default="br-int",
            help="""
The name of the Open vSwitch bridge that is used with linuxnet when connecting
with Open vSwitch."

Possible values:

    Any string representing a valid bridge name.
"""),
    cfg.BoolOpt("send_arp_for_ha",
            default=False,
            help="""
When True, when a device starts up, and upon binding floating IP addresses, arp
messages will be sent to ensure that the arp caches on the compute hosts are
up-to-date.

Related options:

    send_arp_for_ha_count
"""),
    cfg.IntOpt("send_arp_for_ha_count",
            default=3,
            help="""
When arp messages are configured to be sent, they will be sent with the count
set to the value of this option. Of course, if this is set to zero, no arp
messages will be sent.

Possible values:

    Any integer greater than or equal to 0

Related options:

    send_arp_for_ha
"""),
    cfg.BoolOpt("use_single_default_gateway",
            default=False,
            help="""
When set to True, only the firt nic of a VM will get its default gateway from
the DHCP server.
"""),
    cfg.MultiStrOpt("forward_bridge_interface",
            default=["all"],
            help="""
One or more interfaces that bridges can forward traffic to. If any of the items
in this list is the special keyword 'all', then all traffic will be forwarded.

Possible values:

    A list of zero or more interface names, or the word 'all'.
"""),
cfg.StrOpt('metadata_host',
               default='$my_ip',
               help='The IP address for the metadata API server'),
    cfg.IntOpt('metadata_port',
               default=8775,
               min=1,
               max=65535,
               help='The port for the metadata API port'),
    cfg.StrOpt('iptables_top_regex',
               default='',
               help='Regular expression to match the iptables rule that '
                    'should always be on the top.'),
    cfg.StrOpt('iptables_bottom_regex',
               default='',
               help='Regular expression to match the iptables rule that '
                    'should always be on the bottom.'),
    cfg.StrOpt('iptables_drop_action',
               default='DROP',
               help='The table that iptables to jump to when a packet is '
                    'to be dropped.'),
    cfg.IntOpt('ovs_vsctl_timeout',
               default=120,
               help='Amount of time, in seconds, that ovs_vsctl should wait '
                    'for a response from the database. 0 is to wait forever.'),
    cfg.BoolOpt('fake_network',
                default=False,
                help='If passed, use fake network devices and addresses'),
    cfg.IntOpt('ebtables_exec_attempts',
               default=3,
               help='Number of times to retry ebtables commands on failure.'),
    cfg.FloatOpt('ebtables_retry_interval',
                 default=1.0,
                 help='Number of seconds to wait between ebtables retries.'),
]


ldap_dns_opts = [
    cfg.StrOpt('ldap_dns_url',
                default='ldap://ldap.example.com:389',
                help='URL for LDAP server which will store DNS entries'),
    cfg.StrOpt('ldap_dns_user',
                default='uid=admin,ou=people,dc=example,dc=org',
                help='User for LDAP DNS'),
    cfg.StrOpt('ldap_dns_password',
                default='password',
                help='Password for LDAP DNS',
                secret=True),
    cfg.StrOpt('ldap_dns_soa_hostmaster',
                default='hostmaster@example.org',
                help='Hostmaster for LDAP DNS driver Statement of Authority'),
    cfg.MultiStrOpt('ldap_dns_servers',
                default=['dns.example.org'],
                help='DNS Servers for LDAP DNS driver'),
    cfg.StrOpt('ldap_dns_base_dn',
                default='ou=hosts,dc=example,dc=org',
                help='Base DN for DNS entries in LDAP'),
    cfg.StrOpt('ldap_dns_soa_refresh',
                default='1800',
                help='Refresh interval (in seconds) for LDAP DNS driver '
                     'Statement of Authority'),
    cfg.StrOpt('ldap_dns_soa_retry',
                default='3600',
                help='Retry interval (in seconds) for LDAP DNS driver '
                     'Statement of Authority'),
    cfg.StrOpt('ldap_dns_soa_expiry',
                default='86400',
                help='Expiry interval (in seconds) for LDAP DNS driver '
                     'Statement of Authority'),
    cfg.StrOpt('ldap_dns_soa_minimum',
                default='7200',
                help='Minimum interval (in seconds) for LDAP DNS driver '
                     'Statement of Authority'),
]

security_group_opts = [
    cfg.StrOpt('security_group_api',
                default='nova',
                help='DEPRECATED: Full class name of the security API class',
                deprecated_for_removal=True),
]

driver_opts = [
    cfg.StrOpt('network_driver',
               default='nova.network.linux_net',
               help='Driver to use for network creation'),
]

rpcapi_opts = [
    cfg.StrOpt('network_topic',
               default='network',
               help='The topic network nodes listen on'),
    cfg.BoolOpt('multi_host',
                default=False,
                help='Default value for multi_host in networks. Also, if set, '
                     'some rpc network calls will be sent directly to host.'),
]

ALL_DEFAULT_OPTS = (linux_net_opts + network_opts + ldap_dns_opts
                   + security_group_opts + rpcapi_opts + driver_opts)


def register_opts(conf):
    conf.register_opts(linux_net_opts)
    conf.register_opts(network_opts)
    conf.register_opts(ldap_dns_opts)
    conf.register_opts(security_group_opts)
    conf.register_opts(driver_opts)
    conf.register_opts(rpcapi_opts)


def list_opts():
    return {"DEFAULT": ALL_DEFAULT_OPTS}
