import os
import shutil
import json
import pytest
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.Logos_Agent_Resources.Epistemic_Library.Epistemic_Library_Router import Epistemic_Library_Router, FailClosed
from LOGOS_SYSTEM.RUNTIME_CORES.RUNTIME_EXECUTION_CORE.Logos_Core.Logos_Protocol.Logos_Agent_Resources.Epistemic_Library.Utilities.Canonical_Hashing import compute_sha256

TEST_ROOT = os.path.dirname(os.path.abspath(__file__))
EP_LIB_ROOT = os.path.dirname(TEST_ROOT)
AA_STORAGE = os.path.join(EP_LIB_ROOT, 'AA_Storage')
NON_CANONICAL_SMPS = os.path.join(EP_LIB_ROOT, 'Non-Canonical_SMPs')
INDEXES_MANIFESTS = os.path.join(EP_LIB_ROOT, 'Indexes_Manifests')
PERMISSIONS_PATH = os.path.join(INDEXES_MANIFESTS, 'AA_Write_Permissions_Registry.json')

@pytest.fixture(autouse=True)
def clean_test_artifacts():
    # Remove test SMPs and AAs before and after each test
    for d in ['Agent_AAs', 'Protocol_AAs']:
        p = os.path.join(AA_STORAGE, d)
        if os.path.exists(p):
            shutil.rmtree(p)
    for status in ['Status_Provisional', 'Status_Conditional', 'Status_Rejected', 'Statues_Rejected']:
        p = os.path.join(NON_CANONICAL_SMPS, status)
        for f in os.listdir(p):
            if f.startswith('TEST_SMP_'):
                os.remove(os.path.join(p, f))
    index_dir = os.path.join(INDEXES_MANIFESTS, 'Smp_AA_Indexes')
    for smp_key in os.listdir(index_dir):
        if smp_key.startswith('TEST_SMP_'):
            shutil.rmtree(os.path.join(index_dir, smp_key))
    yield
    # Clean up again after test
    for d in ['Agent_AAs', 'Protocol_AAs']:
        p = os.path.join(AA_STORAGE, d)
        if os.path.exists(p):
            shutil.rmtree(p)
    for status in ['Status_Provisional', 'Status_Conditional', 'Status_Rejected', 'Statues_Rejected']:
        p = os.path.join(NON_CANONICAL_SMPS, status)
        for f in os.listdir(p):
            if f.startswith('TEST_SMP_'):
                os.remove(os.path.join(p, f))
    index_dir = os.path.join(INDEXES_MANIFESTS, 'Smp_AA_Indexes')
    for smp_key in os.listdir(index_dir):
        if smp_key.startswith('TEST_SMP_'):
            shutil.rmtree(os.path.join(index_dir, smp_key))

