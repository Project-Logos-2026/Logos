import os
import json
from typing import Dict, Any, Optional
from .Utilities.Canonical_Hashing import compute_sha256, canonicalize_json

EP_LIB_ROOT = os.path.dirname(os.path.abspath(__file__))
AA_STORAGE = os.path.join(EP_LIB_ROOT, 'AA_Storage')
NON_CANONICAL_SMPS = os.path.join(EP_LIB_ROOT, 'Non-Canonical_SMPs')
INDEXES_MANIFESTS = os.path.join(EP_LIB_ROOT, 'Indexes_Manifests')

PERMISSIONS_PATH = os.path.join(INDEXES_MANIFESTS, 'AA_Write_Permissions_Registry.json')
AUDIT_LOG_PATH = os.path.join(INDEXES_MANIFESTS, 'Epistemic_Library_Audit_Log.json')

class FailClosed(Exception):
    pass

def _log_rejection(reason: str, context: Optional[Dict[str, Any]] = None):
    entry = {"reason": reason, "context": context}
    try:
        if os.path.exists(AUDIT_LOG_PATH):
            with open(AUDIT_LOG_PATH, 'r', encoding='utf-8') as f:
                log = json.load(f)
        else:
            log = []
    except Exception:
        log = []
    log.append(entry)
    with open(AUDIT_LOG_PATH, 'w', encoding='utf-8') as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

