import threading
import sys
import os
from os import environ
import logging
import hashlib
import pysftp
from flask import Flask, jsonify, request
from tqdm import tqdm

logging.basicConfig(level=logging.INFO, stream=sys.stdout, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)s %(levelname)s [%(module)-s] [%(name)s] %(funcName)s() %(message)s')
logger = logging.getLogger()

manifest_file_string = 'manifest_file_string'
remote_host = environ.get('remote_host', 'some_host')
ssh_user = environ.get('ssh_user', 'some_user')
ssh_key = environ.get('ssh_key', 'some_key')
whoami = environ.get('whoami', 'it_is_koren_ms')
config_dict = {'remote_host': remote_host, 'ssh_user': ssh_user, 'ssh_key': ssh_key}


class Progressbar(tqdm):
    def update_to(self, gathered: int, total: int):
        self.total = total
        self.update(gathered - self.n)


def file_zipping(l_path=None, zipping=None):
    if not l_path:
        logger.info('did not provide a path/filename.gz for zipping instructions')
        return
    if zipping not in ['zip', 'unzip']:
        logger.info('unknown zipping instructions (zip or unzip)')
        return
    files = os.listdir(l_path)
    os.chdir(l_path)
    if zipping == 'zip':
        logger.info('zip actions here as needed...')
        os.chdir('../')
    if zipping == 'unziping':
        try:
            for f in files:
                if 'gz' not in f:
                    logger.info('{} not a .gz file, will not try to unzip it...'.format(f))
                    continue
                logger.info('unzipping {}/{}'.format(l_path, f))
                os.system('gunzip --keep ' + f)
            os.chdir('../')
        except Exception as ex:
            os.chdir('../')
            logger.info('could not unzip, error: {}'.format(ex))


def remove_local_files(l_path):
    files = os.listdir(l_path)
    for f in files:
        logger.info('removing {}/{} from local disk'.format(l_path, f))
        os.remove('{}/{}'.format(l_path, f))


def validate_checksum(l_path, file, checksums_file):
    md5_check = hashlib.md5()
    # fast hashing to also support huge files
    with open('{}/{}'.format(l_path, file), "rb") as bigfile:
        for chunk in iter(lambda: bigfile.read(5), b""):
            md5_check.update(chunk)
    for c_line in checksums_file:
        file_name = c_line['file_name']
        file_checksum = c_line['file_checksum']
        if file == file_name:
            logger.info('validating {} md5 checksum...'.format(file))
            if md5_check.hexdigest() == file_checksum:
                logger.info('md5 checksum {} for {} is valid...'.format(file_checksum, file))
                return True
            else:
                logger.info('checksum {} for {} is wrong md5 checksum/hash'.format(file_checksum, file))
                return False


app = Flask(__name__)


@app.route('/health', methods=['GET'])
def health():
    print('wait and analyze')
    return 'i am {} and i am alive'.format(whoami)


@app.route('/config', methods=['GET'])
def config():
    request_info = request.args
    print('wait and debug break here', request_info)
    return jsonify(config_dict)


@app.route('/action', methods=['GET'])
def action():
    params = {}
    message = 'no-action'
    status = 'ok'
    try:
        params = request.args
        if not params:
            status = 'error'
            message = 'missing parameters or bad request method (read api documentation)'
    except Exception as ex:
        status = 'error'
        message = '{}, missing parameters or bad request method (read api documentation)'.format(ex)
    direction = params.get('direction', None)
    if not direction:
        status = 'error'
        message = 'missing direction parameter (read api documentation)'
    elif direction not in 'directions':
        status = 'error'
        message = 'unknown direction parameter (read api documentation)'
    else:
        message = 'connecting from scp file server, validating checksums, unzipping..'
        logger.info('\ndownloading from scp file server, validating checksums, unzipping..\n')

        def long_running_task():
            file_zipping('local_path', 'zip')
            conn = pysftp.Connection(remote_host, username=ssh_user, private_key=ssh_key)
            remove_local_files('local_path')

            thread = threading.Thread(target=long_running_task)
            thread.start()
    res = {'status': status, 'message': message}
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
