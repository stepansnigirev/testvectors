from embit import bip32, bip39
from embit.liquid.networks import get_network
from embit.liquid import slip77
from embit.descriptor.checksum import add_checksum
from embit.descriptor import Descriptor
from embit.liquid.pset import PSET
from embit.liquid.finalizer import finalize_psbt
from embit.liquid.transaction import LSIGHASH as SIGHASH
import random

# liquid regtest can have any name except main, test, regtest, liquidv1 and liquidtestnet
NET = get_network("liquidregtest")

MNEMONIC = "glory promote mansion idle axis finger extra february uncover one trip resource lawn turtle enact monster seven myth punch hobby comfort wild raise skin"
SEED = bip39.mnemonic_to_seed(MNEMONIC)
ROOTKEY = bip32.HDKey.from_seed(SEED, version=NET["xprv"])
FGP = ROOTKEY.my_fingerprint.hex() # fingerprint for derivation
MBK = slip77.master_blinding_from_seed(SEED) # master blinding key

# some random cosigner xpubs
SEEDS = [bytes([i]*32) for i in range(1,5)]
COSIGNERS = [bip32.HDKey.from_seed(seed, version=NET["xprv"]) for seed in SEEDS]

# uncomment more lines to add more sighashes
ALL_SIGHASHES = [SIGHASH.ALL, SIGHASH.NONE, SIGHASH.SINGLE]
# ALL_SIGHASHES = ALL_SIGHASHES + [sh | SIGHASH.ANYONECANPAY for sh in ALL_SIGHASHES]
# ALL_SIGHASHES = ALL_SIGHASHES + [sh | SIGHASH.RANGEPROOF for sh in ALL_SIGHASHES]

def sign_psbt(psbt:str, root=ROOTKEY):
    """Replace with your tested functionality"""
    psbt = PSET.from_string(psbt)
    psbt.sign_with(root, sighash=None) # tell embit to sign with whatever sighash is provided
    return str(psbt)

############

def random_wallet_name():
    return "test"+random.randint(0,0xFFFFFFFF).to_bytes(4,'big').hex()

def create_wallet(erpc, d1, d2, mbk=MBK):
    wname = random_wallet_name()
    # to derive addresses
    desc1 = Descriptor.from_string(d1)
    desc2 = Descriptor.from_string(d2)
    # to add checksums
    d1 = add_checksum(str(d1))
    d2 = add_checksum(str(d2))
    erpc.createwallet(wname, True, True, "", False, True, False)
    w = erpc.wallet(wname)
    res = w.importdescriptors([{
            "desc": d1,
            "active": True,
            "internal": False,
            "timestamp": "now",
            "range": 20,
        },{
            "desc": d2,
            "active": True,
            "internal": True,
            "timestamp": "now",
            "range": 20,
        }])
    assert all([k["success"] for k in res])
    w.importmasterblindingkey(mbk.secret.hex())
    # detect addr type as Bitcoin Core is stupid
    if desc1.is_wrapped:
        w.addr_type = "p2sh-segwit"
    elif desc1.is_legacy:
        w.addr_type = "legacy"
    else:
        w.addr_type = "bech32"
    return w

def fund_wallet(erpc, w, amount=1, confidential=True):
    addr = w.getnewaddress("", w.addr_type)
    if not confidential:
        addr = w.getaddressinfo(addr)["unconfidential"]
    wdefault = erpc.wallet()
    wdefault.sendtoaddress(addr, amount)
    wdefault.mine(1)

def inject_sighash(psbt, sighash):
    psbt = PSET.from_string(psbt)
    for inp in psbt.inputs:
        inp.sighash_type = sighash
    return str(psbt)

def create_psbt(erpc, w, amount=0.1, destination=None, confidential=True, confidential_change=True, sighash=None):
    wdefault = erpc.wallet()
    if not destination:
        destination = wdefault.getnewaddress()
    change = w.getrawchangeaddress(w.addr_type)
    if not confidential:
        destination = w.getaddressinfo(destination)["unconfidential"]
    if not confidential_change:
        change = w.getaddressinfo(change)["unconfidential"]
    psbt = w.walletcreatefundedpsbt([], [{destination: amount}], 0, {"includeWatching": True, "changeAddress": change, "fee_rate": 1}, True)
    unblinded = psbt["psbt"]
    try:
        blinded = w.blindpsbt(unblinded)
    except:
        try:
            blinded = w.walletprocesspsbt(unblinded)['psbt']
        except:
            blinded = None
    # inject sighash for all inputs
    if sighash is not None:
        unblinded = inject_sighash(unblinded, sighash)
        if blinded:
            blinded = inject_sighash(blinded, sighash)
    return unblinded, blinded

