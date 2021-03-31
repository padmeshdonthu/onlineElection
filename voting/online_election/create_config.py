import configparser


class CreateConfigParse:

    def add_keys(self):
        config = configparser.ConfigParser()
        config['AWSEducateKeys'] = {'access_key_id': 'ASIAZE7J44S65KWNXVH7',
                                    'secret_access_key': '2qsaVkQLW/UIc0uvLoe0xcvK9+nEeEPdzAVveMlc',
                                    'session_token': 'FwoGZXIvYXdzECsaDJwngepeV9xODmpejCK/AXnsoReEDOR3Vcss4Hw14ZuFxmbxr0fb3in5WGs62jhlauoJfyGwN2XGNjWgsIUQfOJWTXb7iYyMIf+/SOktRXv+UFIH/PdhO7qzhmyfKWheDDFURXQvV9BegL2nEsl7JW+ULg29sLNqeUfqM2twUfflDAgdxNzCNK+n8Laj6Hf+BjmbYj9kpEvtNWkY2vaJcLFgD2jpxbc1Er+WvJcuTyPhbQnrcigYDn85U7YOt2uNvBhTTCkIc61mbiyA9zlSKM2piIMGMi1uNcig7TeMgcZ2X5lj8F1SlgCmdE47ws/DWEYtbxqkMwP+rBxK2l6Qq7aJav8=',
                                    'region_name': 'us-east-1'
                                    }
        with open('.awskeys.ini', 'w') as configfile:
            config.write(configfile)
        return True
