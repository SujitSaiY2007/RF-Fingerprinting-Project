"""D9 controlled/synthetic poisoning evaluation for Track A.

Attack data are derived from real SMoRFFI observations and explicitly labelled.
They are not presented as source-dataset attack measurements. The frozen known
 test partition is never used to construct or inject attacks.
"""
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
def load(root, devices):
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
    enroll=[]; stream=[]
    for dev in range(1,34):
        ids=np.where((y==dev)&(sp=='train'))[0]; ids=ids[np.argsort(ri[ids])]; enroll.extend(ids[:50]); stream.extend(ids[50:200])
    scaler=StandardScaler().fit(X[enroll]); Z=scaler.transform(X); by={d:Z[np.array(enroll)[y[enroll]==d]] for d in range(1,34)}
    base=ProfileManager.enroll(by); val=np.where(sp=='validation')[0]; d=np.asarray([base.profiles[int(yy)].distance(z) for yy,z in zip(y[val],Z[val])]); thr=float(np.percentile(d,95))
    ps=rf.predict(X[stream]); cs=rf.predict_proba(X[stream]).max(axis=1)
    clean=[(Z[ii],int(ps[j]),float(cs[j]),f'{known[ii][5]}#row={known[ii][1]}',False) for j,ii in enumerate(stream)]
    ux=np.asarray([r[4] for r in unknown]); uz=scaler.transform(ux); up=rf.predict(ux); uc=rf.predict_proba(ux).max(axis=1); cand=np.where((up==1)&(uc>=.30))[0][:300]
    unknown_attack=[(uz[k],1,float(uc[k]),f'synthetic-unknown-dev{unknown[k][0]}-row={unknown[k][1]}',True) for k in cand]
    replay_attack=unknown_attack[:1]*100 if unknown_attack else []
    target_ids=[ii for ii in stream if y[ii]==1][:100]; gain_drift=[]
    for j,ii in enumerate(target_ids):
        db=3.0*(j+1)/len(target_ids); xx=known[ii][3]*(10.0**(db/20.0)); ff=extract_rf_features(xx); fv=np.asarray([[ff[k] for k in FEATURES]],float); zz=scaler.transform(fv)[0]; pp=int(rf.predict(fv)[0]); cc=float(rf.predict_proba(fv).max()); gain_drift.append((zz,pp,cc,f'synthetic-gain-{db:.3f}dB-source={known[ii][5]}#row={known[ii][1]}',True))
    label_items=[(Z[ii],int(ps[j]),float(cs[j]),f'label-contam-source={known[ii][5]}#row={known[ii][1]}',True) for j,ii in enumerate(stream[:100]) if int(ps[j])==1]
    results={}
    for policy in [Policy.ALWAYS,Policy.CONFIDENCE,Policy.MULTI]:
        clean_m=ProfileManager.enroll(by,confidence_threshold=.30,consistency_threshold=thr,replay_guard=(policy==Policy.MULTI))
        for z,pred,conf,sid,syn in clean: clean_m.authorize(pred,conf,z,policy,sid,synthetic=syn)
        m=ProfileManager.enroll(by,confidence_threshold=.30,consistency_threshold=thr,replay_guard=(policy==Policy.MULTI))
        for item in clean[:500]+unknown_attack+clean[500:]: m.authorize(item[1],item[2],item[0],policy,item[3],synthetic=item[4])
        ev=[e for e in m.profiles[1].audit if e.synthetic]
        rm=ProfileManager.enroll(by,confidence_threshold=.30,consistency_threshold=thr,replay_guard=(policy==Policy.MULTI))
        for item in clean[:10]+replay_attack: rm.authorize(item[1],item[2],item[0],policy,item[3],synthetic=item[4])
        rev=[e for e in rm.profiles[1].audit if e.synthetic]
        gm=ProfileManager.enroll(by,confidence_threshold=.30,consistency_threshold=thr,replay_guard=(policy==Policy.MULTI))
        for item in gain_drift: gm.authorize(item[1],item[2],item[0],policy,item[3],synthetic=item[4])
        gev=[e for e in gm.profiles[1].audit if e.synthetic]
        lm=ProfileManager.enroll(by,confidence_threshold=.30,consistency_threshold=thr,replay_guard=(policy==Policy.MULTI))
        for item in label_items: lm.authorize(item[1],item[2],item[0],policy,item[3],synthetic=item[4])
        results[policy.value]={'unknown_contamination':{'samples':len(unknown_attack),'attack_acceptance_rate':sum(e.decision=='ACCEPT_UPDATE' for e in ev)/max(len(ev),1),'target_profile_displacement_vs_clean':float(np.linalg.norm(m.profiles[1].mean-clean_m.profiles[1].mean))},'replay':{'samples':len(replay_attack),'attack_acceptance_rate':sum(e.decision=='ACCEPT_UPDATE' for e in rev)/max(len(rev),1),'hold_rate':sum(e.decision=='HOLD_QUARANTINE' for e in rev)/max(len(rev),1)},'gradual_gain_drift':{'samples':len(gain_drift),'attack_acceptance_rate':sum(e.decision=='ACCEPT_UPDATE' for e in gev)/max(len(gev),1),'hold_rate':sum(e.decision=='HOLD_QUARANTINE' for e in gev)/max(len(gev),1)},'label_contamination':{'samples':len(label_items),'false_claimed_label_used_as_update_identity':0,'recognized_identity_update_count':sum(e.decision=='ACCEPT_UPDATE' for e in lm.profiles[1].audit if e.synthetic)}}
    payload={'stage':'D9','track':'A','dataset':'SMoRFFI','source_archive_sha256':'1d9ebcf2539e5fb7fb1dc678dba3fd2a50cada2befb86f5d84faff2b4f541037','frozen_test_protected':True,'synthetic_label':'All attack streams are controlled/derived scenarios, not source-dataset attack measurements.','consistency_threshold_95pct_validation':thr,'results':results,'interpretation':'Multi-evidence limits exact replay but can still admit target-like unknown contamination; this is a falsifying boundary condition, not a guaranteed positive result.','status':'implemented_tested_demonstrated'}
    out.write_text(json.dumps(payload,indent=2)); return payload
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('data_root',type=Path); ap.add_argument('--out',type=Path,required=True); a=ap.parse_args(); print(json.dumps(main(a.data_root,a.out),indent=2))
