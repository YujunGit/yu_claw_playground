#!/usr/bin/env python3
import argparse
import random
import sys
import time

BREAK_LINES = [
    "先别急着高效，摸鱼两分钟，灵感要先泡开。",
    "你现在最需要的不是自律，是一次合法走神。",
    "暂停一下，给大脑一点表演松弛感的空间。",
    "认真休息也是生产流程，不许把摸鱼污名化。",
    "去喝口水，或者对着天花板发一会儿呆。这个环节很专业。",
]

FOCUS_LINES = [
    "好了，摸够了。现在把刚才欠世界的那一点专注还回去。",
    "演出结束，观众散场，轮到你开始推进正事了。",
    "你已经完成高质量偷懒，接下来请切换到低噪音输出模式。",
    "别装死了，回来干活。温柔地，持续地，别一下冲太猛。",
    "现在开工刚刚好。把任务拆小，先推进第一步。",
]

MID_BREAK_LINES = [
    "还在摸鱼阶段，别急，合法摆烂尚未到期。",
    "这是恢复，不是逃避。至少目前我们还可以这么定义。",
    "休息中。请维持一种若有所思但其实没在想事的状态。",
]

MID_FOCUS_LINES = [
    "继续，别追求伟大，先追求把下一步做完。",
    "保持一点点推进就行，稳定比激情耐用。",
    "你现在不需要顿悟，只需要别切窗口。",
]


def banner(text: str):
    print("\n" + "=" * 56)
    print(text)
    print("=" * 56)


def countdown(minutes: int, stage: str):
    seconds = max(0, minutes) * 60
    if seconds == 0:
        return
    tick = 60 if seconds >= 60 else 1
    lines = MID_BREAK_LINES if stage == "break" else MID_FOCUS_LINES
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        print(f"[{stage}] 剩余 {mins:02d}:{secs:02d} · {random.choice(lines)}")
        time.sleep(min(tick, seconds))
        seconds -= tick


def run_session(break_minutes: int, focus_minutes: int, dry_run: bool):
    banner("Reverse Pomodoro Anti-Coach")
    print(random.choice(BREAK_LINES))
    print(f"建议先摸鱼 {break_minutes} 分钟，再专注 {focus_minutes} 分钟。")

    if dry_run:
        print("\n[dry-run] 跳过等待，直接展示下一阶段。")
    else:
        countdown(break_minutes, "break")

    banner("摸鱼时间到，回收灵魂")
    print(random.choice(FOCUS_LINES))

    if dry_run:
        print("[dry-run] 已完成整轮演示。")
    else:
        countdown(focus_minutes, "focus")
        banner("本轮结束")
        print("收工。你可以再来一轮，或者体面地下班。")


def parse_args():
    p = argparse.ArgumentParser(description="A tiny reverse pomodoro anti-coach.")
    p.add_argument("--break", dest="break_minutes", type=int, default=5, help="break minutes")
    p.add_argument("--focus", dest="focus_minutes", type=int, default=25, help="focus minutes")
    p.add_argument("--dry-run", action="store_true", help="skip waiting and only demonstrate messages")
    return p.parse_args()


def main():
    args = parse_args()
    if args.break_minutes < 0 or args.focus_minutes < 0:
        print("时长不能是负数。", file=sys.stderr)
        sys.exit(1)
    run_session(args.break_minutes, args.focus_minutes, args.dry_run)


if __name__ == "__main__":
    main()
