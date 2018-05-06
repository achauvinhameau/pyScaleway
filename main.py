# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2018-05-06 15:17:19 alex>
#

"""Testing the scaleway API."""

import logging
import pprint
import argparse

# from COrg import organization
from CImages import images
from CServers import servers
from CVolumes import volumes

__version__ = '1.0.0'


def cli_read_args():
    """Parse args."""
    parser = argparse.ArgumentParser(description='scaleway API test lab',
                                     epilog="version {}".format(__version__))

    parser.add_argument('--log', '-l',
                        metavar='level',
                        default='ERROR',
                        type=str,
                        help='log level DEBUG, INFO, WARNING, [ERROR]',
                        nargs=1,
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'])

    parser.add_argument('--vol', dest="f_volumes", action='store_const',
                        const=True, default=False, help='list volumes')

    parser.add_argument('--srv', dest="f_servers", action='store_const',
                        const=True, default=False, help='list servers')

    parser.add_argument('--img', dest="f_images", action='store_const',
                        const=True, default=False, help='list images')

    parser.add_argument('--create',
                        metavar=('name', 'image', 'type'),
                        nargs=3,
                        help='create a server, image is a key (see --img),\
                        type = START1-XS...,\
                        name could be set to random')

    parser.add_argument('--delete',
                        metavar=('what', 'id'),
                        nargs=2,
                        help='delete a resource, what=[server]|[volume]')

    parser.add_argument('--tags',
                        metavar='tag',
                        nargs='*',
                        help='tags associated with server')

    return parser.parse_args()


def set_log(args):
    """Set the log format and level based on the args."""
    log_format = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
    log_level = logging.ERROR

    if args.log[0] == "DEBUG":
        log_level = logging.DEBUG
    elif args.log[0] == 'WARNING':
        log_level = logging.WARNING
    elif args.log[0] == 'ERROR':
        log_level = logging.ERROR
    elif args.log[0] == 'INFO':
        log_level = logging.INFO

    logging.basicConfig(format=log_format, level=log_level)


def main():
    """Main bloc for this module."""
    args = cli_read_args()

    set_log(args)

    if args.f_servers:
        print(servers)

    if args.f_images:
        print(images)

    if args.f_volumes:
        print(volumes)

    # -------- create --------------
    if isinstance(args.create, list):
        resp = None

        if args.create[0] == "random":
            srv_name = ""
        else:
            srv_name = args.create[0]

        if isinstance(args.tags, list):
            srv_tags = args.tags
        else:
            srv_tags = ""

        resp = servers.create_server(name=srv_name,
                                     image=args.create[1],
                                     srv_type=args.create[2],
                                     tags=srv_tags)
        pprint.pprint(resp)

    # -------- delete --------------
    elif isinstance(args.delete, list):
        if args.delete[0] == "server":
            resp = servers.delete(srv_id=args.delete[1])
            pprint.pprint(resp)

        elif args.delete[0] == "volume":
            resp = volumes.delete(volume_id=args.delete[1])
            pprint.pprint(resp)

        else:
            logging.error("delete unknown resource")

    logging.info("exiting")


if __name__ == '__main__':
    main()
