import configparser


class ConfigParse:

    def fetch_keys(self):
        config = configparser.ConfigParser()
        config.read('~/.aws/credentials')
        sections = config.sections()
        if 'default' in sections:
            keys = {}
            access_key_id = config['default']['access_key_id']
            secret_access_key = config['default']['secret_access_key']
            session_token = config['default']['session_token']
            keys['access_key_id'] = access_key_id
            keys['secret_access_key'] = secret_access_key
            keys['session_token'] = session_token
            keys['region_name'] = "us-east-1"
            return keys
