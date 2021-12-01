from embit import bip39, bip32, compact
from embit.liquid import slip77
from embit.liquid import networks
from embit.liquid.descriptor import LDescriptor
from embit.psbt import *
from embit.liquid.pset import *
import sys, json

MNEMONIC = "aim aim aim aim aim aim aim aim aim aim aim aim"
DERIVATION = "m/84h/1h/0h"
NETWORK = networks.get_network("elementsregtest")

def jsonify_field(key, value, value_parsed=None):
    o = {
        "key": key.hex(),
        "value": value.hex() if value is not None else None
    }
    if value_parsed is not None:
        o["value_parsed"] = value_parsed
    return o

class JSONLInputScope(LInputScope):
    def to_json(self, version=None):
        obj = {}
        # bitcoin fields
        obj["non_witness_utxo"] = jsonify_field(b"\x00", self.non_witness_utxo.serialize() if self.non_witness_utxo is not None else None)
        obj["witness_utxo"] = jsonify_field(b"\x01", self.witness_utxo.serialize() if self.witness_utxo is not None else None)
        obj["partial_sigs"] = []
        for pub in self.partial_sigs:
            obj["partial_sigs"].append(jsonify_field(b"\x02" + pub.serialize(), self.partial_sigs[pub]))
        obj["sighash_type"] = jsonify_field(b"\x03", self.sighash_type.to_bytes(4, "little") if self.sighash_type is not None else None, self.sighash_type)
        obj["redeem_script"] = jsonify_field(b"\x04", self.redeem_script.data if self.redeem_script else None)
        obj["witness_script"] = jsonify_field(b"\x05", self.witness_script.data if self.witness_script else None)
        obj["bip32_derivations"] = []
        for pub in self.bip32_derivations:
            obj["bip32_derivations"].append(jsonify_field(b"\x06" + pub.serialize(), self.bip32_derivations[pub].serialize()))
        obj["final_scriptsig"] = jsonify_field(b"\x07", self.final_scriptsig.data if self.final_scriptsig else None)
        obj["final_scriptwitness"] = jsonify_field(b"\x08", self.final_scriptwitness.data if self.final_scriptwitness else None)
        if version == 2:
            obj["txid"] = jsonify_field(b"\x0e", bytes(reversed(self.txid)))
            obj["vout"] = jsonify_field(b"\x0f", self.vout.to_bytes(4, 'little'), self.vout)
            obj["sequence"] = jsonify_field(b"\x10", self.sequence.to_bytes(4, 'little'), self.sequence)
        obj["unknown"] = []
        # unknown
        for key in self.unknown:
            obj["unknown"].append(jsonify_field(key, self.unknown[key]))

        # liquid-specific keys
        obj["value"] = jsonify_field(b'\xfc\x08elements\x00', self.value.to_bytes(8, 'little') if self.value is not None else None, self.value)
        obj["value_blinding_factor"] = jsonify_field(b'\xfc\x08elements\x01', self.value_blinding_factor)
        obj["asset"] = jsonify_field(b'\xfc\x08elements\x02', self.asset)
        obj["asset_blinding_factor"] = jsonify_field(b'\xfc\x08elements\x02', self.asset_blinding_factor)
        obj["range_proof"] = jsonify_field(b'\xfc\x04pset\x0e', self.range_proof)
        return obj

