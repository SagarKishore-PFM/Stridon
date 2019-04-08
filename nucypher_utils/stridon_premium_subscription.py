import os
import datetime
# import json
# from binascii import unhexlify

# from umbral import keys
import maya
from twisted.logger import globalLogPublisher
from django.conf import settings

from nucypher.utilities.logging import SimpleObserver
from nucypher.characters.lawful import Ursula
from nucypher.network.middleware import RestMiddleware
from nucypher.config.characters import AliceConfiguration
from nucypher.config.characters import BobConfiguration


def subscribe_and_grant_permission_to(username):
    globalLogPublisher.addObserver(SimpleObserver())

    # Reinitialize Alice from our config file

    ALICE_CONFIG_DIR = os.path.join(
        settings.BASE_DIR,
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

    # Now onto Bob

    SEEDNODE_URL = 'localhost:11501'

    PREMIUM_USERS_DIR = os.path.join(
        settings.BASE_DIR,
        'nucypher_utils',
        'nucypher_data',
        'premium_members_files',
        username)

    ursula = Ursula.from_seed_and_stake_info(
        seed_uri=SEEDNODE_URL,
        federated_only=True,
        minimum_stake=0
    )

    bob_config = BobConfiguration(
        config_root=os.path.join(PREMIUM_USERS_DIR),
        is_me=True,
        known_nodes={ursula},
        start_learning_now=False,
        federated_only=True,
        learn_on_same_thread=True,
    )

    bob_config.initialize(password=passphrase)
    bob_config.keyring.unlock(password=passphrase)
    bob_config_file = bob_config.to_configuration_file()

    premium_user = bob_config.produce()
    policy_end_datetime = maya.now() + datetime.timedelta(days=5)

    label = b'stridon-premium-service'

    policy_pubkey = alice.get_policy_pubkey_from_label(label)

    policy = alice.grant(
        bob=premium_user,
        label=label,
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
