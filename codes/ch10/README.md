# 第 10 章：打包与校验

```bash
python pack.py ../../plugins/hello hello-1.0.0.zip
python verify.py hello-1.0.0.zip
```

`pack.py` 按路径排序、固定时间戳，保证同样的输入得到同样的包。包里附带 `SHA256SUMS.txt`，`verify.py` 逐个文件比对。

签名部分书中只讲流程，真实项目用 Ed25519 或 RSA，标准库不提供，需要 OpenSSL 之类的库。
