import ssl
import subprocess
import sys

from pyVim.connect import SmartConnect
import config


class NoVMsError(Exception):
    pass


class NoIPsError(Exception):
    pass


def _get_dc(host=config.VCENTER_IP, user=config.VCENTER_USER,
            pwd=config.VCENTER_PASSWORD):
    """ Get datacenter

    :param host: vcenter ip
    :param user: vcenter user
    :param pwd: vcenter password
    :return:
    """
    s = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    s.verify_mode = ssl.CERT_NONE
    print('Connecting to vCenter {}....'.format(host))
    c = SmartConnect(host=host, user=user, pwd=pwd, sslContext=s)
    datacenter = c.content.rootFolder.childEntity[0]
    return datacenter


def get_machine_list(name=None):
    """Get machines matched the name
    :param name: machine name or part of machine name

    """
    vms = _get_dc().vmFolder.childEntity
    print('Getting list of VMs...\n')
    list_vms = [vm for vm in vms if hasattr(vm, 'summary')]
    if name is None:
        return list_vms
    else:
        list_vms = [vm for vm in list_vms if name in vm.summary.vm.name]

    if not list_vms:
        raise NoVMsError('No machines matched {} were found'.format(name))

    return list_vms


def get_machine_ips(vms, suffix=None):
    # TODO implement getting machine ips, not ips of few vms
    suffix = '' if suffix is None else suffix
    machine_ips = [pc.summary.guest.ipAddress for pc in vms if suffix in
                  pc.summary.vm.name]
    if not machine_ips:
        raise NoIPsError('No machine ips')
    return machine_ips


def show_vms(name=None, verbose=False):
    vms = get_machine_list(name=name)

    for vm in vms:
        summary = vm.summary
        print("Name         : ", summary.config.name)
        print("IP           : ", summary.guest.ipAddress)
        if verbose:
            print("Path         : ", summary.config.vmPathName)
            print("Guest        : ", summary.config.guestFullName)
            print("State        : ", summary.runtime.powerState)
        print("\n", "="*50, '\n')


def get_machine_ip(vms, suffix=None, net=config.DEFAULT_NET):
    # TODO check network matching
    ip = get_machine_ips(vms, suffix)[0]
    from ipaddress import IPv4Address, IPv4Network
    if IPv4Address(ip) in IPv4Network(net):
        return ip
    raise NoIPsError('{} not in network {}'.format(ip, net))


def open_rdp(ip):
    print('Connecting to {} by RDP...'.format(ip))
    if sys.platform == 'win32':
        subprocess.Popen('mstsc /v:{}'.format(ip))
    elif sys.platform == 'darwin':
        cmd = ('rdp://full%20address=s:{}:3389&audiomode=i:0'
               '&authentication=i:0&use%20multimon=i:0').format(ip)
        print(cmd)
        subprocess.Popen(['open', cmd])
    else:
        raise NotImplementedError(
            'Not implemented for your system: {}'.format(sys.platform))
