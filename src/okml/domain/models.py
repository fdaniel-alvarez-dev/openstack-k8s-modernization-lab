from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class IncidentRecord(BaseModel):
    occurred_on: date
    severity: Literal["sev1", "sev2", "sev3"]
    minutes_to_restore: int = Field(ge=1, le=60 * 24 * 14)
    primary_cause: str


class ProvisioningStep(BaseModel):
    name: str
    minutes_p50: float = Field(gt=0)
    manual_touchpoints: int = Field(ge=0)
    error_rate_percent: float = Field(ge=0, le=100)


class LegacyCompute(BaseModel):
    hypervisor: Literal["kvm", "vmware", "mixed"] = "mixed"
    compute_nodes: int = Field(ge=1)
    overcommit_ratio: float = Field(gt=1.0, le=10.0)
    patch_cadence_days: int = Field(ge=1, le=365)


class LegacyStorage(BaseModel):
    primary_backend: Literal["ceph", "nfs", "vendor_san", "mixed"] = "mixed"
    replication_enabled: bool = True
    backup_success_rate_percent: float = Field(ge=0, le=100)


class LegacyNetwork(BaseModel):
    segmentation: Literal["vlan", "vxlan", "mixed"] = "mixed"
    east_west_visibility: Literal["low", "medium", "high"] = "low"
    change_failure_rate_percent: float = Field(ge=0, le=100)


class LegacyControlPlane(BaseModel):
    openstack_release: str
    ha_enabled: bool
    db_clustered: bool
    message_bus_clustered: bool
    upgrade_strategy: Literal["in_place", "blue_green", "unknown"] = "unknown"


class LegacyTenancy(BaseModel):
    tenants: int = Field(ge=1)
    self_service_portal: bool
    rbac_maturity: Literal["ad_hoc", "role_based", "policy_as_code"] = "ad_hoc"


class LegacyEnvironment(BaseModel):
    name: str
    region: str
    compute: LegacyCompute
    storage: LegacyStorage
    network: LegacyNetwork
    control_plane: LegacyControlPlane
    tenancy: LegacyTenancy

    deployments_per_week: int = Field(ge=0)
    infra_changes_per_week: int = Field(ge=0)
    config_drift_rate_percent: float = Field(ge=0, le=100)

    incidents_last_90d: list[IncidentRecord] = Field(default_factory=list)
    provisioning_workflow: list[ProvisioningStep]


class AssessmentScores(BaseModel):
    reliability_risk: float = Field(ge=0, le=100)
    operational_maturity: float = Field(ge=0, le=100)
    automation_maturity: float = Field(ge=0, le=100)
    standardization: float = Field(ge=0, le=100)


class RoadmapItem(BaseModel):
    id: str
    title: str
    rationale: str
    effort: Literal["S", "M", "L"]
    impact: Literal["M", "H"]
    risk_reduction: Literal["M", "H"]
    priority: int = Field(ge=1)
    tags: list[str] = Field(default_factory=list)


class AssessmentReport(BaseModel):
    env: LegacyEnvironment
    scores: AssessmentScores
    findings: list[str]
    recommendations: list[RoadmapItem]
