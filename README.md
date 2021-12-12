修論実験用リポジトリ
====

グラフ構造を考慮したWord2VecやDock2Vecでの学習

## 機能

### D2Vクラス
* executeメソッド(@staticmethod)
- Doc2Vec学習モデルを生成
- libs/dock2vecs.py

### W2Vクラス
* executeメソッド(@staticmethod)
- Word2Vec学習モデルを生成
- libs/word2vecs.py

### Dockerfileクラス
- Dockerfileをナイーブに解析するオブジェクトを生成
- libs/dockerfiles.py

### Graphクラス
- グラフ構造を表現
- 追加予定機能
    - 命令列の後ろを考慮した構造の表現
- libs/graphs.py

### Primitiveクラス
- Dockerfileをprimitiveに解析
- 既存のインデントを用いて, 命令列ないの単語の重要度を表現
- libs/primitives.py

### Structureクラス
- toStackメソッド(@staticmethod)
-  インデントを考慮して階層構造を表現, 実装
- スタックを利用
- libs/structures.py



## モデル
### libs/delv/default-test-2021-12-05 01:45:27.835636.model
- binnacle-icse202を全て学習させたモデル


## 結果
### naiveなデータでの学習
* Dockerfileにあるレイヤごとの命令を配列として学習
- 入力データが"apt-get"と"install"だった時の結果
    ```bash
        (('+', 0.9916801452636719)
        ('{}', 0.9910140037536621)
        ('-not', 0.9847615957260132)
        ('*tkinter*', 0.9843180179595947)
        ('-executable', 0.9811577200889587)
        ('/usr/local', 0.9765851497650146)
        ('find', 0.9741872549057007)
        ('-exec', 0.9539327621459961)
        ('*.a', 0.9269841909408569)
        ('d', 0.9113402366638184))
    ```

### 前の命令+単語の重要度などを考慮したデータでの学習(少しグラフ構造)
* Dockerfile内のインデントを単語の重要度の尺度として利用
- 入力データが"apt-get"と"install"だった時の結果
    ```bash
        (('update', 0.9994246959686279)
        ('-y', 0.9989630579948425)
        ('--no-install-recommends', 0.9984796047210693)
        ('pkg-config', 0.9965482950210571)
        ('libc6-dev', 0.9931356906890869)
        ('git', 0.9850125312805176)
        ('--no-install-suggests', 0.9848350882530212)
        ('g++', 0.9822943210601807)
        ('build-essential', 0.9681098461151123))
    ```

### 前と後の命令+単語の重要度などを考慮したデータでの学習(少しグラフ構造)
* Dockerfile内のインデントを単語の重要度の尺度として利用
- 入力データが"apt-get"と"install"だった時の結果
    ```bash
        (('update', 0.9975267052650452)
        ('--no-install-recommends', 0.9973561763763428)
        ('-y', 0.9940279722213745)
        ('libc6-dev', 0.9882516264915466)
        ('pkg-config', 0.9873135089874268)  
        ('--no-install-suggests', 0.9772453904151917)
        ('g++', 0.976104736328125)
        ('ca-certificates', 0.961370587348938)
        ('gcc', 0.9584934711456299)
        ('dnf', 0.9575251340866089))
    ```

### インデントを考慮した記述の変換
* スタックを利用, インデントの構造をスタックに積んでいき, POPが行われるタイミングなどでオブジェクトのコピーを行う
- 変換例
    ```bash
        ----------------------------変換前----------------------------
        COPY scripts/sccache.sh /scripts/
        RUN set -ex; \
            \
            find /usr/local -depth \
                \( \
                    \( -type d -a \( -name test -o -name tests -o -name idle_test \) \) \
                    -o \
                    \( -type f -a \( -name '*.pyc' -o -name '*.pyo' \) \) \
                \) -exec rm -rf '{}' +; \
            rm -f get-pip.py
        
        ----------------------------変換後----------------------------
        ["COPY", "scripts/sccache.sh", "/scripts/"],
        ["RUN", "set", "-ex", "AND", "BACK"],
        ["RUN", "find", "/usr/local", "-depth"],
        ["RUN", "find", "/usr/local", "-depth", "-type", "d", "-a", "-name", "test", "-o", "-name", "tests",,,],
        ["RUN", "find", "/usr/local", "-depth", "-type", "d", "-a", "-name", "*.pyc",,,,],
        ["RUN", "rm", "-rf", "get-pip.py"]

    ```

### ファイルパスとレイヤ番号の情報を学習データに付与, Doc2Vecのタグとして利用
* 後で記述
- 付与例
    ```bash
        $FILE_PATH = "./debian-binnacle-icse2020/243133876.Dockerfile"

        FROM debian:buster-slim
        ENV PATH /usr/local/bin:$PATH
        ENV LANG C.UTF-8
        RUN set -eux; \
            apt-get update; \
            apt-get install -y --no-install-recommends \
                ca-certificates \
                netbase \
                tzdata \
            ; \
            rm -rf /var/lib/apt/lists/*
        ENV GPG_KEY E3FF2839C048B25C084DEBE9B26995E310250568
        ENV PYTHON_VERSION 3.9.7

    ```

    ```python
        {
            Hash("./debian-binnacle-icse2020/243133876.Dockerfile/0/0"): 
            [
                "FROM",
                "debian:buster-slim"
            ],
            ...
            Hash("./debian-binnacle-icse2020/243133876.Dockerfile/3/3"):
            [
                "apt-get",
                "install",
                "-y",
                "--no-install-recommends",
                "ca-certificates",
                "AND",
                "BACK"
            ] 
            ...
        }
    ```
