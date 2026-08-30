import numpy as np
from src.profile_evolution import Decision, Policy, ProfileManager

def make_manager():
    return ProfileManager.enroll({1: np.zeros((4,3)), 2: np.ones((4,3))*5}, confidence_threshold=0.30, consistency_threshold=2.0, replay_guard=True)

def test_recognition_is_separate_from_authorization():
    m=make_manager(); identity,_=m.recognize_profile(np.array([0.1,0.1,0.1])); assert identity==1
    event=m.authorize(1,0.9,np.array([0.1,0.1,0.1]),Policy.MULTI,'x'); assert event.decision==Decision.ACCEPT_UPDATE.value

def test_low_confidence_is_hold_not_reject():
    m=make_manager(); event=m.authorize(1,0.2,np.array([0.1,0.1,0.1]),Policy.CONFIDENCE,'x'); assert event.decision==Decision.HOLD.value; assert m.profiles[1].count==4

def test_unknown_identity_is_reject():
    m=make_manager(); event=m.authorize(99,0.99,np.array([0.1,0.1,0.1]),Policy.ALWAYS,'x'); assert event.decision==Decision.REJECT.value

def test_replay_guard_holds_second_occurrence():
    m=make_manager(); x=np.array([0.1,0.1,0.1]); a=m.authorize(1,0.9,x,Policy.MULTI,'x',synthetic=True); b=m.authorize(1,0.9,x,Policy.MULTI,'x-replay',synthetic=True); assert a.decision==Decision.ACCEPT_UPDATE.value; assert b.decision==Decision.HOLD.value; assert b.reason=='replay_detected'

def test_frozen_policy_never_updates():
    m=make_manager(); event=m.authorize(1,0.99,np.array([0.2,0.2,0.2]),Policy.FROZEN,'x'); assert event.decision==Decision.HOLD.value; assert m.profiles[1].count==4
