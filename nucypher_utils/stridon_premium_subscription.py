import os
import datetime
# import json
# from binascii import unhexlify

# from umbral import keys
import maya
from twisted.logger import globalLogPublisher
from django.conf import settings

from nucypher.utilities.logging import SimpleObserver
from nucypher.characters.lawful import Ursula, Bob
from nucypher.network.middleware import RestMiddleware
from nucypher.config.characters import AliceConfiguration


def subscribe_and_grant_permission_to(username):
    globalLogPublisher.addObserver(SimpleObserver())

    # Reinitialize Alice from our config file

    TEMP_ALICE_DIR = os.path.join('/', 'tmp', 'stridon-demo-alice')

    SEEDNODE_URL = 'localhost:11500'

    ursula2 = Ursula.from_seed_and_stake_info(
        seed_uri=SEEDNODE_URL,
        federated_only=True,
        minimum_stake=0
    )

    passphrase = "TEST_ALICE_PASSWORD"

    alice_config = AliceConfiguration(
        config_root=os.path.join(TEMP_ALICE_DIR),
        is_me=True,
        known_nodes={ursula2},
        start_learning_now=False,
        federated_only=True,
        learn_on_same_thread=True,
    )

    alice_config.initialize(password=passphrase)
    alice_config.keyring.unlock(password=passphrase)

    alice = alice_config.produce()
    alice.start_learning_loop(now=True)

    # Now onto Bob

    SEEDNODE_URL = 'localhost:11501'

    PREMIUM_USERS_DIR = os.path.join(
        settings.BASE_DIR,
        'nucypher_utils',
        'nucypher_data',
        'premium_members_files')

    ursula = Ursula.from_seed_and_stake_info(
        seed_uri=SEEDNODE_URL,
        federated_only=True,
        minimum_stake=0
    )

    premium_user = Bob(
        known_nodes=[ursula],
        network_middleware=RestMiddleware(),
        federated_only=True,
        start_learning_now=True,
        learn_on_same_thread=True
    )

    policy_end_datetime = maya.now() + datetime.timedelta(days=5)

    label = b'stridon-premium-service'

    policy_pubkey = alice.get_policy_pubkey_from_label(label)

    # POLICY_FILENAME = "policy-metadata.json"
    # POLICY_FILE = os.path.join(
    #     settings.BASE_DIR,
    #     'nucypher_utils',
    #     'nucypher_data',
    #     POLICY_FILENAME,
    # )
    # policy_json = {
    #     "policy_pubkey": policy_pubkey.to_bytes().hex(),
    # }

    # with open(POLICY_FILE, 'w') as f:
    #     json.dump(policy_json, f)

    policy = alice.grant(
        premium_user,
        label,
        m=1,
        n=1,
        expiration=policy_end_datetime
    )

    assert policy.public_key == policy_pubkey
    alices_pubkey_bytes = bytes(alice.stamp)

    premium_user.join_policy(label, alices_pubkey_bytes)

    PREMIUM_USER_FILENAME = f"{username}.json"
    PREMIUM_USER_FILE = os.path.join(
        PREMIUM_USERS_DIR,
        PREMIUM_USER_FILENAME,
    )

    with open(PREMIUM_USER_FILE, 'w') as fp:
        fp.write('aaa')

    return policy.public_key == policy_pubkey


def revoke_permission_from(username):

    PREMIUM_USERS_DIR = os.path.join(
        settings.BASE_DIR,
        'nucypher_utils',
        'nucypher_data',
        'premium_members_files')

    PREMIUM_USER_FILENAME = f"{username}.json"
    PREMIUM_USER_FILE = os.path.join(
        PREMIUM_USERS_DIR,
        PREMIUM_USER_FILENAME,
    )

    os.remove(PREMIUM_USER_FILE)
    return not os.path.exists(PREMIUM_USER_FILE)
