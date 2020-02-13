# Libraries
from random import randint

randnum = str(randint(100, 999))

# Rev: Decryption Lab-1.0.1
# Changes: Include Owncloud and Desktop VM scripts in python file.


# ssh_key and service_account
sshkey = "gcp_palo_alto:ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDBt3SswQU9rLucn3j7K9/+tyfPNZlOUGPEsne8etv4GWIIEy0wJxbj1io+bvg3IVovnCFiQSrEhHk2hijK6oLJg8fd2QH6dHWNuhrpxk7dt5QPiRqjFG5eQD93tl3G7ihXIV8yGo7ytdEkKTR6Tnh4v4iI2rfC21rSwjHCNhSWEKNy+kN/V+S/5EhBbz4yiaPxiYwr95oMNOM9cU0xN7CgvT2BOdkwr3sp0mBy49Cjp/yD/CckLU52sZ4vve1HsIUsTy3YSnnxLFHuI8PPc0k8IHnfL7MMcSIpUg1zyDhIHhaaryuachqspygkmm99ZhKfpHz7/RyNMW5Ne97qGyL/ gcp_palo_alto"
serviceaccount = "default"

# Locations
zone = "us-west1-b"
region = "us-west1"

# Machine Types
ngfw_machine_type = "n1-standard-4"
desktop_machine_type = "n1-standard-2"
own_cloud_machine_type = "n1-standard-2"
guacamole_machine_type = "n1-standard-2"


# Instance Names
ngfw_instance = "panw-fw" + randnum
owncloud_instance = "owncloud" + randnum
windows_instance = "desktop" + randnum
guacamole_instance = "guacamole" + randnum


# Source Images
pan_ngfw_image = "projects/panw-utd-public-cloud/global/images/pan-vm-series-ngfw901"
owncloud_image = "projects/decryption-lab-dev/global/images/owncloud-final"
windows_desktop_image = "projects/decryption-lab-dev/global/images/desktop-final"
guacamole_server_image = "projects/decryption-lab-dev/global/images/guacamol-final"


# Custom VPCs and Subnets
mgmt_network = "mgmt-network" + randnum
mgmt_subnet = "mgmt-subnet" + randnum
public_network = "public-network" + randnum
public_subnet = "public-subnet" + randnum
owncloud_network = "web-network" + randnum
owncloud_subnet = "web-subnet" + randnum
desktop_network = "db-network" + randnum
desktop_subnet = "db-subnet" + randnum


# Firewall-Rules
owncloud_firewall = "web-firewall" + randnum
desktop_firewall = "db-firewall" + randnum
mgmt_firewall = "mgmt-firewall" + randnum
public_firewall = "public-firewall" + randnum


# Routes
owncloud_route = "web-route" + randnum
desktop_route = "db-route" + randnum


# Internal Static IP Configuration

# PAN firewall Interfaces
managemet_interface_ip = '10.5.0.4'
public_interface_ip = '10.5.1.4'
owncloud_interface_ip = '10.5.2.4'
desktop_interface_ip = '10.5.3.4'


# Servers
owncloud_server_static_internal_ip = '10.5.2.5'
guac_primary_static_internal_ip = '10.5.0.5' # mgmt_network
guac_secondary_static_internal_ip = '10.5.1.3' # public_network

# Desktop interfaces configuration
desktop_static_primary_internal_ip = '10.5.3.5' # desktop_network
desktop_static_secondary_internal_ip = '10.5.1.5' # public network


# Subnets
mgmt_subnet_ip = '10.5.0.0/24'
owncloud_subnet_ip = '10.5.2.0/24'
public_subnet_ip = '10.5.1.0/24'
desktop_subnet_ip = '10.5.3.0/24'


COMPUTE_URL_BASE = 'https://www.googleapis.com/compute/v1/'


