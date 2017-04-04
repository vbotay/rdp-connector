import argparse
import rdp_connect
import config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('vm_name', type=str, help='vm_name')
    parser.add_argument('pc_id', type=str, default=config.DEFAULT_SUFFIX,
                        nargs='?', help='PC Id. Default: 0')

    args = parser.parse_args()
    vm_name = args.vm_name
    machine_sufix = args.pc_id

    vms = rdp_connect.get_machine_list(vm_name)
    ip = rdp_connect.get_machine_ip(vms=vms, suffix=machine_sufix)
    rdp_connect.open_rdp(ip)

if __name__ == '__main__':
    main()
