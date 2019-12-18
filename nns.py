import torch

class one_layer_nn(torch.Module):
    def __init__(self, input_size, hidden_size, output_size):
        self.W1 = torch.nn.Linear(input_size, hidden_size)
        self.W2 = torch.nn.Linear(hidden_size, output_size)
        self.act = torch.nn.ReLU()

        self.softmax = nn.LogSoftmax()
        self.loss = nn.NLLLoss()
    
    def calc_loss(self, output, gold):
        return self.loss(output, gold)
    
    def forward(self, input_vec):
        a1 = self.W1(input_vec)
        z1 = self.act(a1)
        a2 = self.W2(z1)
        out = self.softmax(a2)
        return out


class n_layer_nn(toch.Module):
    def __init__(self, input_size, hidden_sizes, output_size):
        self.Ws = []
        self.Ws.append(torch.nn.Linear(input_size, hidden_sizes[1]))
        for i in range(1, len(hidden_sizes)):
            self.Ws.append(torch.nn.Linear(hidden_sizes[i-1][hidden_sizes[i]]))
        self.final_layer = torch.nn.Linear(hidden_sizes[-1], output_size)
        self.act = torch.nn.ReLU()

        self.softmax = nn.LogSoftmax()
        self.loss = nn.NLLLoss()
    
    def calc_loss(self, output, gold):
        return self.loss(output, gold)

    def forward(self, input_vec)
        cur_val = input_vec
        for weight in self.Ws:
            cur_val = self.act(weight(cur_val))
        return self.softmax(self.final_layer(cur_val))