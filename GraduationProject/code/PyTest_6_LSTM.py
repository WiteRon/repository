import torch
import torch.nn as nn


batch_size = 10
seq_len = 20
vocab_size = 100
embedding_dim = 30  # len of vec = 30
hidden_size = 18
num_layer = 1

input = torch.randint(low=0,high=100,size=[batch_size,seq_len])
embedding = nn.Embedding(vocab_size,embedding_dim)
input_embedded = embedding(input)

lstm = nn.LSTM(input_size=embedding_dim,hidden_size=hidden_size,
               num_layers=num_layer,batch_first=True)
output,(h_n,c_n) = lstm(input_embedded)
print(output.size())
print('*'*100)
print(h_n.size())
print('*'*100)
print(c_n.size())

