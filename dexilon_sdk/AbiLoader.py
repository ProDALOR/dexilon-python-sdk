import os
import json

sdk_dir = os.path.dirname(__file__)


def load_abi(filename: str) -> dict:
    with open(os.path.join(sdk_dir, 'blockchain_abi', filename)) as f:
        return json.load(f)


class AbiLoader:

    bridge = load_abi('bridge_abi.json')
    usdt = load_abi('usdt_abi.json')
