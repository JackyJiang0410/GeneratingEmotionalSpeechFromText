# Tortoise-TTS 使用指南

## 前提条件

1. **已创建 conda 环境**：需要名为 `tortoise` 的 conda 环境
2. **已安装 Tortoise-TTS**：模型代码在 `models/tortoise-tts/` 目录
3. **文本文件已准备**：`data/texts/<emotion>/*.txt` 格式的文本文件

## 步骤 1：检查/创建 conda 环境

### 检查环境是否存在

```bash
conda info --envs | grep tortoise
```

### 如果环境不存在，创建它

```bash
# 创建环境（使用 Python 3.9，根据 Tortoise-TTS 官方文档）
conda create -n tortoise python=3.9 -y

# 激活环境
conda activate tortoise
```

## 步骤 2：安装依赖

### 安装 PyTorch（根据你的硬件）

**对于 Apple Silicon (Mac M系列芯片)：**
```bash
pip install torch torchaudio
```

**对于 NVIDIA GPU：**
```bash
# 访问 https://pytorch.org/ 获取适合你系统的命令
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
```

### 安装 Tortoise-TTS

```bash
# 进入 Tortoise-TTS 目录
cd /Users/haojiang/Desktop/EE381V/Project/models/tortoise-tts

# 安装依赖（如果有 requirements.txt）
pip install -r requirements.txt

# 或者使用 setup.py 安装
pip install -e .

# 或者直接使用 pip 安装
pip install tortoise-tts
```

### 验证安装

```bash
python -c "from tortoise.api import TextToSpeech; print('Tortoise-TTS installed successfully!')"
```

## 步骤 3：运行脚本

### 确保在项目根目录

```bash
cd /Users/haojiang/Desktop/EE381V/Project
```

### 激活环境并运行

```bash
# 激活 tortoise 环境
conda activate tortoise

# 运行脚本
python scripts/run_tortoise_batch.py
```

## 输出

脚本会生成音频文件到：
```
outputs/tortoise/
├── happy/
│   ├── tortoise-happy-01.wav
│   ├── tortoise-happy-02.wav
│   └── tortoise-happy-03.wav
├── sad/
├── angry/
├── tired/
├── excited/
└── neutral/
```

## 故障排查

### 问题 1：找不到 conda 环境

**解决方案**：创建环境（见步骤 1）

### 问题 2：导入错误

```
Error importing Tortoise-TTS: No module named 'tortoise'
```

**解决方案**：
1. 确保在正确的 conda 环境中
2. 确保已安装 Tortoise-TTS（见步骤 2）

### 问题 3：模型加载失败

```
Error loading Tortoise-TTS model: ...
```

**可能原因**：
- 缺少必要的依赖库
- PyTorch 版本不兼容
- 模型文件未下载（Tortoise-TTS 会自动下载，但需要网络连接）

**解决方案**：
1. 检查网络连接
2. 确保所有依赖都已安装
3. 查看详细错误信息

### 问题 4：生成速度慢

**正常现象**：Tortoise-TTS 生成音频较慢，特别是使用 'fast' preset 时。

**可选优化**：
- 脚本已使用 'fast' preset
- 可以在脚本中修改 `preset='fast'` 为其他预设值（'ultra_fast', 'standard', 'high_quality'）

## 完整示例命令

```bash
# 1. 检查环境
conda info --envs | grep tortoise

# 2. 如果不存在，创建环境
conda create -n tortoise python=3.9 -y
conda activate tortoise

# 3. 安装 PyTorch（Apple Silicon）
pip install torch torchaudio

# 4. 安装 Tortoise-TTS
cd /Users/haojiang/Desktop/EE381V/Project/models/tortoise-tts
pip install -r requirements.txt
# 或者
pip install -e .

# 5. 返回项目根目录
cd /Users/haojiang/Desktop/EE381V/Project

# 6. 运行脚本
conda activate tortoise
python scripts/run_tortoise_batch.py
```

## 注意事项

1. **生成时间**：Tortoise-TTS 生成音频需要较长时间，请耐心等待
2. **参考音频**：可选，如果存在 `data/references/<emotion>_ref.wav`，脚本会使用它
3. **模型下载**：首次运行时，Tortoise-TTS 会自动下载模型文件（可能需要几分钟）
4. **内存要求**：Tortoise-TTS 需要较大的内存，确保系统有足够的 RAM

## 输出文件对应关系

与 F5-TTS 输出文件一一对应：

| 输入文件 | F5-TTS 输出 | Tortoise-TTS 输出 |
|---------|------------|-------------------|
| `data/texts/happy/01.txt` | `outputs/f5/happy/f5-happy-01.wav` | `outputs/tortoise/happy/tortoise-happy-01.wav` |
| `data/texts/happy/02.txt` | `outputs/f5/happy/f5-happy-02.wav` | `outputs/tortoise/happy/tortoise-happy-02.wav` |

这样便于对比两个模型在相同输入上的表现。