class JSONLOutputScope(LOutputScope):
    def to_json(self, version=None):
        obj = {}
        # bitcoin fields
        obj["redeem_script"] = jsonify_field(b"\x00", self.redeem_script.data if self.redeem_script else None)
        obj["witness_script"] = jsonify_field(b"\x01", self.witness_script.data if self.witness_script else None)
        obj["bip32_derivations"] = []
        for pub in self.bip32_derivations:
            obj["bip32_derivations"].append(jsonify_field(b"\x02" + pub.serialize(), self.bip32_derivations[pub].serialize()))
        if version == 2:
            obj["value"] = jsonify_field(b"\x03", self.value.to_bytes(8, 'little'), self.value)
            obj["script_pubkey"] = jsonify_field(b"\x04", self.script_pubkey.data if self.script_pubkey is not None else None)
        # unknown
        obj["unknown"] = []
        for key in self.unknown:
            obj["unknown"].append(jsonify_field(key, self.unknown[key]))
        # liquid-specific keys
        if version == 2:
            obj["asset"] = jsonify_field(b'\xfc\x04pset\x02', self.asset)
        if version == 2:
            obj["value_commitment"] = jsonify_field(b'\xfc\x04pset\x01', self.value_commitment)
        else:
            obj["value_commitment"] = jsonify_field(b'\xfc\x08elements\x00', self.value_commitment)
        obj["value_blinding_factor"] = jsonify_field(b'\xfc\x08elements\x01', self.value_blinding_factor)
        if version == 2:
            obj["asset_commitment"] = jsonify_field(b'\xfc\x04pset\x03', self.asset_commitment)
        else:
            obj["asset_commitment"] = jsonify_field(b'\xfc\x08elements\x02', self.asset_commitment)
        obj["asset_blinding_factor"] = jsonify_field(b'\xfc\x08elements\x03', self.asset_blinding_factor)
        if version == 2:
            obj["blinding_pubkey"] = jsonify_field(b'\xfc\x04pset\x06', self.blinding_pubkey)
        else:
            obj["blinding_pubkey"] = jsonify_field(b'\xfc\x08elements\x06', self.blinding_pubkey)
        if version == 2:
            obj["ecdh_pubkey"] = jsonify_field(b'\xfc\x04pset\x07', self.ecdh_pubkey)
        else:
            obj["ecdh_pubkey"] = jsonify_field(b'\xfc\x08elements\x07', self.ecdh_pubkey)

        if version == 2:
            obj["range_proof"] = jsonify_field(b'\xfc\x04pset\x04', self.range_proof)
        else:
            obj["range_proof"] = jsonify_field(b'\xfc\x08elements\x04', self.range_proof)
        if version == 2:
            obj["surjection_proof"] = jsonify_field(b'\xfc\x04pset\x05', self.surjection_proof)
        else:
            obj["surjection_proof"] = jsonify_field(b'\xfc\x08elements\x05', self.surjection_proof)
        obj["blinder_index"] = jsonify_field(b'\xfc\x04pset\x08', self.blinder_index.to_bytes(4, 'little') if self.blinder_index is not None else None, self.blinder_index)
        obj["value_proof"] = jsonify_field(b'\xfc\x04pset\x09', self.value_proof)
        obj["asset_proof"] = jsonify_field(b'\xfc\x04pset\x0a', self.asset_proof)
        return obj

class JSONPSET(PSET):
    PSBTIN_CLS = JSONLInputScope
    PSBTOUT_CLS = JSONLOutputScope
    def to_json(self):
        res = {}
        # magic bytes
        res["magic"] = self.MAGIC.hex()
        # global scope
        res["global"] = {}
        obj = res["global"]
        if self.version != 2:
            # unsigned tx flag
            obj["global_tx"] = {
                "key": "00",
                "value": self.tx.serialize().hex()
            }
        obj["xpubs"] = []
        # xpubs
        for xpub in self.xpubs:
            obj["xpubs"].append({
                "key": (b"\x01" + xpub.serialize()).hex(),
                "value": self.xpubs[xpub].serialize().hex()
            })

        if self.version == 2:
            obj["tx_version"] = {
                "key": "02",
                "value": self.tx_version.to_bytes(4, 'little').hex() if self.tx_version is not None else None,
                "parsed_value": self.tx_version
            }
            obj["locktime"] = {
                "key": "03",
                "value": self.locktime.to_bytes(4, 'little').hex() if self.locktime is not None else None,
                "parsed_value": self.locktime
            }
            obj["num_inputs"] = {
                "key": "04",
                "value": compact.to_bytes(len(self.inputs)).hex(),
                "parsed_value": len(self.inputs)
            }
            obj["num_outputs"] = {
                "key": "05",
                "value": compact.to_bytes(len(self.outputs)).hex(),
                "parsed_value": len(self.outputs)
            }
            obj["psbt_version"] = {
                "key": "fb",
                "value": self.version.to_bytes(4, 'little').hex(),
                "parsed_value": self.version if self.version is not None else None
            }
        # unknown
        obj["unknown"] = []
        for key in self.unknown:
            obj["unknown"].append({
                "key": key.hex(),
                "value": self.unknown[key].hex()    
            })
        # inputs
        res["inputs"] = []
        for inp in self.inputs:
            res["inputs"].append(inp.to_json(version=self.version))
        # outputs
        res["outputs"] = []
        for out in self.outputs:
            res["outputs"].append(out.to_json(version=self.version))
        return res

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} path/to/base64_psbt.txt [path/to/output.json]")
        sys.exit(1)

    with open(sys.argv[1], "r") as f:
        pset = JSONPSET.from_string(f.read())
    
    r = json.dumps(pset.to_json(), indent=2)
    print(r)
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "w") as f:
            f.write(r)