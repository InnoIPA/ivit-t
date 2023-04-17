import logging, sys
from common import config_logger
from argparse import ArgumentParser, SUPPRESS
from webapi import app, socketio, \
                    app_cl_pj, app_ud_dt, app_dy_dt, app_labeling, \
                    app_aug, app_cl_model, app_train, app_export, app_eval, app_icap
from webapi.common import init_db, init_sample_to_db, init_for_icap, register_mqtt_event, get_all_addr
from webapi.common.config import *

def build_argparser():
    parser = ArgumentParser(add_help=False)
    args = parser.add_argument_group('Options')
    args.add_argument('-h', '--help', action='help', default=SUPPRESS, help='Show this help message and exit.')
    args.add_argument('-port', '--port', required=True, help = "Input port number")
    return parser

def main(args):
    # Create initial table in db
    logging.info("Initial database...")
    init_db()
    # Fill in db from sample
    logging.info("Initial sample project...")
    init_sample_to_db()

    app.register_blueprint(app_cl_pj)
    app.register_blueprint(app_ud_dt)
    app.register_blueprint(app_dy_dt)
    app.register_blueprint(app_aug)
    app.register_blueprint(app_labeling)
    app.register_blueprint(app_cl_model)
    app.register_blueprint(app_train)
    app.register_blueprint(app_export)
    app.register_blueprint(app_eval)
    app.register_blueprint(app_icap)

    # Update ip address 
    if app.config.get("HOST") in [ None, "" ]: 
        ips = get_all_addr() 
        host_ip = ips[0] 
        if not (app.config.get("TB") in [ None, "" ]): 
        # if setup icap then compare the first domain is the same 
            for ip in ips: 
                if ip.split('.')[0] == app.config.get("TB").split('.')[0]: 
                    host_ip = ip 
        app.config["HOST"] = host_ip

    logging.info('Update HOST to {}'.format(host_ip))

    # Register iCAP
    logging.info("Initial iCAP register...")
    init_for_icap()
    register_mqtt_event()
    # Running webapi sever
    logging.info("Running webapi server...")
    socketio.run(app, host = "0.0.0.0", port=args.port, debug=False)

if __name__ == '__main__':
    # Create log
    config_logger('./app.log', 'w', "info")
    args = build_argparser().parse_args()
    sys.exit(main(args) or 0)