def GenerateConfig(context):
    outputs = []
    resources = [
        {
            'name': ngfw_instance,
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
                        'sourceImage': ''.join([COMPUTE_URL_BASE, pan_ngfw_image])
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
                        'subnetwork': '$(ref.' + mgmt_subnet + '.selfLink)',
                        'networkIP': managemet_interface_ip,
                    },
                    {
                        'network': '$(ref.' + public_network + '.selfLink)',
                        'subnetwork': '$(ref.' + public_subnet + '.selfLink)',
                        'networkIP': public_interface_ip,
                    },
                    {
                        'network': '$(ref.' + owncloud_network + '.selfLink)',
                        'subnetwork': '$(ref.' + owncloud_subnet + '.selfLink)',
                        'networkIP': owncloud_interface_ip,
                    },
                    {
                        'network': '$(ref.' + desktop_network + '.selfLink)',
                        'subnetwork': '$(ref.' + desktop_subnet + '.selfLink)',
                        'networkIP': desktop_interface_ip,
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
                    'dependsOn': [ngfw_instance],
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
                    'network': '$(ref.' + desktop_network + '.selfLink)',
                    'subnetwork': '$(ref.' + desktop_subnet + '.selfLink)',
                    'networkIP': desktop_static_primary_internal_ip
                    },
                    {
                    'network': '$(ref.' + public_network + '.selfLink)',
                    'subnetwork': '$(ref.' + public_subnet + '.selfLink)',
                    'networkIP': desktop_static_secondary_internal_ip
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
                    'dependsOn': [ngfw_instance, windows_instance],
                    'items': [{
                        'key': 'startup-script',
                        'value': "".join(["#!/bin/bash\n",
                                          "sudo sed -i 's/34.82.191.82/10.5.2.5/g' /var/www/owncloud/config/config.php\n"
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
                    'network': '$(ref.' + owncloud_network + '.selfLink)',
                    'subnetwork': '$(ref.' + owncloud_subnet + '.selfLink)',
                    'networkIP': owncloud_server_static_internal_ip
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
                    'dependsOn': [ngfw_instance, windows_instance],
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
                        'network': '$(ref.' + mgmt_network + '.selfLink)',
                        'accessConfigs': [{
                            'name': 'MGMT Access',
                            'type': 'ONE_TO_ONE_NAT'
                        }],
                        'subnetwork': '$(ref.' + mgmt_subnet + '.selfLink)',
                        'networkIP': guac_primary_static_internal_ip,
                    },
                    {
                    'network': '$(ref.' + public_network + '.selfLink)',
                    'subnetwork': '$(ref.' + public_subnet + '.selfLink)',
                    'networkIP': guac_secondary_static_internal_ip
                    }
                    ]
            }
        },
        {
            'name': owncloud_network,
            'type': 'compute.v1.network',
            'properties': {
                'autoCreateSubnetworks': False,
            }
        },
        {
            'name': owncloud_subnet,
            'type': 'compute.v1.subnetwork',
            'properties': {
                'ipCidrRange': owncloud_subnet_ip,
                'region': region,
                'network': '$(ref.' + owncloud_network + '.selfLink)',
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
            'name': desktop_network,
            'type': 'compute.v1.network',
            'properties': {
                'autoCreateSubnetworks': False,

            }
        },
        {
            'name': desktop_subnet,
            'type': 'compute.v1.subnetwork',
            'properties': {
                'ipCidrRange': desktop_subnet_ip,
                'region': region,
                'network': '$(ref.' + desktop_network + '.selfLink)',
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, desktop_network, owncloud_network, public_network]
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
                    'ports': [22, 443, 8080]
                }]
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, desktop_network, owncloud_network, public_network]
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
                    'ports': [221, 3389]
                }]
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, desktop_network, owncloud_network, public_network]
            },
            'name': owncloud_firewall,
            'type': 'compute.v1.firewall',
            'properties': {
                'region': region,
                'network': '$(ref.' + owncloud_network + '.selfLink)',
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
                'dependsOn': [mgmt_network, desktop_network, owncloud_network, public_network]
            },
            'name': desktop_firewall,
            'type': 'compute.v1.firewall',
            'properties': {
                'region': region,
                'network': '$(ref.' + desktop_network + '.selfLink)',
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
                'dependsOn': [mgmt_network, desktop_network, owncloud_network, public_network]
            },
            'name': owncloud_route,
            'type': 'compute.v1.route',
            'properties': {
                'priority': 100,
                'network': '$(ref.' + owncloud_network + '.selfLink)',
                'destRange': '0.0.0.0/0',
                'nextHopIp': '$(ref.' + ngfw_instance + '.networkInterfaces[2].networkIP)'
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, desktop_network, owncloud_network, public_network]
            },
            'name': desktop_route,
            'type': 'compute.v1.route',
            'properties': {
                'priority': 100,
                'network': '$(ref.' + desktop_network + '.selfLink)',
                'destRange': '0.0.0.0/0',
                'nextHopIp': '$(ref.' + ngfw_instance + '.networkInterfaces[3].networkIP)'
            }
        }

    ]
    outputs.append({'name': 'Guacamole-PublicIP-Address',
                    'value': 'http://' + '$(ref.' + guacamole_instance + '.networkInterfaces[0].accessConfigs[0].natIP)' + ':8080/guacamole'})
    outputs.append({'name': 'PANFirewall-Internal-IP-Address',
                    'value': '$(ref.' + ngfw_instance + '.networkInterfaces[0].networkIP)'})
    outputs.append({'name': 'OwnCloud-Internal-IP-Address',
                    'value': 'http://' + '$(ref.' + owncloud_instance + '.networkInterfaces[0].networkIP)'})
    return {'resources': resources, 'outputs': outputs}
