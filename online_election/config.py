import configparser


class ConfigParse:

    def fetch_keys(self):
        config = configparser.ConfigParser()
        config.read('.awskeys.ini')
        sections = config.sections()
        if 'AWSEducateKeys' in sections:
            keys = {}
            access_key_id = config['AWSEducateKeys']['access_key_id']
            secret_access_key = config['AWSEducateKeys']['secret_access_key']
            session_token = config['AWSEducateKeys']['session_token']
            region_name = config['AWSEducateKeys']['region_name']
            keys['access_key_id'] = access_key_id
            keys['secret_access_key'] = secret_access_key
            keys['session_token'] = session_token
            keys['region_name'] = region_name
            return keys
