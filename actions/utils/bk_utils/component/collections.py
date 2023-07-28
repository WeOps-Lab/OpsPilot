# -*- coding: utf-8 -*-
"""Collections for component client"""
from .apis.bk_login import CollectionsBkLogin
from .apis.bk_paas import CollectionsBkPaas
from .apis.cc import CollectionsCC
from .apis.cmsi import CollectionsCMSI
from .apis.gse import CollectionsGSE
from .apis.iam import CollectionsIAM
from .apis.itsm import CollectionsITSM
from .apis.job import CollectionsJOB
from .apis.monitor import CollectionsMonitor
from .apis.nodeman import CollectionsNodeMan
from .apis.sops import CollectionsSOPS
from .apis.usermanage import CollectionsUSERMANAGE

# Available components
AVAILABLE_COLLECTIONS = {
    "bk_login": CollectionsBkLogin,
    "bk_paas": CollectionsBkPaas,
    "cc": CollectionsCC,
    "cmsi": CollectionsCMSI,
    "gse": CollectionsGSE,
    "itsm": CollectionsITSM,
    "job": CollectionsJOB,
    "sops": CollectionsSOPS,
    "usermanage": CollectionsUSERMANAGE,
    "nodeman": CollectionsNodeMan,
    "iam": CollectionsIAM,
    "monitor": CollectionsMonitor
}