class Epistemic_Library_Router:
    @staticmethod
    def Store_NonCanonical_Smp(smp_core: dict, status: str):
        # Compute hash from immutable fields only
        smp_core_hash = compute_sha256(smp_core)
        smp_id = smp_core.get('Smp_Id')
        if not smp_id:
            _log_rejection('Missing Smp_Id', {'smp_core': smp_core})
            raise FailClosed('Missing Smp_Id')
        status_dir = os.path.join(NON_CANONICAL_SMPS, f'Status_{status}')
        if not os.path.exists(status_dir):
            _log_rejection('Invalid status', {'status': status})
            raise FailClosed('Invalid status')
        smp_key = smp_id.replace('/', '_')
        smp_path = os.path.join(status_dir, f'{smp_key}.smp.json')
        if os.path.exists(smp_path):
            with open(smp_path, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            existing_hash = compute_sha256(existing)
            if existing_hash != smp_core_hash:
                _log_rejection('Attempt to rewrite immutable SMP', {'smp_id': smp_id})
                raise FailClosed('Attempt to rewrite immutable SMP')
        else:
            with open(smp_path, 'w', encoding='utf-8') as f:
                json.dump(smp_core, f, indent=2, ensure_ascii=False)
        return {'Smp_Id': smp_id, 'Smp_Key': smp_key, 'Smp_Core_Hash': smp_core_hash, 'Smp_Path': smp_path}

    @staticmethod
    def Attach_NonCanonical_Aa(parent_smp_id: str, aa_payload: dict, aa_type: str, author_class: str, author_id: str, status_context: str):
        # Verify parent SMP exists
        found = False
        smp_key = parent_smp_id.replace('/', '_')
        for status in ['Provisional', 'Conditional', 'Rejected']:
            status_dir = os.path.join(NON_CANONICAL_SMPS, f'Status_{status}')
            smp_path = os.path.join(status_dir, f'{smp_key}.smp.json')
            if os.path.exists(smp_path):
                found = True
                break
        if not found:
            _log_rejection('Parent SMP not found', {'parent_smp_id': parent_smp_id})
            raise FailClosed('Parent SMP not found')
        # Verify write permission (strict fail-closed)
        with open(PERMISSIONS_PATH, 'r', encoding='utf-8') as f:
            registry = json.load(f)
        allowed = registry.get('Allowed', {})
        # Validate author class exists
        if author_class not in allowed:
            _log_rejection('Unauthorized author class', {
                'author_class': author_class,
                'author_id': author_id,
                'aa_type': aa_type
            })
            raise FailClosed('Unauthorized AA type')
        class_permissions = allowed.get(author_class)
        # AGENT permissions are dict[author_id] -> list[aa_types]
        if isinstance(class_permissions, dict):
            if author_id not in class_permissions:
                _log_rejection('Unauthorized author id', {
                    'author_class': author_class,
                    'author_id': author_id,
                    'aa_type': aa_type
                })
                raise FailClosed('Unauthorized AA type')
            allowed_types = class_permissions.get(author_id, [])
            if aa_type not in allowed_types:
                _log_rejection('Unauthorized AA type', {
                    'author_class': author_class,
                    'author_id': author_id,
                    'aa_type': aa_type
                })
                raise FailClosed('Unauthorized AA type')
        # PROTOCOL permissions are list[str]
        elif isinstance(class_permissions, list):
            if aa_type not in class_permissions:
                _log_rejection('Unauthorized AA type', {
                    'author_class': author_class,
                    'author_id': author_id,
                    'aa_type': aa_type
                })
                raise FailClosed('Unauthorized AA type')
        else:
            _log_rejection('Invalid permission registry structure', {
                'author_class': author_class
            })
            raise FailClosed('Unauthorized AA type')
        # Verify parent SMP exists
        found = False
        smp_key = parent_smp_id.replace('/', '_')
        for status in ['Provisional', 'Conditional', 'Rejected']:
            status_dir = os.path.join(NON_CANONICAL_SMPS, f'Status_{status}')
            smp_path = os.path.join(status_dir, f'{smp_key}.smp.json')
            if os.path.exists(smp_path):
                found = True
                break
        if not found:
            _log_rejection('Parent SMP not found', {'parent_smp_id': parent_smp_id})
            raise FailClosed('Parent SMP not found')
        # Verify write permission (strict fail-closed)
        with open(PERMISSIONS_PATH, 'r', encoding='utf-8') as f:
            registry = json.load(f)
        allowed = registry.get('Allowed', {})
        # Validate author class exists
        if author_class not in allowed:
            _log_rejection('Unauthorized author class', {
                'author_class': author_class,
                'author_id': author_id,
                'aa_type': aa_type
            })
            raise FailClosed('Unauthorized AA type')
        class_permissions = allowed.get(author_class)
        # AGENT permissions are dict[author_id] -> list[aa_types]
        if isinstance(class_permissions, dict):
            if author_id not in class_permissions:
                _log_rejection('Unauthorized author id', {
                    'author_class': author_class,
                    'author_id': author_id,
                    'aa_type': aa_type
                })
                raise FailClosed('Unauthorized AA type')
            allowed_types = class_permissions.get(author_id, [])
            if aa_type not in allowed_types:
                _log_rejection('Unauthorized AA type', {
                    'author_class': author_class,
                    'author_id': author_id,
                    'aa_type': aa_type
                })
                raise FailClosed('Unauthorized AA type')
        # PROTOCOL permissions are list[str]
        elif isinstance(class_permissions, list):
            if aa_type not in class_permissions:
                _log_rejection('Unauthorized AA type', {
                    'author_class': author_class,
                    'author_id': author_id,
                    'aa_type': aa_type
                })
                raise FailClosed('Unauthorized AA type')
        else:
            _log_rejection('Invalid permission registry structure', {
                'author_class': author_class
            })
            raise FailClosed('Unauthorized AA type')
        # Compute AA hash
        aa_content_hash = compute_sha256(aa_payload)
        aa_id = aa_payload.get('Aa_Id')
        if not aa_id:
            _log_rejection('Missing Aa_Id', {'aa_payload': aa_payload})
            raise FailClosed('Missing Aa_Id')
        # Directory-safe Smp_Key
        aa_dir = os.path.join(AA_STORAGE, f'{author_class}_AAs', smp_key, 'AAs', aa_type)
        os.makedirs(aa_dir, exist_ok=True)
        aa_path = os.path.join(aa_dir, f'{aa_id}.aa.json')
        if os.path.exists(aa_path):
            with open(aa_path, 'r', encoding='utf-8') as f:
                existing = json.load(f)
            existing_hash = compute_sha256(existing)
            if existing_hash != aa_content_hash:
                _log_rejection('Attempt to overwrite AA', {'aa_id': aa_id})
                raise FailClosed('Attempt to overwrite AA')
        else:
            with open(aa_path, 'w', encoding='utf-8') as f:
                json.dump(aa_payload, f, indent=2, ensure_ascii=False)
        # Chain hash enforcement
        prev_chain_hash = aa_payload.get('Prev_AA_Chain_Hash')
        index_path = os.path.join(INDEXES_MANIFESTS, 'Smp_AA_Indexes', smp_key, 'Smp_AA_Index.json')
        os.makedirs(os.path.dirname(index_path), exist_ok=True)
        if os.path.exists(index_path):
            with open(index_path, 'r', encoding='utf-8') as f:
                index = json.load(f)
            current_head = index.get('Current_Chain_Head_Hash')
            if prev_chain_hash != current_head:
                _log_rejection('Chain hash mismatch', {'aa_id': aa_id, 'prev_chain_hash': prev_chain_hash, 'current_head': current_head})
                raise FailClosed('Chain hash mismatch')
        else:
            index = {
                'Smp_Id': parent_smp_id,
                'Smp_Key': smp_key,
                'Smp_Core_Hash': None,
                'Current_Chain_Head_Hash': None,
                'Attachments': []
            }
        # Update index
        attachment = {
            'Aa_Id': aa_id,
            'Aa_Type': aa_type,
            'Author_Class': author_class,
            'Author_Id': author_id,
            'Created_At': aa_payload.get('Created_At'),
            'Aa_Content_Hash': aa_content_hash,
            'Parent_Smp_Core_Hash': None,
            'Path': aa_path,
            'Supersedes_AA_Id': aa_payload.get('Supersedes_AA_Id'),
            'Prev_AA_Chain_Hash': prev_chain_hash,
            'Status_At_Time_Of_Attachment': status_context
        }
        index['Attachments'].append(attachment)
        index['Current_Chain_Head_Hash'] = aa_content_hash
        with open(index_path, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
        return {'Aa_Id': aa_id, 'Aa_Content_Hash': aa_content_hash, 'Aa_Path': aa_path, 'Index_Path': index_path}
