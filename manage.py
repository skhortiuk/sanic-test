import argparse

from service_api.app import app

parser = argparse.ArgumentParser()
parser.add_argument('--host',
                    help='Setup host ip to listen up, default to 0.0.0.0',
                    default='0.0.0.0')
parser.add_argument('--port', help='Setup port to attach, default to 8008',
                    default='8008')
parser.add_argument('--workers', help='Setup workers to run, default to 1',
                    type=int, default=1)
parser.add_argument('--debug', help='Enable or disable debugging')
args = parser.parse_args()

if __name__ == '__main__':
    app.run(
        host=args.host,
        port=args.port,
        workers=args.workers,
        debug=args.debug,
    )
