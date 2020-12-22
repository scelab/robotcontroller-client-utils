# robotcontroller-client-utils
Sota (CommU) を遠隔操作するための便利クラス・関数のセットです。

- client.py: Sota(CommU)内部で動作しているRobotControllerと通信するためのクラスを含むモジュールです。
- jtalk.py: OpenJTalkを用いて音声合成を行う関数を含むモジュールです。
- posedef.py: ポーズを定義しているモジュールです。
- robot.py: Sota(CommU)を操作するためのクラスを含むモジュールです。client, jtalk, posedefモジュールを用いています。

Sota (CommU)を動かすプログラムを作る時は、上記のモジュールにあるクラスや関数を使うと便利です。
使い方の例はrobot.pyの中にあります。
