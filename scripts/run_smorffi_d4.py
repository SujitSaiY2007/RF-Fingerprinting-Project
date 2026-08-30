"""Track-A D4 baseline runner.

Consumes the frozen D2 SMoRFFI representation and deterministic split. Device/MAC
identifiers are labels/provenance only. The baseline is not accuracy-tuned.
"""
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
import numpy as np
from src.smorffi_d2 import parse_canonical_preamble, deterministic_split
from src.smorffi_d4 import D4Config, build_model, set_seed, iq_to_tensor

def load_rows(root:Path, devices:set[str]|None=None):
 X=[];y=[];split=[];sources=[]
 for path in sorted(root.rglob('*.csv')):
  with path.open('r',encoding='utf-8-sig',newline='') as f:
   reader=csv.DictReader(f)
   for row_index,row in enumerate(reader):
    device=str(row['Device Number'])
    if devices is not None and device not in devices: continue
    p=parse_canonical_preamble(row['preamble']);X.append(iq_to_tensor(p.iq));y.append(device);split.append(deterministic_split(device,row_index));sources.append({'file':path.name,'source_row_index':row_index,'device':device})
 if not X: raise ValueError('no SMoRFFI CSV observations found')
 return np.stack(X),np.asarray(y),np.asarray(split),sources

def train(root:Path,output:Path,config:D4Config,devices:set[str]|None=None):
 import torch
 set_seed(config.seed); torch.set_num_threads(4)
 X,y_text,split,sources=load_rows(root,devices);labels=sorted(np.unique(y_text));label_to_int={v:i for i,v in enumerate(labels)};y=np.asarray([label_to_int[v] for v in y_text],dtype=np.int64)
 train_mask,validation_mask,test_mask=[split==k for k in ('train','validation','test')]
 model=build_model(len(labels),config.embedding_dim);opt=torch.optim.Adam(model.parameters(),lr=config.learning_rate,weight_decay=config.weight_decay);loss_fn=torch.nn.CrossEntropyLoss()
 train_x=torch.from_numpy(X[train_mask]);train_y=torch.from_numpy(y[train_mask]);generator=torch.Generator().manual_seed(config.seed);history=[]
 for epoch in range(config.epochs):
  model.train();total=0.0;perm=torch.randperm(len(train_x),generator=generator)
  for start in range(0,len(train_x),config.batch_size):
   idx=perm[start:start+config.batch_size];opt.zero_grad(set_to_none=True);_,logits=model(train_x[idx]);loss=loss_fn(logits,train_y[idx]);loss.backward();opt.step();total+=float(loss.detach())
  model.eval()
  with torch.no_grad(): _,val_logits=model(torch.from_numpy(X[validation_mask]))
  history.append({'epoch':epoch+1,'train_loss':total/max(1,(len(train_x)+config.batch_size-1)//config.batch_size),'validation_accuracy':float((val_logits.argmax(1).numpy()==y[validation_mask]).mean())})
 model.eval()
 with torch.no_grad(): zt,logits=model(torch.from_numpy(X[test_mask]))
 pred=logits.argmax(1).numpy();result={'status':'reproducible-baseline','dataset':{'rows':int(len(X)),'devices':len(labels)},'split_counts':{k:int((split==k).sum()) for k in ('train','validation','test')},'embedding_dim':config.embedding_dim,'test_accuracy':float((pred==y[test_mask]).mean()),'history':history,'sources_sha256':__import__('hashlib').sha256(json.dumps(sources,sort_keys=True).encode()).hexdigest()}
 output.mkdir(parents=True,exist_ok=True);torch.save({'state_dict':model.state_dict(),'labels':labels,'config':config.__dict__},output/'d4_model.pt');np.savez_compressed(output/'d4_test_embeddings.npz',embedding=zt.numpy(),y=y[test_mask],labels=np.asarray(labels),pred=pred);(output/'d4_result.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('data_root',type=Path);ap.add_argument('--output',type=Path,default=Path('experiments/track_a/d4'));ap.add_argument('--devices',nargs='*',help='optional explicit device numbers; omit to use all files');a=ap.parse_args();print(json.dumps(train(a.data_root,a.output,D4Config(),set(a.devices) if a.devices else None),indent=2))
