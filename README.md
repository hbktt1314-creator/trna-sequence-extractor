# tRNA Sequence Extractor

从 GenBank 注释和 FASTA 序列中提取 tRNA 基因序列及相关注释，并将结果追加保存到 Excel 文件。

> 当前仓库脚本是一个按固定文件名运行的原型。使用前请阅读下方的输入要求和注意事项；特别是脚本会覆盖写回 `trna_gene.xlsx`，建议先备份。

## 功能

脚本 `gbfile_parese.py` 会：

1. 读取 GenBank 文件中的 `tRNA` 特征。
2. 提取反密码子、推导出的氨基酸类型、染色体、基因坐标和链方向等注释。
3. 按注释坐标从 FASTA 序列中提取核苷酸序列；负链序列会进行反向互补处理。
4. 将结果追加到已有的 Excel 工作簿并保存。

## 环境与依赖

建议使用 Python 3.9 或更高版本。安装依赖：

```bash
python -m pip install biopython "pandas<2.0" openpyxl
```

脚本当前使用 `DataFrame.append()`，该接口在 pandas 2.0 中已移除，因此需要 pandas 1.x。若要使用 pandas 2.x，需要先将脚本中的追加逻辑改为 `pd.concat()`。

## 输入文件

脚本从**当前工作目录**读取以下固定名称的文件：

| 文件 | 用途 |
| --- | --- |
| `sequence.gb` | 包含 tRNA 注释的 GenBank 文件 |
| `序列sequence.fasta` | 用于按坐标提取序列的 FASTA 文件 |
| `trna_gene.xlsx` | 已存在的 Excel 工作簿；脚本会在其后追加结果 |

目录示例：

```text
项目目录/
├── gbfile_parese.py
├── sequence.gb
├── 序列sequence.fasta
└── trna_gene.xlsx
```

`trna_gene.xlsx` 必须预先存在且可由 pandas 读取。请确认 GenBank 注释和 FASTA 序列使用相同参考序列及相容的坐标体系。

## 运行

在上述文件所在目录执行：

```bash
python gbfile_parese.py
```

程序会将新提取的行追加到 `trna_gene.xlsx`，然后**覆盖保存同一个文件**。重复运行会再次追加结果，可能造成重复记录。运行前请备份原 Excel 文件。

## 输出字段

脚本新增的主要列包括：

- `Isotype-氨基酸`：由 GenBank 的 anticodon 注释字段解析出的 tRNA 氨基酸类型。
- `anticodon-反密码子`：反密码子。
- `chromosome-染色体`：染色体标识。
- `locus-基因位置`：基因坐标；负链位置使用 `complement(...)` 表示。
- `正负链`：链方向（`+` 或 `-`）。
- `序列`：从 FASTA 中提取的核苷酸序列；负链为反向互补序列。

## 重要限制与注意事项

- **FASTA 记录匹配：**当前实现会将每条 tRNA 注释依次用于每条 FASTA 记录，并未依据染色体或序列 ID 进行匹配。若 FASTA 中包含多条记录，结果可能来自不对应的记录。建议先确认 FASTA 只有与注释坐标对应的目标序列，或改进脚本实现显式匹配。
- **注释格式假设：**脚本按固定位置读取 GenBank 描述中的染色体字符，并假设 anticodon qualifier 存在且具有特定格式。其他来源的 GenBank 文件可能导致解析错误或信息错误。
- **边界处理：**当前代码会跳过 `end >= 序列长度` 的特征，因此恰好延伸到序列末端的特征也可能被跳过。
- **反向互补：**当前实现显式处理 A、T、G、C；其他符号会保留原样。含模糊碱基的序列需要验证输出。
- **数据安全与许可：**公开仓库中不要提交未获授权公开的基因组数据、样本信息或敏感研究数据。请确认输入数据的使用和再分发许可。
- **科学结果验证：**输出应与原始注释及序列进行抽样核对；该脚本不替代对坐标、染色体匹配和生物学注释的人工验证。

## 许可证

本项目采用 [Apache License 2.0](LICENSE)。
