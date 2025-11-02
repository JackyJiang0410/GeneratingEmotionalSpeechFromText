# Emo-TTS Benchmark

一个用于对比 F5-TTS 和 Tortoise-TTS 两个模型在情绪语音合成任务上的性能评估项目。

## 项目结构

```
emo-tts-benchmark/
├── models/
│   ├── f5-tts/          # F5-TTS 模型（已 git clone）
│   └── tortoise-tts/     # Tortoise-TTS 模型（已 git clone）
├── data/
│   ├── texts/           # 文本文件目录
│   │   ├── happy/        # 快乐情绪文本
│   │   │   ├── 01.txt
│   │   │   ├── 02.txt
│   │   │   └── ...
│   │   ├── sad/          # 悲伤情绪文本
│   │   │   ├── 01.txt
│   │   │   ├── 02.txt
│   │   │   └── ...
│   │   ├── angry/        # 愤怒情绪文本
│   │   ├── tired/        # 疲惫情绪文本
│   │   ├── excited/      # 兴奋情绪文本
│   │   └── neutral/      # 中性情绪文本
│   └── references/      # 情绪参考音频目录（可选，如 happy_ref.wav, sad_ref.wav...）
├── outputs/
│   ├── f5/              # F5-TTS 输出目录
│   │   ├── happy/
│   │   ├── sad/
│   │   └── ...
│   └── tortoise/         # Tortoise-TTS 输出目录
│       ├── happy/
│       ├── sad/
│       └── ...
├── scripts/
│   ├── run_f5_batch.py       # F5-TTS 批量生成脚本
│   └── run_tortoise_batch.py  # Tortoise-TTS 批量生成脚本
└── README.md
```

## 使用说明

### 1. 准备数据

在 `data/texts/` 目录下为每种情绪创建对应的文件夹，并在每个文件夹中放置多个文本文件：

```
data/texts/
├── happy/
│   ├── 01.txt
│   ├── 02.txt
│   └── ...
├── sad/
│   ├── 01.txt
│   ├── 02.txt
│   └── ...
├── angry/
│   ├── 01.txt
│   └── ...
├── tired/
├── excited/
└── neutral/
```

每个 `.txt` 文件包含一行文本，该文本将被生成一条语音。

**注意：**
- 文件命名可以是任意格式（如 `01.txt`, `file1.txt` 等）
- 输出文件名将基于输入文件名生成（如 `01.txt` -> `f5-happy-01.wav`）

可选：在 `data/references/` 目录下放置参考音频文件（命名格式：`<emotion>_ref.wav`），如：
- `happy_ref.wav`
- `sad_ref.wav`
- ...

如果不存在参考音频，脚本将使用模型默认设置生成。

### 2. 运行批量生成

两个脚本都使用 Python 格式，运行方式统一：

#### F5-TTS

```bash
conda activate f5
python scripts/run_f5_batch.py
```

#### Tortoise-TTS

```bash
conda activate tortoise
python scripts/run_tortoise_batch.py
```

### 3. 输出格式

生成的音频文件将按以下格式命名：

- F5-TTS: `outputs/f5/<emotion>/f5-<emotion>-<filename>.wav`
- Tortoise-TTS: `outputs/tortoise/<emotion>/tortoise-<emotion>-<filename>.wav`

其中：
- `<emotion>`: 情绪名称（happy, sad, angry, tired, excited, neutral）
- `<filename>`: 输入文本文件的文件名（不含扩展名）

**示例：**
- 输入：`data/texts/happy/01.txt`
- F5-TTS 输出：`outputs/f5/happy/f5-happy-01.wav`
- Tortoise-TTS 输出：`outputs/tortoise/happy/tortoise-happy-01.wav`

### 4. 对比分析

生成的音频文件按照统一的命名规则输出，方便进行对比：

- 相同的输入文本文件在 F5-TTS 和 Tortoise-TTS 上生成的音频文件名对应（除了前缀）
- 例如：
  - `outputs/f5/happy/f5-happy-01.wav`
  - `outputs/tortoise/happy/tortoise-happy-01.wav`

这两个文件使用相同的输入文本文件（`data/texts/happy/01.txt`）生成，便于对比两个模型的效果。

## 注意事项

1. **环境要求**：
   - F5-TTS 需要在对应的 conda 环境中运行
   - Tortoise-TTS 需要在对应的 conda 环境中运行

2. **模型目录**：
   - 不要修改 `models/f5-tts/` 和 `models/tortoise-tts/` 目录中的内容
   - 脚本只会读取这些目录，不会修改它们

3. **参考音频**：
   - 参考音频为可选，如果不存在，脚本会使用模型默认设置
   - 参考音频格式应为 WAV

4. **输出目录**：
   - 脚本会自动创建所需的输出目录
   - 如果输出文件已存在，将被覆盖

5. **文本文件**：
   - 每个文本文件应包含一行文本
   - 空文件将被跳过
   - 文件名将用于生成对应的输出文件名

## 脚本说明

### `run_f5_batch.py`

F5-TTS 批量生成脚本（Python）。该脚本：
- 遍历 `data/texts/<emotion>/` 目录下的所有文本文件
- 检查是否有对应的参考音频（`data/references/<emotion>_ref.wav`）
- 如果没有参考音频，使用 F5-TTS 默认参考音频
- 对每个文本文件生成语音，保存到 `outputs/f5/<emotion>/f5-<emotion>-<filename>.wav`

### `run_tortoise_batch.py`

Tortoise-TTS 批量生成脚本（Python）。该脚本：
- 遍历 `data/texts/<emotion>/` 目录下的所有文本文件
- 检查是否有对应的参考音频（`data/references/<emotion>_ref.wav`）
- 如果没有参考音频，使用随机 conditioning latents
- 对每个文本文件生成语音，保存到 `outputs/tortoise/<emotion>/tortoise-<emotion>-<filename>.wav`
- 使用 'fast' preset 以加快生成速度

## 支持的情绪

- `happy` - 快乐
- `sad` - 悲伤
- `angry` - 愤怒
- `tired` - 疲惫
- `excited` - 兴奋
- `neutral` - 中性

