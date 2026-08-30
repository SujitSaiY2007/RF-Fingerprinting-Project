"""D6/D7 Track-A evaluation for the frozen D5 Random Forest.

D6: threshold max class probability on known validation only, then evaluate
unknown devices 34-123 on their deterministic test partition.
D7: apply controlled gain/AWGN perturbations to the frozen known test I/Q;
never retrain or tune on the perturbed test data.
"""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.smorffi_d2 import deterministic_split, parse_canonical_preamble
from src.smorffi_d3 import extract_rf_features
FEATURES=['i_mean','i_std','q_mean','q_std','amplitude_mean','amplitude_std','rms_amplitude','crest_factor','mean_power','iq_variance_ratio_db','iq_correlation','mean_phase_step_rad','std_phase_step_rad','spectral_centroid_hz','spectral_spread_hz','spectral_entropy_bits']
def feats(z):
 return np.asarray([[extract_rf_features(s)[k] for k in FEATURES] for s in z],dtype=float)
def load(root, known=False, unknown_test=False):
 rows=[]
 for p in sorted(root.glob('*.csv')):
  with p.open('r',encoding='utf-8-sig',newline='') as f:
   for i,r in enumerate(csv.DictReader(f)):
    d=int(r['Device Number']); ok=(1<=d<=33) if known else (d>=34 and deterministic_split(str(d),i)=='test') if unknown_test else False
    if ok:
     q=parse_canonical_preamble(r['preamble']); rows.append((d,i,q.samples[:288]))
 return rows
def metrics(y,p): return {'accuracy':float(accuracy_score(y,p)),'macro_f1':float(f1_score(y,p,average='macro')),'balanced_accuracy':float(balanced_accuracy_score(y,p))}
def main(root):
 rows=load(root,known=True); y=np.array([r[0] for r in rows]); sp=np.array([deterministic_split(str(r[0]),r[1]) for r in rows]); X=feats([r[2] for r in rows])
 m=RandomForestClassifier(n_estimators=100,random_state=20260830,n_jobs=-1,max_features='sqrt').fit(X[sp=='train'],y[sp=='train'])
 pv=m.predict_proba(X[sp=='validation']); thr=float(np.quantile(pv.max(1),.05)); yt=y[sp=='test']; base=m.predict(X[sp=='test']); pk=m.predict_proba(X[sp=='test'])
 ur=load(root,unknown_test=True); Xu=feats([r[2] for r in ur]); yu=np.array([r[0] for r in ur]); pu=m.predict_proba(Xu)
 out={'D6':{'threshold':thr,'rule':'5th percentile max validation class probability','known_test_acceptance':float((pk.max(1)>=thr).mean()),'unknown_test_rejection':float((pu.max(1)<thr).mean()),'unknown_test_n':len(yu),'unknown_devices':len(set(yu))},'D7':{}}
 raw=np.stack([np.asarray(s,dtype=np.complex128) for _,_,s in rows if False]) if False else None
 # Reconstruct complex samples from the same frozen known-test rows.
 z=np.stack([np.asarray(s,dtype=np.complex128) for d,i,s in rows if deterministic_split(str(d),i)=='test'])
 rng=np.random.default_rng(20260830)
 for db in [-6,-3,3,6]: out['D7'][f'gain_{db:+dB}']=metrics(yt,m.predict(feats(z*10**(db/20))))
 for snr in [20,10,5,0]:
  p=np.mean(np.abs(z)**2,axis=1,keepdims=True); n=(rng.normal(size=z.shape)+1j*rng.normal(size=z.shape))*np.sqrt(p/(10**(snr/10))/2); out['D7'][f'awgn_{snr}dB']=metrics(yt,m.predict(feats(z+n)))
 return out
if __name__=='__main__':
 ap=argparse.ArgumentParser(); ap.add_argument('data_root',type=Path); ap.add_argument('--out',type=Path); a=ap.parse_args(); r=main(a.data_root); print(json.dumps(r,indent=2)); a.out and a.out.write_text(json.dumps(r,indent=2))