def check_psbt(erpc, unsigned, signed, sighash=None):
    if sighash:
        psbt = PSET.from_string(signed)
        for inp in psbt.inputs:
            for sig in inp.partial_sigs.values():
                assert sig[-1] == sighash
    combined = erpc.combinepsbt([unsigned, signed])
    final = erpc.finalizepsbt(combined)
    if final["complete"]:
        raw = final["hex"]
    else: # finalize in elements is buggy, may not finalize
        tx = finalize_psbt(PSET.from_string(combined))
        assert tx is not None
        raw = str(tx)
    # test accept
    assert erpc.testmempoolaccept([raw])[0]["allowed"]

def bulk_check(erpc, descriptors):
    w = create_wallet(erpc, *descriptors)
    fund_wallet(erpc, w, 10, confidential=True)
    for sh in ALL_SIGHASHES:
        unblinded, blinded = create_psbt(erpc, w, sighash=sh)
        # blinding may fail if all inputs and outputs are confidential, so fund_wallet will return None in blinded
        unsigned = blinded or unblinded
        signed = sign_psbt(unsigned)
        check_psbt(erpc, unsigned, signed, sighash=sh)
    # test all confidential-unconfidential pairs
    for conf_input in [True, False]:
        w = create_wallet(erpc, *descriptors)
        fund_wallet(erpc, w, 10, confidential=conf_input)
        for conf_destination in [True, False]:
            unblinded, blinded = create_psbt(erpc, w, confidential=conf_destination)
            # blinding may fail if all inputs and outputs are confidential, so fund_wallet will return None in blinded
            unsigned = blinded or unblinded
            signed = sign_psbt(unsigned)
            check_psbt(erpc, unsigned, signed)

##########################

def test_wpkh(erpc):
    derivation = "84h/1h/0h"
    xpub = ROOTKEY.derive(f"m/{derivation}").to_public()
    # change and receive descriptors
    descriptors = (
        f"wpkh([{FGP}/{derivation}]{xpub}/0/*)",
        f"wpkh([{FGP}/{derivation}]{xpub}/1/*)"
    )
    bulk_check(erpc, descriptors)

def test_sh_wpkh(erpc):
    derivation = "49h/1h/0h"
    xpub = ROOTKEY.derive(f"m/{derivation}").to_public()
    # change and receive descriptors
    descriptors = (
        f"sh(wpkh([{FGP}/{derivation}]{xpub}/0/*))",
        f"sh(wpkh([{FGP}/{derivation}]{xpub}/1/*))"
    )
    bulk_check(erpc, descriptors)

def test_pkh(erpc):
    derivation = "44h/1h/0h"
    xpub = ROOTKEY.derive(f"m/{derivation}").to_public()
    # change and receive descriptors
    descriptors = (
        f"pkh([{FGP}/{derivation}]{xpub}/0/*)",
        f"pkh([{FGP}/{derivation}]{xpub}/1/*)"
    )
    bulk_check(erpc, descriptors)

def test_wsh(erpc):
    # 1-of-2 multisig
    derivation = "48h/1h/0h/2h"
    xpub = ROOTKEY.derive(f"m/{derivation}").to_public()
    cosigner = COSIGNERS[0].derive(f"m/{derivation}").to_public()
    # change and receive descriptors
    descriptors = (
        f"wsh(sortedmulti(1,[12345678/{derivation}]{cosigner},[{FGP}/{derivation}]{xpub}/0/*))",
        f"wsh(sortedmulti(1,[12345678/{derivation}]{cosigner},[{FGP}/{derivation}]{xpub}/1/*))"
    )
    bulk_check(erpc, descriptors)

def test_sh_wsh(erpc):
    # 1-of-2 multisig
    derivation = "48h/1h/0h/1h"
    xpub = ROOTKEY.derive(f"m/{derivation}").to_public()
    cosigner = COSIGNERS[0].derive(f"m/{derivation}").to_public()
    # change and receive descriptors
    descriptors = (
        f"sh(wsh(sortedmulti(1,[12345678/{derivation}]{cosigner},[{FGP}/{derivation}]{xpub}/0/*)))",
        f"sh(wsh(sortedmulti(1,[12345678/{derivation}]{cosigner},[{FGP}/{derivation}]{xpub}/1/*)))"
    )
    bulk_check(erpc, descriptors)

def test_sh(erpc):
    # 1-of-2 multisig
    derivation = "45h"
    xpub = ROOTKEY.derive(f"m/{derivation}").to_public()
    cosigner = COSIGNERS[0].derive(f"m/{derivation}").to_public()
    # change and receive descriptors
    descriptors = (
        f"sh(sortedmulti(1,[12345678/{derivation}]{cosigner},[{FGP}/{derivation}]{xpub}/0/*))",
        f"sh(sortedmulti(1,[12345678/{derivation}]{cosigner},[{FGP}/{derivation}]{xpub}/1/*))"
    )
    bulk_check(erpc, descriptors)
