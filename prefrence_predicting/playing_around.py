import numpy as np
import torch

var1 = [[1],[2],[3],[4]]
var2 = [[1],[2],[3],[4]]

var1 = torch.tensor(var1,dtype=torch.float)
var2 = torch.sub(1,var1)

var = torch.squeeze(torch.stack((var1,var2),axis=2))
print (var)
