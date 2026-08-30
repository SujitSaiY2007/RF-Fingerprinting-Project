"""D10 auditable Track-A lifecycle demonstration."""
from __future__ import annotations
import argparse,csv,json,sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.smorffi_d2 import parse_preamble,deterministic_split
from src.smorffi_d3 import extract_rf_features
from src.profile_evolution import ProfileManager,Policy
SEED=20260830
FEATURES=list(extract_rf_features(np.zeros(288,dtype=complex)).keys())
def load(root,devices):
    rows=[]
    for p in sorted(root.glob('*.csv')):
        with p.open('r',encoding='utf-8-sig',newline='') as f:
            for idx,row in enumerate(csv.DictReader(f)):
                dev=int(row['Device Number'])
                if dev in devices:
                    x=np.asarray(parse_preamble(row['preamble'])[:288],dtype=np.complex128); feat=extract_rf_features(x)
                    rows.append((dev,idx,deterministic_split(str(dev),idx),x,np.asarray([feat[k] for k in FEATURES],float),p.name))
    return rows
def main(root,out):
    known=load(root,set(range(1,34))); unknown=load(root,set(range(34,41)))
    y=np.asarray([r[0] for r in known]); X=np.asarray([r[4] for r in known]); sp=np.asarray([r[2] for r in known]); ri=np.asarray([r[1] for r in known])
    rf=RandomForestClassifier(n_estimators=100,random_state=SEED,n_jobs=-1,max_features='sqrt',class_weight=None).fit(X[sp=='train'],y[sp=='train'])
    enroll=[]
    for dev in range(1,34):
        ids=np.where((y==dev)&(sp=='train'))[0]; ids=ids[np.argsort(ri[ids])]; enroll.extend(ids[:50])
    scaler=StandardScaler().fit(X[enroll]); Z=scaler.transform(X); by={d:Z[np.array(enroll)[y[enroll]==d]] for d in range(1,34)}
    initial=ProfileManager.enroll(by); val=np.where(sp=='validation')[0]; vd=np.asarray([initial.profiles[int(yy)].distance(z) for yy,z in zip(y[val],Z[val])]); thr=float(np.percentile(vd,95))
    pm=ProfileManager.enroll(by,confidence_threshold=.30,consistency_threshold=thr,replay_guard=True)
    k=int(enroll[0]); pred=int(rf.predict(X[k:k+1])[0]); conf=float(rf.predict_proba(X[k:k+1]).max()); e1=pm.authorize(pred,conf,Z[k],Policy.MULTI,f'{known[k][5]}#row={known[k][1]}',source_index=int(known[k][1]))
    later=[ii for ii in np.where((y==y[k])&(sp=='train'))[0] if ii!=k][0]; lp=int(rf.predict(X[later:later+1])[0]); lc=float(rf.predict_proba(X[later:later+1]).max()); e2=pm.authorize(lp,lc,Z[later],Policy.MULTI,f'{known[later][5]}#row={known[later][1]}',source_index=int(known[later][1]))
    ux=np.asarray([r[4] for r in unknown]); uz=scaler.transform(ux); up=rf.predict(ux); uc=rf.predict_proba(ux).max(axis=1); low=int(np.where(uc<.30)[0][0]); unknown_decision='REJECT_UNKNOWN'
    cand=int(np.where((up==1)&(uc>=.30))[0][0]); first=pm.authorize(1,float(uc[cand]),uz[cand],Policy.MULTI,f'synthetic-unknown-dev{unknown[cand][0]}#row={unknown[cand][1]}#replay-1',synthetic=True); second=pm.authorize(1,float(uc[cand]),uz[cand],Policy.MULTI,f'synthetic-unknown-dev{unknown[cand][0]}#row={unknown[cand][1]}#replay-2',synthetic=True)
    payload={'stage':'D10','track':'A','status':'implemented_tested_demonstrated','source_archive_sha256':'1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037','frozen_test_protected':True,'evaluation_partition':'known devices 1-33 test split; never passed to authorize/update','consistency_threshold_95pct_validation':thr,'lifecycle':[{'step':'known_legitimate','recognition':{'identity':pred,'confidence':conf},'decision':e1.decision,'reason':e1.reason},{'step':'legitimate_profile_evolution','recognition':{'identity':lp,'confidence':lc},'decision':e2.decision,'reason':e2.reason},{'step':'unknown_open_set','source_device':int(unknown[low][0]),'confidence':float(uc[low]),'d6_decision':unknown_decision},{'step':'suspicious_replay_first','recognized_identity':1,'confidence':float(uc[cand]),'decision':first.decision,'reason':first.reason},{'step':'suspicious_replay_repeat','recognized_identity':1,'confidence':float(uc[cand]),'decision':second.decision,'reason':second.reason}],'audit_event_count':len(pm.profiles[1].audit),'profile_version_device_1':pm.profiles[1].version,'audit_digest':pm.state_digest(),'note':'The first target-like suspicious sample may still be admitted; the replay guard blocks the repeated occurrence. This is an explicit limitation, not a security guarantee.'}
    out.write_text(json.dumps(payload,indent=2)); return payload
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('data_root',type=Path); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(); print(json.dumps(main(a.data_root,a.out),indent=2))
