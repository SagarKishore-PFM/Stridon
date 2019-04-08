import json
import os
from umbral import keys
from binascii import unhexlify
import msgpack
from django.conf import settings
from nucypher.characters.lawful import Enrico


def encrypt_data(plain_text, datasource_filename):
    POLICY_FILENAME = "policy-metadata.json"

    POLICY_FILE = os.path.join(
        settings.BASE_DIR,
        'nucypher_utils',
        'nucypher_data',
        POLICY_FILENAME,
    )

    with open(POLICY_FILE, 'rb') as fp:
        policy_pubkey_data = json.load(fp)

    policy_pubkey_string = policy_pubkey_data['policy_pubkey']

    policy_pubkey_bytes = unhexlify(policy_pubkey_string)
    policy_pubkey = keys.UmbralPublicKey.from_bytes(policy_pubkey_bytes)

    data_source = Enrico(
        policy_encrypting_key=policy_pubkey
    )

    data_source_public_key = bytes(data_source.stamp)

    plain_text = bytes(plain_text, 'utf-8')
    message_kit, _signature = data_source.encrypt_message(plain_text)
    kit_bytes = message_kit.to_bytes()
    kit = kit_bytes
    data = {
            'data_source_public_key': data_source_public_key,
            'kits': kit,
    }

    # data souce pub key naming convention:
    # author_name-article_title-article_id-datasource-pubkey.msgpack

    DATA_SOURCE_DIR = os.path.join(
        settings.BASE_DIR,
        'nucypher_utils',
        'nucypher_data',
    )

    DATA_SOURCE_FILE_NAME = datasource_filename

    with open(
        os.path.join(
            DATA_SOURCE_DIR, DATA_SOURCE_FILE_NAME
        ),
        "wb"
    ) as file:
        msgpack.dump(data, file, use_bin_type=True)

    return kit_bytes
