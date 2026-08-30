"""Track-A D5 classical RF-feature baseline.

Uses the frozen D2 2x288 I/Q input, deterministic D2 split, and the current
repository D3 interpretable feature extractor. This is intentionally a fixed
Random Forest baseline, not a hyperparameter search and not a reconstruction
of the historical ~60-feature experiment.
"""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, balanced_accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.smorffi_d2 import deterministic_split, parse_canonical_preamble
from src.smorffi_d3 import extract_rf_features

DEFAULT_SEED = 20260830

def load_track_a(root: Path):
    rows=[]
    for p in sorted(root.glob('*.csv')):
        with p.open('r', encoding='utf-8-sig', newline='') as f:
            for idx, row in enumerate(csv.DictReader(f)):
                dev=int(row['Device Number'])
                if 1 <= dev <= 33:
                    parsed=parse_canonical_preamble(row['preamble'])
                    feats=extract_rf_features(parsed.samples)
                    rows.append((dev, idx, deterministic_split(str(dev), idx), feats, p.name))
    keys=list(rows[0][3].keys())
    X=np.asarray([[r[3][k] for k in keys] for r in rows], dtype=np.float64)
    y=np.asarray([r[0] for r in rows])
    split=np.asarray([r[2] for r in rows])
    return X,y,split,keys,rows

def evaluate(root: Path, seed: int = DEFAULT_SEED):
    X,y,split,keys,rows=load_track_a(root)
    model=RandomForestClassifier(n_estimators=100, random_state=seed, n_jobs=-1, max_features='sqrt', class_weight=None)
    model.fit(X[split=='train'], y[split=='train'])
    yt=y[split=='test']; pred=model.predict(X[split=='test'])
    labels=list(range(1,34))
    pr,re,f1,support=precision_recall_fscore_support(yt,pred,labels=labels,zero_division=0)
    return {
      'dataset': {'devices':'1-33','rows':int(len(y)),'train':int((split=='train').sum()),'validation':int((split=='validation').sum()),'test':int((split=='test').sum())},
      'feature_set': {'count':len(keys),'names':keys,'source':'src/smorffi_d3.py'},
      'model': {'type':'RandomForestClassifier','n_estimators':100,'random_state':seed,'max_features':'sqrt','class_weight':None,'tuning':False},
      'metrics': {'accuracy':float(accuracy_score(yt,pred)),'macro_f1':float(f1_score(yt,pred,average='macro')),'balanced_accuracy':float(balanced_accuracy_score(yt,pred))},
      'per_device': {str(c):{'precision':float(pr[i]),'recall':float(re[i]),'f1':float(f1[i]),'support':int(support[i])} for i,c in enumerate(labels)},
      'confusion_matrix': confusion_matrix(yt,pred,labels=labels).tolist(),
      'feature_importance': {k:float(v) for k,v in sorted(zip(keys,model.feature_importances_),key=lambda z:-z[1])},
      'historical_comparison': {'reported_accuracy':0.9112,'historical_feature_count':'~60','status':'not exactly reproduced because the historical ~60-feature list, exact 10186-row selection and historical configuration are unavailable'},
    }

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('data_root',type=Path); ap.add_argument('--out',type=Path,default=None); args=ap.parse_args()
    result=evaluate(args.data_root)
    text=json.dumps(result,indent=2)
    if args.out: args.out.write_text(text)
    print(text)
