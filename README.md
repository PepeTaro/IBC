# Identity-based cryptography(IBC) デモ

## 特徴
* Type 1 pairingを使用したIBCデモ。(つまりSupersingular)
* 楕円曲線はE/F_{q}:y^2 = x^3 + 1の形で固定している。
* PairingはModified Weil pairingを使用。

## 注意
* 32ビット Debian GNU/Linux 11 (bullseye)上でのみ動作確認済み。
* ユニットテストしていない部分あり。
* ハッシュ関数H2でTrace mapを使用しているがセキュリティが高いのか否かはわからない、ただCollision Free。

### デモ
```sh
cd demo
python3 demo.py
```

### テスト
```sh
python3 -m unittest tests/test_*.py
```

#### 参考文献
* Lawrence C. Washington.Elliptic Curves Number Theory and Cryptography, Second Edition
* J.H. Silverman, Jill Pipher, Jeffrey Hoffstein.An Introduction to Mathematical Cryptography
* Craig Costello.Pairings for beginners.https://static1.squarespace.com/static/5fdbb09f31d71c1227082339/t/5ff394720493bd28278889c6/1609798774687/PairingsForBeginners.pdf
* Ben Lynn.ON THE IMPLEMENTATION OF PAIRING-BASED CRYPTOSYSTEMS.https://crypto.stanford.edu/pbc/thesis.pdf
* R. W. Mak.Identity-based encryption using supersingular curves with the Weil pairing.https://fse.studenttheses.ub.rug.nl/12902/1/Thesis-1.pdf
