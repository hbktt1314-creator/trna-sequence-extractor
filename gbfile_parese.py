import uuid
from Bio import SeqIO
import pandas as pd
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import Seq

# 初始化结果列表
tRNA_records = []
id = 0
output_res = []


# 打开文件
with open("./sequence（1）.gb", "r") as file:
    # 读取文件内容
    records = list(SeqIO.parse(file, "genbank"))

    # 初始化结果列表
    #tRNA_records = []

    # 遍历记录
    for record in records:
        index = record.description.find('chromosome')
        if index != -1:
            chromosome = record.description[48:49]
        # 染色体 print(chromosome)
        # 查找tRNA特征
        for feature in record.features:
            if feature.type == "tRNA":
                # 提取携带氨基酸
                amino_acid = feature.qualifiers.get("codon_table", "")

                # 提取反密码子
                anticodon_a = feature.qualifiers.get("anticodon", "")[0].split(',')
                anticodon_a3 = anticodon_a[-1].upper()
                anticodon_a[-1] = anticodon_a3
                anticodon = [",".join(anticodon_a)]
                #氨基酸 print(anticodon_a[1].split(':')[1])
                #反密码子 print(anticodon_a[2].split(':')[1][0:3])

                # 提取染色体信息
                #chromosome = feature.qualifiers.get("chromosome", "")
                position = feature.location.start

                # TRNA基因位置
                trna_start = feature.location.start+1
                trna_end = feature.location.end
                # tRNA.append((feature.location.start, feature.location.end))

                # 正负链
                strand = feature.strand

                # TRNA名字
                trna_name = 'trna_name{}'.format(id)
                id = id + 1

                if strand == -1:
                    locus = "complement({}..{})".format(trna_start, trna_end)
                else:
                    locus = "{}..{}".format(trna_start,trna_end)
                if strand == -1:
                    p_n = "-"
                else:
                    p_n = "+"

                # 添加到结果列表
                tRNA_records.append({
                    "carries_amino_acid": amino_acid,
                    "anticodon": anticodon,
                    "chromosome": chromosome,
                    "position": position,
                    "trna_start": trna_start,
                    "trna_end": trna_end,
                    "strand": strand,
                    "trna_name":trna_name,
                    "Isotype-氨基酸": "tRNA-" + anticodon_a[1].split(':')[1],
                    "anticodon-反密码子": anticodon_a[2].split(':')[1][0:3],
                    "chromosome-染色体": chromosome,
                    "locus-基因位置": locus,
                    "正负链": p_n,
                    # "strand": record.features[0].strand
                })

# 关闭文件
file.close()

# 读取输入文件（FASTA格式）
filename = "./序列sequence(1).fasta"
sequences = list(SeqIO.parse(filename, "fasta"))

# 定义tRNA位置列表
tRNA_positions = []

for tRNA in tRNA_records:
    # print("trna_start:", tRNA["trna_start"])
    # print("trna_end:", tRNA["trna_end"])
    # print("strand:", tRNA["strand"])
    tRNA_positions.append((tRNA["trna_start"],tRNA["trna_end"],tRNA["strand"],tRNA['trna_name'],tRNA['Isotype-氨基酸'],tRNA['anticodon-反密码子'],tRNA['chromosome-染色体'],tRNA['locus-基因位置'],tRNA['正负链']))

# 提取tRNA序列
tRNA_sequences2 = []
tRNA_sequences = []

for seq_record in sequences:
    seq_id = seq_record.id
    seq_length = len(seq_record.seq)

    for start, end, strand,trna_name,an_ji_suan,anticodon,chromosome,locus,p_n in tRNA_positions:
        if start >= seq_length or end >= seq_length:
            continue


        # 提取tRNA序列
        tRNA_seq = seq_record.seq[start-1:end]

        # tRNA_record = SeqRecord(tRNA_seq, id=f"{seq_id}_tRNA", description=f"{trna_name} tRNA")
        # tRNA_sequences.append(tRNA_record)

        # 负链 互补
        reverse_sequences = ''
        if strand == -1:
            for tcag in tRNA_seq[::-1]:
                if tcag == "T":
                    reverse_sequences += "A"
                elif tcag == "A":
                    reverse_sequences += "T"
                elif tcag == "G":
                    reverse_sequences += "C"
                elif tcag == "C":
                    reverse_sequences += "G"
                else:
                    reverse_sequences += tcag
        else:
            reverse_sequences = tRNA_seq

        tRNA_sequences2.append({
                    "Isotype-氨基酸": an_ji_suan,
                    "anticodon-反密码子": anticodon,
                    "chromosome-染色体": chromosome,
                    "locus-基因位置": locus,
                    "正负链": p_n,
                    "序列": reverse_sequences,
                    # "strand": record.features[0].strand
                })


original_data = pd.read_excel('./trna_gene.xlsx')

data2 = pd.DataFrame(tRNA_sequences2)
# 将新数据与旧数据合并起来
save_data = original_data.append(data2)
save_data.to_excel('./trna_gene.xlsx', index=False)
