# testvectors

## Private keys

Recovery phrases (generated with [`gen_mnemonics.py`](gen_mnemonics.py)):
- `aim aim aim aim aim aim aim aim aim aim aim aim`
- `bus bus bus bus bus bus bus bus bus bus bus bus`
- `cave cave cave cave cave cave cave cave cave cave cave cave`

For single-sig first mnemonic is used. For 2-of-3 multisig - all three are used in `sortedmulti` descriptor.

Default derivation paths:
- `m/84h/1h/0h` for single sig segwit (`wpkh(A)`)
- `m/48h/1h/0h/2h` for multisig segwit (`wsh(sortedmulti(A,B,C))`)

## Test vectors

- Liquid-specific test vectors: [liquid](./liquid/) folder
- Bitcoin