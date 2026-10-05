"""typing - 终端打字速度测试。

显示一句话，你照着打，回车后给出 WPM（每分钟词数）与正确率。
WPM 按行业标准计算：(字符数 / 5) / 分钟数。
纯标准库，纯本地。
"""

import argparse
import json
import random
import sys
import time

# 自写简单句子（原创，无版权问题）
SENTENCES_EN = [
    "The quick brown fox jumps over the lazy dog.",
    "Pack my box with five dozen liquor jugs.",
    "How vexingly quick daft zebras jump.",
    "The five boxing wizards jump quickly.",
    "Weave a circle round him thrice.",
    "A very bad quack might jinx zippy fowls.",
    "Big fjords vex quick waltz nymph.",
    "Jaded zombies acted quaintly but kept driving their oxen forward.",
    "The job requires extra pluck and zeal from every young wage earner.",
    "We promptly judged antique ivory buckles for the next prize.",
    "Amazingly few discotheques provide jukeboxes.",
    "Heavy boxes perform quick waltzes and jigs.",
    "Jack quietly moved the big zebra over the fence.",
    "The wizard quickly jinxed the gnomes before they vaporized.",
    "Sphinx of black quartz, judge my vow.",
    "Two driven jocks help fax my big quiz.",
    "Five quacking zephyrs jolt my wax bed.",
    "The jay, pig, fox, zebra and my wolves quack.",
    "Blowzy night-frumps vex'd Jack Q.",
    "Quizzical twins proved my hijack-bug fix.",
    "Practice makes perfect, so keep typing every day.",
    "A journey of a thousand miles begins with a single step.",
    "Slow and steady wins the race.",
    "The early bird catches the worm.",
    "Actions speak louder than words.",
    "Where there is a will, there is a way.",
    "Time waits for no one.",
    "Better late than never.",
    "Do not count your chickens before they hatch.",
    "Every cloud has a silver lining.",
]

SENTENCES_ZH = [
    "今天天气很好，适合出去散步。",
    "读书使人明智，实践使人进步。",
    "一寸光阴一寸金，寸金难买寸光阴。",
    "千里之行，始于足下。",
    "学而不思则罔，思而不学则殆。",
    "工欲善其事，必先利其器。",
    "纸上得来终觉浅，绝知此事要躬行。",
    "山重水复疑无路，柳暗花明又一村。",
    "不积跬步，无以至千里。",
    "业精于勤，荒于嬉；行成于思，毁于随。",
    "春眠不觉晓，处处闻啼鸟。",
    "白日依山尽，黄河入海流。",
    "举头望明月，低头思故乡。",
    "海内存知己，天涯若比邻。",
    "会当凌绝顶，一览众山小。",
    "长风破浪会有时，直挂云帆济沧海。",
    "路漫漫其修远兮，吾将上下而求索。",
    "天行健，君子以自强不息。",
    "己所不欲，勿施于人。",
    "三人行，必有我师焉。",
]


def calc_wpm(chars, seconds):
    """标准 WPM = (字符数 / 5) / 分钟数。"""
    if seconds <= 0:
        return 0.0
    return (chars / 5.0) / (seconds / 60.0)


def calc_accuracy(target, typed):
    """字符级正确率：逐位置对比，正确数 / max(目标长度, 输入长度)。"""
    if not target and not typed:
        return 100.0
    correct = sum(1 for a, b in zip(target, typed) if a == b)
    total = max(len(target), len(typed))
    return correct / total * 100.0


def pick_sentence(lang, rng):
    if lang == "zh":
        return rng.choice(SENTENCES_ZH)
    return rng.choice(SENTENCES_EN)


def play_round(target, get_input):
    print()
    print("请照着输入下面这句话：")
    print("  " + target)
    start = time.monotonic()
    typed = get_input()
    elapsed = time.monotonic() - start
    wpm = calc_wpm(len(typed), elapsed)
    acc = calc_accuracy(target, typed)
    print(f"  用时：{elapsed:.1f} 秒　速度：{wpm:.1f} WPM　正确率：{acc:.1f}%")
    return wpm, acc


def cmd_main(argv=None):
    p = argparse.ArgumentParser(prog="typing", description="终端打字速度测试")
    p.add_argument("--version", action="version", version="typing 0.1.0")
    p.add_argument("--lang", choices=["en", "zh"], default="zh",
                   help="句子语言（默认 zh）")
    p.add_argument("--rounds", type=int, default=1,
                   help="测试轮数，取平均值（默认 1）")
    p.add_argument("--seed", type=int, default=None,
                   help="随机种子（固定句子顺序，用于演示/测试）")
    p.add_argument("--script", action="store_true",
                   help="从 stdin 读取每轮的输入（用于测试/脚本）")
    p.add_argument("--json", action="store_true", help="JSON 输出")
    args = p.parse_args(argv)

    if args.rounds < 1:
        print("error: --rounds 必须 >= 1", file=sys.stderr)
        return 2

    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    lines = sys.stdin.read().splitlines() if args.script else None

    results = []
    for i in range(args.rounds):
        target = pick_sentence(args.lang, rng)
        if args.script:
            typed = lines[i] if i < len(lines) else ""
            start = time.monotonic()
            elapsed = max(time.monotonic() - start, 0.001)
            wpm = calc_wpm(len(typed), elapsed)
            acc = calc_accuracy(target, typed)
            print(f"第 {i + 1} 轮：{wpm:.1f} WPM，正确率 {acc:.1f}%")
        else:
            if args.rounds > 1:
                print(f"—— 第 {i + 1}/{args.rounds} 轮 ——")
            wpm, acc = play_round(target, lambda: input("> "))
        results.append({"target": target, "wpm": round(wpm, 1),
                        "accuracy": round(acc, 1)})

    avg_wpm = sum(r["wpm"] for r in results) / len(results)
    avg_acc = sum(r["accuracy"] for r in results) / len(results)

    if args.json:
        print(json.dumps({"rounds": results, "avg_wpm": round(avg_wpm, 1),
                          "avg_accuracy": round(avg_acc, 1)},
                         ensure_ascii=False, indent=2))
    else:
        if len(results) > 1:
            print()
            print(f"平均：{avg_wpm:.1f} WPM，正确率 {avg_acc:.1f}%")
    return 0


def main():
    sys.exit(cmd_main())


if __name__ == "__main__":
    main()
