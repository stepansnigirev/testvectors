# Liquid-specific test vectors

## Single-sig

Mnemonic: `aim aim aim aim aim aim aim aim aim aim aim aim`.

All on regtest.

### Blinding key

Blidning key is generated according to [slip77](https://github.com/satoshilabs/slips/blob/master/slip-0077.md)

Implementation: [embit/liquid/slip77.py](https://github.com/diybitcoinhardware/embit/blob/master/src/embit/liquid/slip77.py)

Seed: `eb592e6b1c53b02506a5413be14c5ebc9b4a02f5eebcbedd33d1377942880c01e3b8b3a50878e0ec9a731646ed3380823487024bf83e993330868189ee54084b`

Master blinding key: `L24LLSbccJ52ESXkRvnKxYik3iBJvH2uQHf6X3xnsKZ3sw8RHMmA`

Master blinding key in hex: `905cfe33a3dfb37db513d1078c16bcfdf906ecd944c5ddd37fdfbcc5e619c141`

### Addresses

Account key at path `m/84h/1h/0h`: `tprv8gbueYfEQRKK27pEQigGtGfbKfvMFL7hf3jnTvVULrUa9refu8DLm7bhM5ePtD8mWV3axvg3j4JbJhU3qKmSH2mf6MXP1RrpRu4AWFbDKSG`

Xpub at path `m/84h/1h/0h`: `tpubDDHwnxhUYnzyuar2JNLsHgKhthSHQfJcEMLZkSXmm8GxzLuSXX2vwcDZXEa2GZ4MEe25pMrQ1NH8c2FM2G3FV3QXuWUc8iT2GhwyRahb7ze`

Single-key descriptors:

- receiving: `wpkh(tpubDDHwnxhUYnzyuar2JNLsHgKhthSHQfJcEMLZkSXmm8GxzLuSXX2vwcDZXEa2GZ4MEe25pMrQ1NH8c2FM2G3FV3QXuWUc8iT2GhwyRahb7ze/0/*)`
- change: `wpkh(tpubDDHwnxhUYnzyuar2JNLsHgKhthSHQfJcEMLZkSXmm8GxzLuSXX2vwcDZXEa2GZ4MEe25pMrQ1NH8c2FM2G3FV3QXuWUc8iT2GhwyRahb7ze/1/*)`

Combined blinded descriptor (supported only by embit-based projects like Specter-Desktop and Specter-DIY):

```
blinded(slip77(L24LLSbccJ52ESXkRvnKxYik3iBJvH2uQHf6X3xnsKZ3sw8RHMmA),wpkh(tpubDDHwnxhUYnzyuar2JNLsHgKhthSHQfJcEMLZkSXmm8GxzLuSXX2vwcDZXEa2GZ4MEe25pMrQ1NH8c2FM2G3FV3QXuWUc8iT2GhwyRahb7ze/{0,1}/*))
```

First receving addresses:

| # | Confidential | Unconfidential |
|---|--------------|----------------|
| 0 | `el1qq2nr7tzx5kud6vj46zp5uu3uf3pqgegl9cmfxvlmdtv828l0amhu927dkt5f4xuu04nr8wegakqtwgn4l4kjqp8fsnkwyzp5y` | `ert1q40xm96y6nww86e3nhv5wmq9hyf6l6mfqv3pmtj` |
| 1 | `el1qq0drtearcqfktv4wxc0ym5n3nydad8gca8xt2qalrvmncwsr6cmvvf7mnm2j5crwkyc9uq76e6zpy0drmnh8v4g8gsg39mjl4` | `ert1qyldea4f2vphtzvz7q0dvapqj8k3aemnk3a45df` |
| 2 | `el1qqflluphnplgjakqq4unfdt6p0drcmdphs72wr6deaed0tzngmlgfe2dyacpv4pd3cez5yt9kmh8f50urwr4gkeukw2qkuwjsq` | `ert1q4xjwuqk2skcuv32z9jmdmn5687php65tvn7f4x` |
| 3 | `el1qqwpzdtw0gk9j8femv2rm0mtgwtks67zj08r99g0f9ncjq3c5ha7ue42wcqn0fsqkauemzygaxfmy0ru6hpz47y9pgslphclpc` | `ert1q648vqfh5cqtw7va3zywnyaj837dts32lfzl358` |
| 4 | `el1qqwcgfp2fv29al7rhm2fv9wqvt5t7l6pds9zd26dup3m3hwkhjmalamacph2zhzszxwt0keg4wgtnv5afw9ayu9jzv9sz7ng8r` | `ert1qa7uqm4pt3gpr89hmv52hy9ek2w5hz7jwgfqyk2` |

### Transactions

#### Fully confidential transaction

Transactions are parsed with [`parse_pset.py`](parse_pset.py) script. I hope I didn't mess it up.

Example of PSBT transaction sent for signing:

Inputs:
- `10000000` of `LBTC` on my regtest (they are different in different regtests)
- `100000000` of `9a8351bdde7dea6bd61ec10caccdda411744ee50e25eee86bb9d6cfffe0a0c93` asset
Outputs:
- `30000000` of `9a8351bdde7dea6bd61ec10caccdda411744ee50e25eee86bb9d6cfffe0a0c93` to `el1qqw5v247uc9mnfmg2zhzjkdu67uxm8z42dj7zlqmqxd89e7n9ytjdfsgyhgudfqe8mj5hjq258x9py8dg9gqfcskval2jk7rdc`
- Change `70000000` of `9a8351bdde7dea6bd61ec10caccdda411744ee50e25eee86bb9d6cfffe0a0c93` to `el1qq2jdl6uyzrv6p4n3d3yhpx58tlemnqq7rzrc5g8t5nu5tqs92cf9d25fyk04vrh2lhku8vfe3sa8puz3aenvwngdfhyk0la73`
- LBTC change of `9999624` to `el1qqgmznjj8a0rps0ysnqvvn6z6m7e36l653wgn4hk44u2zkn9lwlw8c5kpdaqatkrz808vam0qd993j5xtn9p9qv4ddve36yn9t`
- Fee `376` sat

Base64 PSET:

[data/single_confidential.txt](data/single_confidential.txt)

Json form of the same transaction with all the fields:

[data/single_confidential.json](data/single_confidential.json)

Hashes for signing **without rangeproofs**:

```
0 : c1a68d391684a0993320ce137f68189a032493438bb5a4175177b1a6272741b5
1 : af553c55ff4dbe6fd5999b3116fe42e2ae1dd49360cd3e6edb03bbf961c6be68
```

Singed transaction:

[data/single_confidential_signed.txt](data/single_confidential_signed.txt)

Signed in json format:

[data/single_confidential_signed.json](data/single_confidential_signed.json)

Hashes for signing **with rangeproofs**:

```
0 : 238bf1650f1c1f35c653baad9125b439bf4c41dec22fc074b454db9a9412b803
1 : 4b2dd1899b632fb9494aa21f5cc65310bd98482531e0513c0eaaca641dbd3fe8
```

Singed transaction:

[data/single_confidential_signed_rangeproof.txt](data/single_confidential_signed_rangeproof.txt)

Signed in json format:

[data/single_confidential_signed_rangeproof.json](data/single_confidential_signed_rangeproof.json)
