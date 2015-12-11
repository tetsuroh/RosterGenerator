# RosterGenerator
遺伝的アルゴリズムを使って勤務表を生成する

シフト制の勤務表を条件にしたがって生成します。

最大連続勤務日数、今日と明日で必ずセットになるようなシフト(たとえば夜勤）などが設定できます。

エクセル形式での出力にopenpyxlを使っています https://openpyxl.readthedocs.org

## 使い方
```
$ python main.py
```
