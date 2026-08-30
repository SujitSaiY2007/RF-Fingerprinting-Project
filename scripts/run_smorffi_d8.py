"""D8 Track-A profile-evolution experiment.

Uses real SMoRFFI observations (devices 1-33) and the frozen D2 split. The
training partition is divided by source-row index into an enrollment segment
and a later engineering update stream. This is not a temporal claim. The
frozen test partition is never passed to the profile update path.
"""
from __future__ import annotations
import argparse, csv, json, sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.smorffi_d2 import parse_preamble, deterministic_split
from src.smorffi_d3 import extract_rf_features
from src.profile_evolution import ProfileManager, Policy

SEED=20260830
DEVICES=range(1,34)
FEATURES=list(extract_rf_features(np.zeros(288,dtype=complex)).keys())

def load(root:Path):
    rows=[]
    for p in sorted(root.glob('*.csv')):
        with p.open('r',encoding='utf-8-sig',newline='') as f:
            for idx,row in enumerate(csv.DictReader(f)):
                dev=int(row['Device Number'])
                if dev in DEVICES:
                    x=np.asarray(parse_preamble(row['preamble'])[:288],dtype=np.complex128)
                    feat=extract_rf_features(x)
                    rows.append((dev,idx,deterministic_split(str(dev),idx),np.asarray([feat[k] for k in FEATURES],float),p.name))
    return rows

def profile_accuracy(manager,X,y):
    return float(accuracy_score(y,[manager.recognize_profile(x)[0] for x in X]))

def run(root:Path,out:Path):
    rows=load(root); X=np.asarray([r[3] for r in rows]); y=np.asarray([r[0] for r in rows]); split=np.asarray([r[2] for r in rows]); source=np.asarray([r[1] for r in rows])
    rf=RandomForestClassifier(n_estimators=100,random_state=SEED,n_jobs=-1,max_features='sqrt',class_weight=None).fit(X[split=='train'],y[split=='train'])
    enroll=[]; stream=[]
    for dev in DEVICES:
        ids=np.where((y==dev)&(split=='train'))[0]; ids=ids[np.argsort(source[ids])]; enroll.extend(ids[:50]); stream.extend(ids[50:200])
    scaler=StandardScaler().fit(X[enroll]); Z=scaler.transform(X)
    by={d:Z[np.array(enroll)[y[enroll]==d]] for d in DEVICES}
    base=ProfileManager.enroll(by)
    val=np.where(split=='validation')[0]
    val_dist=np.asarray([base.profiles[int(yy)].distance(z) for yy,z in zip(y[val],Z[val])])
    consistency_threshold=float(np.percentile(val_dist,95))
    test=np.where(split=='test')[0]
    stream_pred=rf.predict(X[stream]); stream_conf=rf.predict_proba(X[stream]).max(axis=1)
    results={}
    for policy in [Policy.FROZEN,Policy.ALWAYS,Policy.CONFIDENCE,Policy.MULTI]:
        m=ProfileManager.enroll(by,confidence_threshold=.30,consistency_threshold=consistency_threshold,replay_guard=(policy==Policy.MULTI))
        events=[]
        for j,ii in enumerate(stream):
            events.append(m.authorize(int(stream_pred[j]),float(stream_conf[j]),Z[ii],policy,f'{rows[ii][4]}#row={rows[ii][1]}',synthetic=False,source_index=int(rows[ii][1])))
        results[policy.value]={
            'frozen_test_profile_accuracy_before_stream':profile_accuracy(ProfileManager.enroll(by,confidence_threshold=.30,consistency_threshold=consistency_threshold),Z[test],y[test]),
            'frozen_test_profile_accuracy_after_stream':profile_accuracy(m,Z[test],y[test]),
            'update_events':sum(e.decision=='ACCEPT_UPDATE' for e in events),
            'hold_events':sum(e.decision=='HOLD_QUARANTINE' for e in events),
            'reject_events':sum(e.decision=='REJECT' for e in events),
            'profile_state_digest':m.state_digest()}
    payload={'stage':'D8','track':'A','dataset':'SMoRFFI','synthetic':False,'source_archive_sha256':'1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037','known_devices':'1-33','rows':len(rows),'enrollment_per_device':50,'update_stream_per_device':150,'stream_order':'source_row_index ascending within device; not claimed temporal','frozen_evaluation':'test partition selected before stream and never used for updates','scaler_fit':'enrollment only','confidence_threshold':0.30,'consistency_threshold_95pct_validation':consistency_threshold,'results':results,'status':'implemented_tested_demonstrated','provenance':'real SMoRFFI observations; no synthetic transformations in D8 core run','recognition_note':'Local fixed-RF execution is an interface input only; it does not revise the canonical recorded D5 87.39% metric.'}
    out.write_text(json.dumps(payload,indent=2)); return payload

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('data_root',type=Path); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(); print(json.dumps(run(a.data_root,a.out),indent=2))
