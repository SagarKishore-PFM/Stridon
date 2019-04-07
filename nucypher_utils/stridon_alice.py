import os
import json
import shutil

from twisted.logger import globalLogPublisher

from nucypher.characters.lawful import Ursula
from nucypher.utilities.logging import SimpleObserver
from nucypher.config.characters import AliceConfiguration


def initialize_alice_policy_pubkey(
        alice_encryption_password: str = "TEST_ALICE_PASSWORD"):

    """
    Takes in alice's encryption password as input and generates and
    stores the policy pubkey.
    """

    globalLogPublisher.addObserver(SimpleObserver())

    TEMP_ALICE_DIR = os.path.join('/', 'tmp', 'stridon-demo-alice')

    # We expect the url of the seednode as the first argument.
    SEEDNODE_URL = 'localhost:11500'

    POLICY_FILENAME = "policy-metadata.json"

    shutil.rmtree(TEMP_ALICE_DIR, ignore_errors=True)

    ursula = Ursula.from_seed_and_stake_info(
        seed_uri=SEEDNODE_URL,
        federated_only=True,
        minimum_stake=0
    )

    passphrase = alice_encryption_password

    alice_config = AliceConfiguration(
        config_root=os.path.join(TEMP_ALICE_DIR),
        is_me=True,
        known_nodes={ursula},
        start_learning_now=False,
        federated_only=True,
        learn_on_same_thread=True,
    )

    alice_config.initialize(password=passphrase)
    alice_config.keyring.unlock(password=passphrase)
    alice_config_file = alice_config.to_configuration_file()

    alice = alice_config.produce()
    label = "stridon-premium-service"
    label = label.encode()

    policy_pubkey = alice.get_policy_pubkey_from_label(label)

    print("The policy public key for label '{}' is {}".format(
        label.decode("utf-8"),
        policy_pubkey.to_bytes().hex()
        )
    )

    policy_json = {
        "policy_pubkey": policy_pubkey.to_bytes().hex(),
    }

    POLICY_FILE = os.path.join(
        os.getcwd(),
        'nucypher_utils',
        'nucypher_data',
        POLICY_FILENAME,
    )

    with open(POLICY_FILE, 'w') as f:
        json.dump(policy_json, f)
