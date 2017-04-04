import os

VCENTER_IP = os.environ.get('VCENTER_IP', 'default_ip')
VCENTER_USER = os.environ.get('VCENTER_USER', 'default_username')
VCENTER_PASSWORD = os.environ.get('VCENTER_PASSWORD', 'default_pwd')

# IP of vm should be matched with the followng net
DEFAULT_NET = os.environ.get('DEFAULT_NET', '10.0.0.0/8')

# Suffix of VM if by name matched more then one VM
# e.g. machine name labs1machine, suffix pc0
# so vm name is labs1machinepc0
DEFAULT_SUFFIX = os.environ.get('DEFAULT_SUFFIX', 'default_suffix')
