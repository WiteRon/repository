import torch
import numpy as np
import torch.nn as nn
import torch.nn.functional as F


batch_size = 2
max_num_src_words = 8
max_num_tgt_words = 8#这两个参数是单词表数目，字母的编号一共可以是1-8
max_src_seq_len = 5
max_tgt_seq_len = 5#这两个参数是句子的长度，一次数据一共最多能有几个字母（编号）
model_dim = 8
max_position_len = 5

src_len = torch.Tensor([2,4]).to(torch.int32)
tgt_len = torch.Tensor([4,3]).to(torch.int32)

src_seq = torch.cat([torch.unsqueeze(F.pad(torch.randint(1,max_num_src_words,(L,)),(0,max_src_seq_len-L)),0) for L in src_len])
tgt_seq = torch.cat([torch.unsqueeze(F.pad(torch.randint(1,max_num_tgt_words,(L,)),(0,max_tgt_seq_len-L)),0) for L in tgt_len])

src_embedding_table = nn.Embedding(max_num_src_words+1,model_dim)
tgt_embedding_table = nn.Embedding(max_num_tgt_words+1,model_dim)
src_embedding = src_embedding_table(src_seq)
tgt_embedding = tgt_embedding_table(tgt_seq)
pos_mat = torch.arange(max_position_len).reshape((-1,1))
i_mat = torch.pow(10000,torch.arange(max_position_len).reshape((1,-1))/model_dim)
pe_embedding_table = torch.zeros(max_position_len,model_dim)
pe_embedding_table[:,0::2] = torch.sin(pos_mat/i_mat)
pe_embedding_table[:,1::2] = torch.cos(pos_mat/i_mat)
pe_embedding = nn.Embedding(max_position_len,model_dim)
pe_embedding.weight = nn.Parameter(pe_embedding_table,requires_grad=False)
src_pos = torch.cat([torch.unsqueeze(torch.arange(max(src_len)),0) for L in src_len]).to(torch.int32)
tgt_pos = torch.cat([torch.unsqueeze(torch.arange(max(tgt_len)),0) for L in tgt_len]).to(torch.int32)
src_pe_embedding = pe_embedding(src_pos)
tgt_pe_embedding = pe_embedding(tgt_pos)

nn.Linear()










