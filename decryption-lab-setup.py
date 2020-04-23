# Libraries
from random import randint

randnum = str(randint(100, 999))

# Description: This template deploy the VM-Series firewall private image and other necessary resources to practice the decryption workshop
# Author: Palo Alto Networks (RD Singh)
# Template version: 1.0
# Date Modified: 2020-04-20
# Updated windows_desktop_image from windows-desktop-20200413 to windows-desktop-20200420

# ssh_key and service_account
sshkey = "gcp_palo_alto:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDBt3SswQU9rLucn3j7K9/+tyfPNZlOUGPEsne8etv4GWIIEy0wJxbj1io+bvg3IVovnCFiQSrEhHk2hijK6oLJg8fd2QH6dHWNuhrpxk7dt5QPiRqjFG5eQD93tl3G7ihXIV8yGo7ytdEkKTR6Tnh4v4iI2rfC21rSwjHCNhSWEKNy+kN/V+S/5EhBbz4yiaPxiYwr95oMNOM9cU0xN7CgvT2BOdkwr3sp0mBy49Cjp/yD/CckLU52sZ4vve1HsIUsTy3YSnnxLFHuI8PPc0k8IHnfL7MMcSIpUg1zyDhIHhaaryuachqspygkmm99ZhKfpHz7/RyNMW5Ne97qGyL/ gcp_palo_alto"
serviceaccount = "default"

# Locations
zone = "us-central1-b"
region = "us-central1"

# Machine Types
ngfw_machine_type = "n1-standard-4"
desktop_machine_type = "n1-standard-2"
own_cloud_machine_type = "n1-standard-2"
guacamole_machine_type = "n1-standard-2"


# Instance Names
vmseries_ngfw_instance = "vmseries-ngfw" + randnum
owncloud_instance = "owncloud" + randnum
windows_instance = "windows-desktop" + randnum
guacamole_instance = "guacamole" + randnum


# Source Images
vmseries_ngfw_image = "projects/decryption-lab-dev/global/images/vmseries-ngfw-v91-20200413"
owncloud_image = "projects/decryption-lab-dev/global/images/owncloud-image-20200413"
windows_desktop_image = "projects/decryption-lab-dev/global/images/windows-desktop-20200420"
guacamole_server_image = "projects/decryption-lab-dev/global/images/guacamole-image-202004013"

# Custom VPCs and Subnets
mgmt_network = "mgmt-network" + randnum
mgmt_subnet = "mgmt-subnet" + randnum
public_network = "public-network" + randnum
public_subnet = "public-subnet" + randnum
untrust_network = "untrust-network" + randnum
untrust_subnet = "untrust-subnet" + randnum
trust_network = "trust-network" + randnum
trust_subnet = "trust-subnet" + randnum

# Firewall-Rules
mgmt_firewall = "mgmt-firewall" + randnum
public_firewall = "public-firewall" + randnum
untrust_firewall = "untrust-firewall" + randnum
trust_firewall = "trust-firewall" + randnum

# Routes
untrust_route = "untrust-route" + randnum
trust_route = "trust-route" + randnum


# Subnets
mgmt_subnet_ip = '10.5.1.0/24'
public_subnet_ip = '10.5.0.0/24'
untrust_subnet_ip = '172.16.1.0/24'
trust_subnet_ip = '192.168.11.0/24'

# VM-Series firewall Interfaces
vmseries_mgmt_interface_ip = '10.5.1.99'
vmseries_untrust_interface_ip = '172.16.1.99'
vmseries_trust_interface_ip = '192.168.11.99'


# Guacamole interfaces configuration (Mgmt and Public Network)
guac_mgmt_ip = '10.5.1.5'  # mgmt_network
guac_public_ip = '10.5.0.5'  # public_network

# Desktop interfaces configuration (mgmt and trust Network)
desktop_mgmt_ip = '10.5.1.10'
desktop_trust_ip = '192.168.11.100'

# Owncloud interfaces configuration (untrust Network)
owncloud_untrust_ip = '172.16.1.100'


COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'


