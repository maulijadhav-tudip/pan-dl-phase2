# Libraries
from random import randint

randnum = str(randint(100, 999))

# Rev: Decryption Lab-1.0.3


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
trust2_network = "trust2-network" + randnum
trust2_subnet = "trust2-subnet" + randnum
trust1_network = "trust1-network" + randnum
trust1_subnet = "trust1-subnet" + randnum


# Firewall-Rules
trust2_firewall = "trust2-firewall" + randnum
trust1_firewall = "trust1-firewall" + randnum
mgmt_firewall = "mgmt-firewall" + randnum
public_firewall = "public-firewall" + randnum


# Routes
trust2_route = "trust2-route" + randnum
trust1_route = "trust1-route" + randnum


# Internal Static IP Configuration

# PAN firewall Interfaces
managemet_interface_ip = '10.5.1.4'
public_interface_ip = '10.5.0.4'
trust2_interface_ip = '10.5.3.4'  # trust 2
trust1_interface_ip = '10.5.2.4' # trust 1


# Make fourth octet consistent
# Owncloud primary interface - public

# Servers
# Guacamole interfaces configuration (Mgmt and Public Network)
guac_primary_static_internal_ip = '10.5.1.5'  # mgmt_network
guac_secondary_static_internal_ip = '10.5.0.5'  # public_network

# Desktop interfaces configuration (Public Network)
owncloud_server_static_internal_ip = '10.5.0.15'  # public_network

# Desktop interfaces configuration (Trust 1 and Public Network)
desktop_static_primary_internal_ip = '10.5.2.10'  # trust_1_network
desktop_static_secondary_internal_ip = '10.5.0.10'  # public network


# Subnets
mgmt_subnet_ip = '10.5.1.0/24'
trust2_subnet_ip = '10.5.3.0/24'

public_subnet_ip = '10.5.0.0/24'
trust1_subnet_ip = '10.5.2.0/24'


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
                        'accessConfigs': [{
                            'name': 'MGMT Access',
                            'type': 'ONE_TO_ONE_NAT'
                        }],
                        'subnetwork': '$(ref.' + mgmt_subnet + '.selfLink)',
                        'networkIP': managemet_interface_ip,
                    },
                    {
                        'network': '$(ref.' + public_network + '.selfLink)',
                        'subnetwork': '$(ref.' + public_subnet + '.selfLink)',
                        'networkIP': public_interface_ip,
                    },
                    {
                        'network': '$(ref.' + trust2_network + '.selfLink)',
                        'subnetwork': '$(ref.' + trust2_subnet + '.selfLink)',
                        'networkIP': trust2_interface_ip,
                    },
                    {
                        'network': '$(ref.' + trust1_network + '.selfLink)',
                        'subnetwork': '$(ref.' + trust1_subnet + '.selfLink)',
                        'networkIP': trust1_interface_ip,
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
                    'network': '$(ref.' + trust1_network + '.selfLink)',
                    'subnetwork': '$(ref.' + trust1_subnet + '.selfLink)',
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
                    'network': '$(ref.' + public_network + '.selfLink)',
                    'subnetwork': '$(ref.' + public_subnet + '.selfLink)',
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
            'name': trust2_network,
            'type': 'compute.v1.network',
            'properties': {
                'autoCreateSubnetworks': False,
            }
        },
        {
            'name': trust2_subnet,
            'type': 'compute.v1.subnetwork',
            'properties': {
                'ipCidrRange': trust2_subnet_ip,
                'region': region,
                'network': '$(ref.' + trust2_network + '.selfLink)',
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
            'name': trust1_network,
            'type': 'compute.v1.network',
            'properties': {
                'autoCreateSubnetworks': False,

            }
        },
        {
            'name': trust1_subnet,
            'type': 'compute.v1.subnetwork',
            'properties': {
                'ipCidrRange': trust1_subnet_ip,
                'region': region,
                'network': '$(ref.' + trust1_network + '.selfLink)',
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, trust1_network, trust2_network, public_network]
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
                'dependsOn': [mgmt_network, trust1_network, trust2_network, public_network]
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
                    'ports': [22, 3389, 443]
                }]
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, trust1_network, trust2_network, public_network]
            },
            'name': trust2_firewall,
            'type': 'compute.v1.firewall',
            'properties': {
                'region': region,
                'network': '$(ref.' + trust2_network + '.selfLink)',
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
                'dependsOn': [mgmt_network, trust1_network, trust2_network, public_network]
            },
            'name': trust1_firewall,
            'type': 'compute.v1.firewall',
            'properties': {
                'region': region,
                'network': '$(ref.' + trust1_network + '.selfLink)',
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
                'dependsOn': [mgmt_network, trust1_network, trust2_network, public_network]
            },
            'name': trust2_route,
            'type': 'compute.v1.route',
            'properties': {
                'priority': 100,
                'network': '$(ref.' + trust2_network + '.selfLink)',
                'destRange': '0.0.0.0/0',
                'nextHopIp': '$(ref.' + ngfw_instance + '.networkInterfaces[2].networkIP)'
            }
        },
        {
            'metadata': {
                'dependsOn': [mgmt_network, trust1_network, trust2_network, public_network]
            },
            'name': trust1_route,
            'type': 'compute.v1.route',
            'properties': {
                'priority': 100,
                'network': '$(ref.' + trust1_network + '.selfLink)',
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
