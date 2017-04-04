import argparse
import rdp_connect
import config


def run_show_list(args):
    rdp_connect.show_vms(name=args.vm_name,
                         verbose=args.verbose)


def run_rdp_connect(args):
    vms = rdp_connect.get_machine_list(args.vm_name)
    ip = rdp_connect.get_machine_ip(vms=vms, suffix=args.suffix)
    rdp_connect.open_rdp(ip)


def cli():
    # TODO descriptions
    parser = argparse.ArgumentParser(prog="VM manager",
                                     description="Description")

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    parser_rdp = subparsers.add_parser('rdp',
                                       description='Open RDP to specified VM')
    parser_rdp.add_argument('-n', '--vm-name', type=str, help='vm name',
                            required=True)
    parser_rdp.add_argument('-s', '--suffix', type=str,
                            default=config.DEFAULT_SUFFIX,
                            help='Default: {}'.format(config.DEFAULT_SUFFIX))
    parser_rdp.set_defaults(func=run_rdp_connect)

    parser_show = subparsers.add_parser('list',
                                        description='List of VMs')
    parser_show.add_argument('-n', '--vm-name', type=str,
                             help='part of vm name')
    parser_show.add_argument('-v', '--verbose', action='store_true',
                             help='verbose output')
    parser_show.set_defaults(func=run_show_list)

    return parser.parse_args()


def main():
    args = cli()
    args.func(args)

if __name__ == '__main__':
    main()
