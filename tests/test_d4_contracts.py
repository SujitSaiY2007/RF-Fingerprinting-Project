import numpy as np
import torch
from src.smorffi_d2 import deterministic_split, parse_canonical_preamble
from src.smorffi_d4 import build_model, iq_to_tensor

def test_d2_split_is_deterministic():
    assert deterministic_split('1', 0) == deterministic_split('1', 0)

def test_canonical_iq_shape():
    text='[' + ' '.join(['1+2j'] * 288) + ']'
    parsed=parse_canonical_preamble(text)
    x=iq_to_tensor(parsed.iq)
    assert parsed.canonical_length == 288
    assert x.shape == (2, 288)
    assert x.dtype == np.float32

def test_d4_model_output_contract():
    model=build_model(33)
    z,logits=model(torch.zeros(4,2,288))
    assert z.shape == (4,32)
    assert logits.shape == (4,33)
