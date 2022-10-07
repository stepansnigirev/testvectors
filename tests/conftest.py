import subprocess
import signal
import pytest
import shutil
import time
import os
import json
from collections import OrderedDict
from util.rpc import BitcoinRPC

DATADIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "blockchain")
RPCUSER = "liquid"
RPCPASSWORD = "secret"
RPCPORT = 18998
PORT = 18999
ELEMETSD = os.environ.get("ELEMETSD_CMD", default="elementsd")
CMD = f"{ELEMETSD} -datadir={DATADIR} -chain=liquidregtest \
        -rpcuser={RPCUSER} -rpcpassword={RPCPASSWORD} -rpcport={RPCPORT} -port={PORT} \
        -fallbackfee=0.0000001 -validatepegin=0 -initialfreecoins=2100000000000000"

TEST_DATA_FILE = os.environ.get("TEST_DATA_FILE", default="test_data.json")

def get_coins(rpc):
    # create default wallet if doesn't exist
    if "" not in rpc.listwallets():
        rpc.createwallet("")
    w = rpc.wallet("")
    # get free coins
    w.rescanblockchain()
    w.mine(10)
    balance = w.getbalance()
    addr = w.getnewaddress()
    # send half to our own address to make them confidential
    w.sendtoaddress(addr, balance["bitcoin"]//2)
    w.mine(1)
    # generate some reissueable asset
    w.issueasset(10000, 1)
    w.mine(1)
    assert w.getbalance().get("bitcoin", 0) > 0

@pytest.fixture(scope="function", autouse=True)
def erpc():
    """Starts elementsd and gives back rpc instance to work with"""
    # create datadir for elements
    if os.path.isdir(DATADIR):
        shutil.rmtree(DATADIR)
    os.makedirs(DATADIR)
    # start elementsd
    proc = subprocess.Popen(CMD,
                            stdout=subprocess.PIPE,
                            shell=True, preexec_fn=os.setsid)
    time.sleep(2)
    try:
        rpc = BitcoinRPC(user=RPCUSER, password=RPCPASSWORD, port=RPCPORT)
        for i in range(100):
            try: # checking if elements is loaded already
                rpc.getblockchaininfo()
            except:
                time.sleep(0.2)
        get_coins(rpc)
        yield rpc
        # stop elementsd
    finally:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # Send the signal to all the process groups
        time.sleep(2)
    # cleanup
    for i in range(100):
        try:
            shutil.rmtree(DATADIR)
            time.sleep(2)
            return
        except Exception as e:
            time.sleep(1)

class TestDataCollector(object):
    """Collects test tata and dumps it to JSON file"""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.data = OrderedDict()
        self.skip = True

    def define_suite(
        self,
        kind: str,
        name: str,
        mbk: str,
        policy_map: str,
        keys_info: list,
        description: str = ""
    ) -> None:
        self.skip = False
        self.kind = kind
        self.suite = name

        if kind not in self.data:
            self.data[kind] = OrderedDict()

        if name in self.data[kind]:
            suite = self.data[kind][name]
            if (
                suite["description"] != description or
                suite["mbk"] != mbk or
                suite["policy_map"] != policy_map or
                suite["keys_info"] != keys_info
            ):
                raise ValueError("unequal parameters for existing test suite")
            return

        self.data[kind][name] = OrderedDict({
            "description": description,
            "mbk": mbk,
            "policy_map": policy_map,
            "keys_info": keys_info,
            "tests": list()
        })

    def skip_suite(self) -> None:
        self.skip = True

    def add_test(
        self,
        pset: str,
        signatures: dict,
        sighash: int = None,
        description: str = ""
    ) -> None:
        if self.skip:
            return

        test = OrderedDict({
            "description": description,
            "pset": pset,
            "signatures": signatures,
            "sighash": sighash
        })

        try:
            self.data[self.kind][self.suite]["tests"].append(test)
        except KeyError:
            raise RuntimeError("test suite not properly defined")

    def dump(self):
        try:
            os.remove(self.filename)
        except OSError:
            pass
        with open(self.filename, "w") as write_file:
            json.dump(self.data, write_file, indent=2)

@pytest.fixture(scope="module", autouse=True)
def collector():
    """Creates and provides test data collector"""

    collector_obj = TestDataCollector(TEST_DATA_FILE)
    yield collector_obj
    collector_obj.dump()