def test_smp_core_storage():
    smp_core = {'Smp_Id': 'TEST_SMP_1', 'immutable_field': 'abc'}
    result = Epistemic_Library_Router.Store_NonCanonical_Smp(smp_core, 'Provisional')
    smp_path = result['Smp_Path']
    assert os.path.exists(smp_path)
    with open(smp_path, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    assert compute_sha256(loaded) == result['Smp_Core_Hash']
    # Attempt overwrite with different core
    smp_core2 = {'Smp_Id': 'TEST_SMP_1', 'immutable_field': 'xyz'}
    with pytest.raises(FailClosed):
        Epistemic_Library_Router.Store_NonCanonical_Smp(smp_core2, 'Provisional')

def test_aa_attachment_chain_hashing():
    smp_core = {'Smp_Id': 'TEST_SMP_2', 'immutable_field': 'abc'}
    Epistemic_Library_Router.Store_NonCanonical_Smp(smp_core, 'Provisional')
    aa1 = {'Aa_Id': 'AA1', 'Created_At': '2026-02-24T00:00:00Z', 'Prev_AA_Chain_Hash': None}
    aa2 = {'Aa_Id': 'AA2', 'Created_At': '2026-02-24T00:01:00Z', 'Prev_AA_Chain_Hash': None}
    # Patch registry on disk
    with open(PERMISSIONS_PATH, 'r', encoding='utf-8') as f:
        original_reg = json.load(f)
    reg = original_reg.copy()
    reg['Allowed'].setdefault('AGENT', {})
    reg['Allowed']['AGENT']['TEST'] = ['AA1', 'AA2', 'AA3']
    with open(PERMISSIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
    try:
        res1 = Epistemic_Library_Router.Attach_NonCanonical_Aa('TEST_SMP_2', aa1, 'AA1', 'AGENT', 'TEST', 'Provisional')
        index_path = res1['Index_Path']
        with open(index_path, 'r', encoding='utf-8') as f:
            index = json.load(f)
        assert index['Current_Chain_Head_Hash'] == res1['Aa_Content_Hash']
        aa2['Prev_AA_Chain_Hash'] = res1['Aa_Content_Hash']
        res2 = Epistemic_Library_Router.Attach_NonCanonical_Aa('TEST_SMP_2', aa2, 'AA2', 'AGENT', 'TEST', 'Provisional')
        with open(index_path, 'r', encoding='utf-8') as f:
            index2 = json.load(f)
        assert aa2['Prev_AA_Chain_Hash'] == res1['Aa_Content_Hash']
        assert index2['Current_Chain_Head_Hash'] == res2['Aa_Content_Hash']
        # Manual chain mismatch
        aa3 = {'Aa_Id': 'AA3', 'Created_At': '2026-02-24T00:02:00Z', 'Prev_AA_Chain_Hash': 'bad_hash'}
        with pytest.raises(FailClosed):
            Epistemic_Library_Router.Attach_NonCanonical_Aa('TEST_SMP_2', aa3, 'AA3', 'AGENT', 'TEST', 'Provisional')
    finally:
        with open(PERMISSIONS_PATH, 'w', encoding='utf-8') as f:
            json.dump(original_reg, f, indent=2, ensure_ascii=False)

def test_permission_registry_enforcement():
    smp_core = {'Smp_Id': 'TEST_SMP_3', 'immutable_field': 'abc'}
    Epistemic_Library_Router.Store_NonCanonical_Smp(smp_core, 'Provisional')
    aa = {'Aa_Id': 'AA1', 'Created_At': '2026-02-24T00:00:00Z', 'Prev_AA_Chain_Hash': None}
    with open(PERMISSIONS_PATH, 'r', encoding='utf-8') as f:
        original_reg = json.load(f)
    reg = original_reg.copy()
    reg['Allowed'].setdefault('AGENT', {})
    reg['Allowed']['AGENT'].pop('TEST', None)
    with open(PERMISSIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
    try:
        with pytest.raises(FailClosed):
            Epistemic_Library_Router.Attach_NonCanonical_Aa('TEST_SMP_3', aa, 'AA1', 'AGENT', 'TEST', 'Provisional')
    finally:
        with open(PERMISSIONS_PATH, 'w', encoding='utf-8') as f:
            json.dump(original_reg, f, indent=2, ensure_ascii=False)

def test_parent_smp_validation():
    aa = {'Aa_Id': 'AA1', 'Created_At': '2026-02-24T00:00:00Z', 'Prev_AA_Chain_Hash': None}
    with pytest.raises(FailClosed):
        Epistemic_Library_Router.Attach_NonCanonical_Aa('NONEXISTENT_SMP', aa, 'AA1', 'AGENT', 'TEST', 'Provisional')

def test_alias_behavior():
    smp_core = {'Smp_Id': 'TEST_SMP_4', 'immutable_field': 'abc'}
    Epistemic_Library_Router.Store_NonCanonical_Smp(smp_core, 'Rejected')
    smp_key = smp_core['Smp_Id'].replace('/', '_')
    rejected_dir = os.path.join(NON_CANONICAL_SMPS, 'Status_Rejected')
    smp_path = os.path.join(rejected_dir, f'{smp_key}.smp.json')
    assert os.path.exists(smp_path)
    # Check alias mapping in manifest
    manifest_path = os.path.join(INDEXES_MANIFESTS, 'Epistemic_Library_Manifest.json')
    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    assert 'Statues_Rejected' in manifest.get('Alias_Mapping', {})

def test_deterministic_hash_consistency():
    smp_core = {'Smp_Id': 'TEST_SMP_5', 'immutable_field': 'abc'}
    h1 = compute_sha256(smp_core)
    h2 = compute_sha256(smp_core)
    assert h1 == h2
    aa = {'Aa_Id': 'AA1', 'Created_At': '2026-02-24T00:00:00Z', 'Prev_AA_Chain_Hash': None}
    h3 = compute_sha256(aa)
    h4 = compute_sha256(aa)
    assert h3 == h4

def test_append_only_enforcement():
    smp_core = {'Smp_Id': 'TEST_SMP_6', 'immutable_field': 'abc'}
    Epistemic_Library_Router.Store_NonCanonical_Smp(smp_core, 'Provisional')
    aa = {'Aa_Id': 'AA1', 'Created_At': '2026-02-24T00:00:00Z', 'Prev_AA_Chain_Hash': None}
    with open(PERMISSIONS_PATH, 'r', encoding='utf-8') as f:
        original_reg = json.load(f)
    reg = original_reg.copy()
    reg['Allowed'].setdefault('AGENT', {})
    reg['Allowed']['AGENT']['TEST'] = ['AA1']
    with open(PERMISSIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(reg, f, indent=2, ensure_ascii=False)
    try:
        Epistemic_Library_Router.Attach_NonCanonical_Aa('TEST_SMP_6', aa, 'AA1', 'AGENT', 'TEST', 'Provisional')
        # Attempt to modify existing AA file
        aa_mod = {'Aa_Id': 'AA1', 'Created_At': '2026-02-24T00:00:01Z', 'Prev_AA_Chain_Hash': None}
        with pytest.raises(FailClosed):
            Epistemic_Library_Router.Attach_NonCanonical_Aa('TEST_SMP_6', aa_mod, 'AA1', 'AGENT', 'TEST', 'Provisional')
    finally:
        with open(PERMISSIONS_PATH, 'w', encoding='utf-8') as f:
            json.dump(original_reg, f, indent=2, ensure_ascii=False)
