# Reverse Pomodoro Anti-Coach

一个反着来的小番茄钟：

- 先一本正经地劝你摸鱼几分钟
- 然后温柔但欠揍地把你拉回工作
- 适合命令行快速来一轮

## 用法

```bash
python3 anti_coach.py
python3 anti_coach.py --break 3 --focus 10
python3 anti_coach.py --break 1 --focus 5 --dry-run
```

## 参数

- `--break`: 摸鱼时长（分钟），默认 5
- `--focus`: 回来工作时长（分钟），默认 25
- `--dry-run`: 不等待，直接演示整轮文案

## 说明

这是一个轻量 CLI playground 项目，重点在气质和体验，不是严肃的效率工具。
