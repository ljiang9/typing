# typing — 终端打字速度测试

显示一句话，你照着打字，回车后给出速度（WPM）与正确率。纯标准库，纯本地运行。

## 安装

无需安装，Python 3.10+ 直接运行：

```bash
cd typing
python3 -m typing
```

## 用法

```bash
python3 -m typing                 # 中文句子，打一轮
python3 -m typing --lang en       # 英文句子
python3 -m typing --rounds 3      # 打三轮，取平均
python3 -m typing --seed 42       # 固定句子顺序（演示/测试）
python3 -m typing --json          # JSON 输出
```

## 计分说明

- **WPM**：按行业标准 `(字符数 / 5) / 分钟数` 计算。注意这是"标准词"（5 字符 = 1 词），不是真实单词数。
- **正确率**：字符级逐位置对比，正确字符数 / max(目标长度, 输入长度)。多打或少打的字都算错。

## 局限（诚实说明）

- 按"行"计时：从句子显示到你按回车为止，没有逐键实时计时。
- WPM 的"5 字符 = 1 词"是行业惯例，中文按字数算，跨语言对比意义不大。
- 内置句子是自写简单句，不是标准测试题库。

## License

MIT
