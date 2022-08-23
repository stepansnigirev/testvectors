import subprocess
import signal
import pytest
import shutil
import time
import os
from util.rpc import BitcoinRPC

DATADIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), "blockchain")
RPCUSER = "liquid"
RPCPASSWORD = "secret"
RPCPORT = 18998
PORT = 18999
CMD = f"elementsd -datadir={DATADIR} -chain=liquidregtest \
        -rpcuser={RPCUSER} -rpcpassword={RPCPASSWORD} -rpcport={RPCPORT} -port={PORT} \
        -fallbackfee=0.0000001 -validatepegin=0 -initialfreecoins=2100000000000000"

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

@pytest.fixture(scope="module", autouse=True)
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
    try:
        rpc = BitcoinRPC(user=RPCUSER, password=RPCPASSWORD, port=RPCPORT)
        for i in range(10):
            try: # checking if elements is loaded already
                rpc.getblockchaininfo()
            except:
                time.sleep(0.2)
        get_coins(rpc)
        yield rpc
        # stop elementsd
    finally:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)  # Send the signal to all the process groups
    # cleanup
    for i in range(10):
        try:
            shutil.rmtree(DATADIR)
            return
        except Exception as e:
            time.sleep(1)
