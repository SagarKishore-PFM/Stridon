import json
import os
from umbral import keys
from binascii import unhexlify

from django.conf import settings
# from ..stridon_app.models import Article
from stridon_app.models import Article
from nucypher.characters.lawful import Enrico

### NOTE!!!!!
### NOT YET WORKING!!!!!!!!!!!
###
def encrypt_data(plain_text):
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
            'data_source': data_source_public_key,
            'kits': kit,
    }

# umbral.keys.wrap_key(policy_pubkey)

# message_source = bytes(article.title, 'utf-8')


# pt = msgpack.dumps(enc_req, use_bin_type=True)
# message_kit = data_source.encrypt_message(pt)

# pt = bytes(article.title, 'utf-8')

#####
# article_data = {
#     'title': article.title,
#     'content': article.content,
#     'is_premium_content': article.is_premium_content,
# }

# plain_text = msgpack.dumps(article_data, use_bin_type=True)
# message_kit = data_source.encrypt_message(plain_text)
# data = {
#     'data_source_pubkey': data_source_public_key,
#     'message_kit': message_kit,
# }
