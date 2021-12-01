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

Bitcoin Core compatible descriptors:

- receiving: `wpkh([9d120b19/84h/1h/0h]tpubDDHwnxhUYnzyuar2JNLsHgKhthSHQfJcEMLZkSXmm8GxzLuSXX2vwcDZXEa2GZ4MEe25pMrQ1NH8c2FM2G3FV3QXuWUc8iT2GhwyRahb7ze/0/*)`
- change: `wpkh([9d120b19/84h/1h/0h]tpubDDHwnxhUYnzyuar2JNLsHgKhthSHQfJcEMLZkSXmm8GxzLuSXX2vwcDZXEa2GZ4MEe25pMrQ1NH8c2FM2G3FV3QXuWUc8iT2GhwyRahb7ze/1/*)`

Combined blinded descriptor (supported only by embit-based projects like Specter-Desktop and Specter-DIY):

```
blinded(slip77(L24LLSbccJ52ESXkRvnKxYik3iBJvH2uQHf6X3xnsKZ3sw8RHMmA),wpkh([9d120b19/84h/1h/0h]tpubDDHwnxhUYnzyuar2JNLsHgKhthSHQfJcEMLZkSXmm8GxzLuSXX2vwcDZXEa2GZ4MEe25pMrQ1NH8c2FM2G3FV3QXuWUc8iT2GhwyRahb7ze/{0,1}/*))
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

## Multisig 2-of-3

Mnemonics:
- `aim aim aim aim aim aim aim aim aim aim aim aim`
- `bus bus bus bus bus bus bus bus bus bus bus bus`
- `cave cave cave cave cave cave cave cave cave cave cave cave`

All on regtest.

### Blinding key

Blidning key is generated on external wallet and passed when the wallet is registered on the device.

Master blinding key: `L1XvKmnKWuC4a5sbz3Ez6LCfMCbaXMBCcQk7C62ziN5NjoEgjN5N`

Master blinding key in hex: `80b796c76c895bda151cd5c40f3a11afcd96d66f99347a760d3f7b8aaa5815b5`

### Addresses

Bitcoin Core compatible descriptors:

- receiving: `wsh(sortedmulti(2,[9d120b19/48h/1h/0h/2h]tpubDDxAoxVrJU3Vgk1PbNDWth2And1m6EyiR6MgzGsq5S3MGCZaHdN34tX4ZRGEFRZUZELgPhuy9gQTp2myUbyfuYbmFoLwgauovh5gbzHghwR/0/*,[42b01983/48h/1h/0h/2h]tpubDFjEjEPeyFun6FHqS248kK51SwLVx3hVzWdAFwsDXza1Lfjy1KASoBhMiiJMqtJTUAPdM7zbrx3BNgYMQNyGNVwkyNS1Wi82bb2Hwij7K9L/0/*,[9860e1eb/48h/1h/0h/2h]tpubDESXi1fi17YeJJA7xAn5sqHPvEBFpPscRv9QEzJpJQw4D7QfAWw8xfXuGdW1wMQvdj9vz8SxCSTVdhcS4Sro5GYdMojR2JYE3GuHBWipnxy/0/*))`
- change: `wsh(sortedmulti(2,[9d120b19/48h/1h/0h/2h]tpubDDxAoxVrJU3Vgk1PbNDWth2And1m6EyiR6MgzGsq5S3MGCZaHdN34tX4ZRGEFRZUZELgPhuy9gQTp2myUbyfuYbmFoLwgauovh5gbzHghwR/1/*,[42b01983/48h/1h/0h/2h]tpubDFjEjEPeyFun6FHqS248kK51SwLVx3hVzWdAFwsDXza1Lfjy1KASoBhMiiJMqtJTUAPdM7zbrx3BNgYMQNyGNVwkyNS1Wi82bb2Hwij7K9L/1/*,[9860e1eb/48h/1h/0h/2h]tpubDESXi1fi17YeJJA7xAn5sqHPvEBFpPscRv9QEzJpJQw4D7QfAWw8xfXuGdW1wMQvdj9vz8SxCSTVdhcS4Sro5GYdMojR2JYE3GuHBWipnxy/1/*))`

Combined blinded descriptor (supported only by embit-based projects like Specter-Desktop and Specter-DIY):

```
blinded(slip77(L1XvKmnKWuC4a5sbz3Ez6LCfMCbaXMBCcQk7C62ziN5NjoEgjN5N),wsh(sortedmulti(2,[9d120b19/48h/1h/0h/2h]tpubDDxAoxVrJU3Vgk1PbNDWth2And1m6EyiR6MgzGsq5S3MGCZaHdN34tX4ZRGEFRZUZELgPhuy9gQTp2myUbyfuYbmFoLwgauovh5gbzHghwR/{0,1}/*,[42b01983/48h/1h/0h/2h]tpubDFjEjEPeyFun6FHqS248kK51SwLVx3hVzWdAFwsDXza1Lfjy1KASoBhMiiJMqtJTUAPdM7zbrx3BNgYMQNyGNVwkyNS1Wi82bb2Hwij7K9L/{0,1}/*,[9860e1eb/48h/1h/0h/2h]tpubDESXi1fi17YeJJA7xAn5sqHPvEBFpPscRv9QEzJpJQw4D7QfAWw8xfXuGdW1wMQvdj9vz8SxCSTVdhcS4Sro5GYdMojR2JYE3GuHBWipnxy/{0,1}/*)))
```


First receving addresses:

| # | Confidential | Unconfidential |
|---|--------------|----------------|
| 0 | `el1qq0n9xlnd4xt8ffk509s7zq4ddvn3647rlw0tzxl0pym790wchzcy895cq3z4sd70wpp8vfwa38n43ad3tncavfnvsgl8cth8840u9wzxrhj80nfnrxx8` | `ert1qj6vqg32cxl8hqsnkyhwcne6c7kc4euwkyekgy0nu9mnn6h7zhprqwy5uu0` |
| 1 | `el1qqvqwnkt9tuv8rcd2zhm6xysrv6qu6fgrmtv7yzcwmvytrfuwwk3gfm0k6d2hav8up9dmwjxnz4hn7ez8qk364wr99nnh56gkrzkn7ts977h7vqlznvtj` | `ert1qahmdx4t7kr7qjkahfrf32melv3rstga2hpjjeem6dytp3tfl9czsmctrq9` |
| 2 | `el1qqg3h9950kk9m0lqan0y3fctqgdvlhql2qkjc6usyn7jsy2f0rvzh0mlfvyt58fl8vt5dd4z6l2s6q4knz6wj0km0f3un2lx8dtxfxvkxnrrpe7a76cpk` | `ert1qal5kz96r5lnk96xk63d04gdq2mf3d8f8mdh5c7f40nrk4nynxtrqpqeqwc` |
| 3 | `el1qqgsjchy4g277srz3gh7hwwx9ez43zrf5lrjmwwp9qhemymx39k3uw00cju9zhaqqsy24u6g4xq46c6lq2ekvcjsr7hnckl5klrsdr6ape4f9z049t9kg` | `ert1q8hufwz3t7sqgz927dy2nq2avd0s9vmxvfgplteut06t03cx3awssu27wn4` |
| 4 | `el1qqvhmu34xdpzuumxguu75t7h6nwua20sj52avz7t4es80r890rtkewspqagzvtkc5t9wz6x838k739h848kkdu9a5mnlsmvmw8fvmc8lyf6ytzylx8cdg` | `ert1qgqsw5px9mv29jhpdrrcnm0gjmn6nmtx7z76delcdkdhr5kdurljq7w56ev` |

### Transactions

#### Fully confidential transaction

Example of PSBT transaction sent for signing:

Inputs:
- `10000000` of `LBTC` on my regtest (they are different in different regtests)
- `100000000` of `9a8351bdde7dea6bd61ec10caccdda411744ee50e25eee86bb9d6cfffe0a0c93` asset
Outputs:
- `30000000` of `9a8351bdde7dea6bd61ec10caccdda411744ee50e25eee86bb9d6cfffe0a0c93` to `el1qqw5v247uc9mnfmg2zhzjkdu67uxm8z42dj7zlqmqxd89e7n9ytjdfsgyhgudfqe8mj5hjq258x9py8dg9gqfcskval2jk7rdc`
- Change `70000000` of `9a8351bdde7dea6bd61ec10caccdda411744ee50e25eee86bb9d6cfffe0a0c93` to `el1qqtqxy5dev2yevmt3fcswpsv2nle6tzzk04gvrw843aszgqj2xh8frlvfvjf6pav2uk2eg025ud2ly4mxqe6l5v83l6vplkc0w2lrr98j96wscjw3qvke`
- LBTC change of `999961` to `el1qqvzw2wc5lqlp2hhjvstdgkswf5n0h7yaysanj6z6czcg84f250mxpx0a6sgq9cqwpya9ytvlfrwhn38gg3hwagtftlm8m4hplz859mrnlsypd8f6kfqs`
- Fee `390` sat

Base64 PSET:

[data/multi_confidential.txt](data/multi_confidential.txt)

Json form of the same transaction with all the fields:

[data/multi_confidential.json](data/multi_confidential.json)

Hashes for signing **without rangeproofs**:

```
0 : 1a16541c3b7f36104aaf23f673e7db2e6a8000c28cf71e06e0abb48dc9c26d95
1 : 90a30c7ff77ec47dec52e201102f780d08425eb32dbf9beec1296e72c46ddf61
```

**Signed transactions only contain 1 signature from `aim` mnemonic.**

Singed transaction:

[data/multi_confidential_signed.txt](data/multi_confidential_signed.txt)

Signed in json format:

[data/multi_confidential_signed.json](data/multi_confidential_signed.json)

Hashes for signing **with rangeproofs**:

```
0 : d97220b36c17490ed039bdf9990e6824a15a30a2262785b5767f085323f89611
1 : 770bd41d23afa8efe45649628d08f05212f6b51773d7c70a0b4ad6802a82ccbe
```

Singed transaction:

[data/multi_confidential_signed_rangeproof.txt](data/multi_confidential_signed_rangeproof.txt)

Signed in json format:

[data/multi_confidential_signed_rangeproof.json](data/multi_confidential_signed_rangeproof.json)