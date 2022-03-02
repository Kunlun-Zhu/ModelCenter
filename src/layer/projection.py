import torch
import bmpretrain as bmp
import cpm_kernels.torch as ct
from .linear import Linear
import math

class Projection(bmp.DistributedModule):
    def __init__(self,
                 dim_out : int,
                 dim_in : int,
                 length_scale : bool = False,
                 dtype = torch.half,
                 int8 = False,
                 init_mean = 0.0,
                 init_std = 1,
                 bias = False,
                ):
        super().__init__()

        self.w = Linear(
            dim_in = dim_in,
            dim_out = dim_out,
            length_scale = length_scale,
            length_scale_before = True,
            dtype = dtype,
            int8 = int8,
            init_mean = init_mean,
            init_std = init_std,
            bias = bias,
        )

    def forward(self, x : torch.Tensor):
        """
        Args:
            hidden : (batch_size, dim_in, seq_len)           int32
        Returns:
            logits : (batch, seq_len, dim_out)        fp16
        """
        logits = self.w(x)
        logits = ct.transpose(logits)   # eqauls to .transpose(1, 2)
        return logits