def GenerateConfig(context):
    outputs = []
    resources = [
        {
            'name': vmseries_ngfw_instance,
            'type': 'compute.v1.instance',
            'properties': {
                'zone': zone,
                'machineType': ''.join([COMPUTE_URL_BASE, 'projects/', context.env['project'],
                                        '/zones/', zone,
                                        '/machineTypes/', ngfw_machine_type]),
                'canIpForward': True,
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': ''.join([COMPUTE_URL_BASE, vmseries_ngfw_image])
                    }
                }],
                'metadata': {
                    'items': [{'key': 'ssh-keys', 'value': sshkey},
                              {'key': 'serial-port-enable', 'value': '1'}]
                },
                'serviceAccounts': [{
                    'email': serviceaccount,
                    'scopes': [
                        'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                        'https://www.googleapis.com/auth/devstorage.read_only',
                        'https://www.googleapis.com/auth/logging.write',
                        'https://www.googleapis.com/auth/monitoring.write',
                    ]}
                ],
                'networkInterfaces': [
                    {
                        'network': '$(ref.' + mgmt_network + '.selfLink)',
                        'accessConfigs': [{
                            'name': 'MGMT Access',
                            'type': 'ONE_TO_ONE_NAT'
                        }],
                        'subnetwork': '$(ref.' + mgmt_subnet + '.selfLink)',
                        'networkIP': vmseries_mgmt_interface_ip,
                    },
                    {
                        'network': '$(ref.' + untrust_network + '.selfLink)',
                        'subnetwork': '$(ref.' + untrust_subnet + '.selfLink)',
                        'networkIP': vmseries_untrust_interface_ip,
                    },
                    {
                        'network': '$(ref.' + trust_network + '.selfLink)',
                        'subnetwork': '$(ref.' + trust_subnet + '.selfLink)',
                        'networkIP': vmseries_trust_interface_ip,
                    }
                ]
            }
        },
        {
            'name': windows_instance,
            'type': 'compute.v1.instance',
            'properties': {
                'zone': zone,
                'machineType': ''.join([COMPUTE_URL_BASE, 'projects/', context.env["project"],
                                        '/zones/', zone,
                                        '/machineTypes/', desktop_machine_type]),
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': ''.join([COMPUTE_URL_BASE, windows_desktop_image])
                    }
                }],
                'metadata': {
                    'dependsOn': [vmseries_ngfw_instance],
                    'items': []
                },
                'serviceAccounts': [{
                    'email': serviceaccount,
                    'scopes': [
                        'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                        'https://www.googleapis.com/auth/devstorage.read_only',
                        'https://www.googleapis.com/auth/logging.write',
                        'https://www.googleapis.com/auth/monitoring.write',
                        'https://www.googleapis.com/auth/compute.readonly',
                    ]}
                ],
                'networkInterfaces': [{
                    'network': '$(ref.' + trust_network + '.selfLink)',
                    'subnetwork': '$(ref.' + trust_subnet + '.selfLink)',
                    'networkIP': desktop_trust_ip
                    },
                    {
                    'network': '$(ref.' + mgmt_network + '.selfLink)',
                    'subnetwork': '$(ref.' + mgmt_subnet + '.selfLink)',
                    'networkIP': desktop_mgmt_ip
                }]
            }
        },
        {
            'name': owncloud_instance,
            'type': 'compute.v1.instance',
            'properties': {
                'zone': zone,
                'machineType': ''.join([COMPUTE_URL_BASE, 'projects/', context.env["project"],
                                        '/zones/', zone,
                                        '/machineTypes/', own_cloud_machine_type]),
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': ''.join([COMPUTE_URL_BASE, owncloud_image])
                    }
                }],
                'metadata': {
                    'dependsOn': [vmseries_ngfw_instance, windows_instance],
                    'items': [{
                        'key': 'startup-script',
                        'value': "".join(["#!/bin/bash\n",
                                          "sudo sed -i 's/34.82.191.82/192.168.11.100/g' /var/www/owncloud/config/config.php\n"
                                          ])},
                        {'key': 'ssh-keys', 'value': sshkey},
                        {'key': 'serial-port-enable', 'value': '1'}]
                },
                'serviceAccounts': [{
                    'email': serviceaccount,
                    'scopes': [
                        'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                        'https://www.googleapis.com/auth/devstorage.read_only',
                        'https://www.googleapis.com/auth/logging.write',
                        'https://www.googleapis.com/auth/monitoring.write',
                        'https://www.googleapis.com/auth/compute.readonly',
                    ]}
                ],
                'networkInterfaces': [{
                    'network': '$(ref.' + untrust_network + '.selfLink)',
                    'subnetwork': '$(ref.' + untrust_subnet + '.selfLink)',
                    'networkIP': owncloud_untrust_ip
                }]
            }
        },
        {
            'name': guacamole_instance,
            'type': 'compute.v1.instance',
            'properties': {
                'zone': zone,
                'machineType': ''.join([COMPUTE_URL_BASE, 'projects/', context.env["project"],
                                        '/zones/', zone,
                                        '/machineTypes/', guacamole_machine_type]),
                'disks': [{
                    'deviceName': 'boot',
                    'type': 'PERSISTENT',
                    'boot': True,
                    'autoDelete': True,
                    'initializeParams': {
                        'sourceImage': ''.join([COMPUTE_URL_BASE, guacamole_server_image])
                    }
                }],
                'metadata': {
                    'dependsOn': [vmseries_ngfw_instance, windows_instance],
                    'items': [{
                        'key': 'startup-script',
                        'value': "".join(["#!/bin/bash\n",
                                          "echo 'startup-script'\n"
                                          ])},
                        {'key': 'ssh-keys', 'value': sshkey},
                        {'key': 'serial-port-enable', 'value': '1'}]
                },
                'serviceAccounts': [{
                    'email': serviceaccount,
                    'scopes': [
                        'https://www.googleapis.com/auth/cloud.useraccounts.readonly',
                        'https://www.googleapis.com/auth/devstorage.read_only',
                        'https://www.googleapis.com/auth/logging.write',
                        'https://www.googleapis.com/auth/monitoring.write',
                        'https://www.googleapis.com/auth/compute.readonly',
                    ]}
                ],
                'networkInterfaces': [{
                        'network': '$(ref.' + public_network + '.selfLink)',
                        'accessConfigs': [{
                            'name': 'MGMT Access',
                            'type': 'ONE_TO_ONE_NAT'
                        }],
                        'subnetwork': '$(ref.' + public_subnet + '.selfLink)',
                        'networkIP': guac_public_ip,
                    },
                    {
                    'network': '$(ref.' + mgmt_network + '.selfLink)',
                    'subnetwork': '$(ref.' + mgmt_subnet + '.selfLink)',
                    'networkIP': guac_mgmt_ip
                    }
                    ]
            }
        },
        {
            'name': mgmt_network,
            'type': 'compute.v1.network',
            'properties': {
                'autoCreateSubnetworks': False,
            }
        },
        {
            'name': mgmt_subnet,
            'type': 'compute.v1.subnetwork',
            'properties': {
                'ipCidrRange': mgmt_subnet_ip,
                'region': region,
                'network': '$(ref.' + mgmt_network + '.selfLink)',
            }
        },
        {
            'name': public_network,
            'type': 'compute.v1.network',
            'properties': {
                'autoCreateSubnetworks': False,
            }
        },
        {
            'name': public_subnet,
            'type': 'compute.v1.subnetwork',
            'properties': {
                'ipCidrRange': public_subnet_ip,
                'region': region,
                'network': '$(ref.' + public_network + '.selfLink)',
            }
        },

        {
            'name': trust_network,
            'type': 'compute.v1.network',
            'properties': {
                'autoCreateSubnetworks': False,

            }
        },
        {
            'name': trust_subnet,
            'type': 'compute.v1.subnetwork',
            'properties': {
                'ipCidrRange': trust_subnet_ip,
                'region': region,
                'network': '$(ref.' + trust_network + '.selfLink)',
            }
        },
        {
            'name': untrust_network,
            'type': 'compute.v1.network',
            'properties': {
                'autoCreateSubnetworks': False,
            }
        },
        {
            'name': untrust_subnet,
            'type': 'compute.v1.subnetwork',
            'properties': {
                'ipCidrRange': untrust_subnet_ip,
                'region': region,
                'network': '$(ref.' + untrust_network + '.selfLink)',
            }
        },

        {
            'metadata': {
                'dependsOn': [mgmt_network, public_network, trust_network, untrust_network]
            },
            'name': mgmt_firewall,
            'type': 'compute.v1.firewall',
            'properties': {
                'region': region,
                'network': '$(ref.' + mgmt_network + '.selfLink)',
                'direction': 'INGRESS',
                'priority': 1000,
                'sourceRanges': ['0.0.0.0/0'],
                'allowed': [{
                    'IPProtocol': 'tcp',
                    'ports': [22, 443, 8080, 3389]
                }]
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, public_network, trust_network, untrust_network]
            },
            'name': public_firewall,
            'type': 'compute.v1.firewall',
            'properties': {
                'region': region,
                'network': '$(ref.' + public_network + '.selfLink)',
                'direction': 'INGRESS',
                'priority': 1000,
                'sourceRanges': ['0.0.0.0/0'],
                'allowed': [{
                    'IPProtocol': 'tcp',
                    'ports': [22, 443, 8080, 3389]
                }]
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, public_network, trust_network, untrust_network]
            },
            'name': untrust_firewall,
            'type': 'compute.v1.firewall',
            'properties': {
                'region': region,
                'network': '$(ref.' + untrust_network + '.selfLink)',
                'direction': 'INGRESS',
                'priority': 1000,
                'sourceRanges': ['0.0.0.0/0'],
                'allowed': [{
                    'IPProtocol': 'tcp',
                }, {
                    'IPProtocol': 'udp',
                }, {
                    'IPProtocol': 'icmp'
                }]
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, public_network, trust_network, untrust_network]
            },
            'name': trust_firewall,
            'type': 'compute.v1.firewall',
            'properties': {
                'region': region,
                'network': '$(ref.' + trust_network + '.selfLink)',
                'direction': 'INGRESS',
                'priority': 1000,
                'sourceRanges': ['0.0.0.0/0'],
                'allowed': [{
                    'IPProtocol': 'tcp',
                }, {
                    'IPProtocol': 'udp',
                }, {
                    'IPProtocol': 'icmp'
                }]
            }
        },

        {
            'metadata': {
                'dependsOn': [mgmt_network, public_network, trust_network, untrust_network]
            },
            'name': untrust_route,
            'type': 'compute.v1.route',
            'properties': {
                'priority': 100,
                'network': '$(ref.' + untrust_network + '.selfLink)',
                'destRange': '0.0.0.0/0',
                'nextHopIp': '$(ref.' + vmseries_ngfw_instance + '.networkInterfaces[1].networkIP)'
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, public_network, trust_network, untrust_network]
            },
            'name': trust_route,
            'type': 'compute.v1.route',
            'properties': {
                'priority': 100,
                'network': '$(ref.' + trust_network + '.selfLink)',
                'destRange': '0.0.0.0/0',
                'nextHopIp': '$(ref.' + vmseries_ngfw_instance + '.networkInterfaces[2].networkIP)'
            }
        }

    ]
    outputs.append({'name': 'Guacamole-PublicIP-Address',
                    'value': 'http://' + '$(ref.' + guacamole_instance + '.networkInterfaces[0].accessConfigs[0].natIP)' + ':8080/guacamole'})
    outputs.append({'name': 'PANFirewall-Internal-IP-Address',
                    'value': '$(ref.' + vmseries_ngfw_instance + '.networkInterfaces[0].networkIP)'})
    outputs.append({'name': 'OwnCloud-Internal-IP-Address',
                    'value': 'http://' + '$(ref.' + owncloud_instance + '.networkInterfaces[0].networkIP)'})
    return {'resources': resources, 'outputs': outputs}
