# Blinding keys test vectors

Requirements: `embit` (`pip3 install -r requirements.txt`)

use `blinding_key.py` script like this:

```sh
python3 blinding_key.py "aim aim aim aim aim aim aim aim aim aim aim aim" "00148320611ff032223c1f4bb1fbbd2291fd2b3f43d9"
```

Output:
```
Root key: xprv9s21ZrQH143K4J3ivVfLX8GZtDZhHJ1qHfJEvFr6zdzrXRNppYzpG5kfaEGLm3x3tq98v3k1SW5RCQHoP9oXP1TsdL35apbwsE9JrpeQd94
Master blinding key: 905cfe33a3dfb37db513d1078c16bcfdf906ecd944c5ddd37fdfbcc5e619c141
Blinding key for script 00148320611ff032223c1f4bb1fbbd2291fd2b3f43d9: 13f8a9a5f79f93e77546ac073db19ab9506eefe2af871c2fab0ed382f1bdd53a
Unconfidential address: ex1qsvsxz8lsxg3rc86tk8am6g53l54n7s7ezrcagj
Confidential address: lq1qq08y67ffhm7ktpkk8lw7mu2zktyw5m2j3k9eyj5fgaeeek3g29zrdqeqvy0lqv3z8s05hv0mh53frlft8apajw5m4m3mtgwfx
```
