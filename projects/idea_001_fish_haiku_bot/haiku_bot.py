#!/usr/bin/env python3
"""
Fish Haiku Bot
生成轻量、可重复、带一点赛博感的中文俳句。
"""

from __future__ import annotations
import argparse
import random

OPENERS = [
    "夜色很薄", "风从屏幕吹过", "云在代码上漂", "小鱼跃出光标", "月亮落进终端"
]
MIDDLES = [
    "{topic}轻轻发亮", "{topic}在心里回声", "{topic}穿过雨线", "{topic}像未读消息", "{topic}停在掌心"
]
ENDERS = [
    "我把它写进海里", "明天继续游", "世界忽然安静", "只剩一串泡泡", "然后星星点头"
]


def make_haiku(topic: str, seed: int | None = None) -> str:
    rng = random.Random(seed)
    a = rng.choice(OPENERS)
    b = rng.choice(MIDDLES).format(topic=topic)
    c = rng.choice(ENDERS)
    return f"{a}，\n{b}，\n{c}。"


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate cyber-fish style Chinese haikus")
    parser.add_argument("topic", nargs="?", default="今天", help="haiku topic")
    parser.add_argument("-n", "--count", type=int, default=3, help="number of haikus")
    parser.add_argument("--seed", type=int, default=None, help="random seed")
    args = parser.parse_args()

    for i in range(args.count):
        seed = None if args.seed is None else args.seed + i
        print(f"\n--- Haiku {i+1} ---")
        print(make_haiku(args.topic, seed=seed))


if __name__ == "__main__":
    main()
