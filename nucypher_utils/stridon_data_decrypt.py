import os
import json
from binascii import unhexlify
import datetime

import maya
import msgpack
from umbral import keys

from django.conf import settings
from stridon_app.models import Article  # for testing only

from nucypher.characters.lawful import Enrico as Enrico
from nucypher.crypto.powers import SigningPower
from nucypher.network.middleware import RestMiddleware
from nucypher.crypto import kits
from nucypher.config.characters import AliceConfiguration, BobConfiguration


article_instance = Article.objects.all()[0]
username = article_instance.author.username

DATASOURCE_FILENAME = f"\
{article_instance.author.username}-\
{article_instance.title}-\
datasource-pubkey.msgpack"


DATA_SOURCE_DIR = os.path.join(
    settings.BASE_DIR,
    'nucypher_utils',
    'nucypher_data',
)


with open(
    os.path.join(
        DATA_SOURCE_DIR, DATASOURCE_FILENAME
    ),
    "rb"
) as file:
    data = msgpack.load(file)

data_source_public_key = data[b'data_source_public_key']

cipher_text = data[b'kits']

POLICY_FILENAME = "policy-metadata.json"

POLICY_FILE = os.path.join(
    settings.BASE_DIR,
    'nucypher_utils',
    'nucypher_data',
    POLICY_FILENAME,
)

with open(POLICY_FILE, 'r') as f:
    policy_pubkey_data = json.load(f)


policy_pubkey_string = policy_pubkey_data['policy_pubkey']

policy_pubkey_bytes = unhexlify(policy_pubkey_string)
policy_pubkey = keys.UmbralPublicKey.from_bytes(policy_pubkey_bytes)

enrico_as_understood_by_bob = Enrico.from_public_keys(
    {SigningPower: data_source_public_key},
    policy_encrypting_key=policy_pubkey,
)

# ALICE_PUBKEY_FILE = os.path.join(
#     settings.BASE_DIR,
#     'nucypher_utils',
#     'nucypher_data',
#     'alice_pubkey.json',
# )

# with open(ALICE_PUBKEY_FILE, 'r') as fp:
#     alice_pubkey_json = json.load(fp)

ALICE_CONFIG_DIR = os.path.join(
    settings.BASE_DIR,
    'nucypher_utils',
    'nucypher_data',
    'nucypher_char_configs',
    'stridon-demo-alice')

ALICE_CONFIG_FILE = os.path.join(
    ALICE_CONFIG_DIR,
    "alice.config"
)

passphrase = "TEST_ALICE_PASSWORD"

new_alice_config = AliceConfiguration.from_configuration_file(
        filepath=ALICE_CONFIG_FILE,
        network_middleware=RestMiddleware(),
        start_learning_now=False,
        save_metadata=False,
    )
new_alice_config.keyring.unlock(password=passphrase)

alice = new_alice_config()

alice.start_learning_loop(now=True)

alice_pubkey = keys.UmbralPublicKey.from_bytes(bytes(alice.stamp))

# SEEDNODE_URL = 'localhost:11501'

# ursula = Ursula.from_seed_and_stake_info(
#     seed_uri=SEEDNODE_URL,
#     federated_only=True,
#     minimum_stake=0
# )

# premium_user = Bob(
#     known_nodes=[ursula],
#     network_middleware=RestMiddleware(),
#     federated_only=True,
#     start_learning_now=True,
#     learn_on_same_thread=True
# )
BOB_CONFIG_DIR = os.path.join(
        settings.BASE_DIR,
        'nucypher_utils',
        'nucypher_data',
        'nucypher_char_configs',
        username)

BOB_CONFIG_FILE = os.path.join(
    BOB_CONFIG_DIR,
    "bob.config"
)

new_premium_user = BobConfiguration.from_configuration_file(
    filepath=BOB_CONFIG_FILE,
    network_middleware=RestMiddleware(),
    start_learning_now=False,
    save_metadata=False,
)

new_premium_user.keyring.unlock(password=passphrase)
premium_user = new_premium_user()

policy_end_datetime = maya.now() + datetime.timedelta(days=5)

label = b'stridon-premium-service'

cipher_kit = kits.UmbralMessageKit.from_bytes(cipher_text)

from nucypher.crypto.powers import SigningPower, DecryptingPower
print("ALICE")
print(alice.public_keys(SigningPower))
print(alice.public_keys(DecryptingPower))
print("PREMIUM_USER")
print(premium_user.public_keys(SigningPower))
print(premium_user.public_keys(DecryptingPower))

# delivered_cleartexts = premium_user.retrieve(
#     message_kit=cipher_kit,
#     data_source=enrico_as_understood_by_bob,
#     alice_verifying_key=alice_pubkey,
#     label=label
# )


