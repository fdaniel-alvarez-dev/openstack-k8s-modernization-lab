from __future__ import annotations

from okml.domain.models import AssessmentScores, LegacyEnvironment


def _clamp(x: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, x))


def score_environment(env: LegacyEnvironment) -> AssessmentScores:
    incidents = env.incidents_last_90d
    sev1 = sum(1 for i in incidents if i.severity == "sev1")
    sev2 = sum(1 for i in incidents if i.severity == "sev2")
    mttr_avg = (
        (sum(i.minutes_to_restore for i in incidents) / len(incidents)) if incidents else 30.0
    )

    prov_manual = sum(s.manual_touchpoints for s in env.provisioning_workflow)
    prov_error = sum(s.error_rate_percent for s in env.provisioning_workflow) / max(
        1, len(env.provisioning_workflow)
    )

    reliability_risk = 15.0
    reliability_risk += sev1 * 12 + sev2 * 6
    reliability_risk += (mttr_avg / 60.0) * 10
    reliability_risk += 8 if not env.control_plane.ha_enabled else 0
    reliability_risk += 5 if not env.control_plane.db_clustered else 0
    reliability_risk += 4 if not env.control_plane.message_bus_clustered else 0
    reliability_risk += (env.network.change_failure_rate_percent / 100.0) * 12
    reliability_risk += (100.0 - env.storage.backup_success_rate_percent) * 0.08
    reliability_risk = _clamp(reliability_risk)

    operational_maturity = 55.0
    operational_maturity -= sev1 * 5
    operational_maturity -= (env.config_drift_rate_percent / 100.0) * 18
    operational_maturity -= (
        8 if env.control_plane.upgrade_strategy in {"unknown", "in_place"} else 0
    )
    operational_maturity += 7 if env.control_plane.ha_enabled else -5
    operational_maturity += 5 if env.storage.replication_enabled else -6
    operational_maturity += 6 if env.network.east_west_visibility in {"medium", "high"} else -5
    operational_maturity = _clamp(operational_maturity)

    automation_maturity = 40.0
    automation_maturity -= min(18.0, prov_manual * 1.5)
    automation_maturity -= min(12.0, prov_error * 0.6)
    automation_maturity += min(12.0, env.infra_changes_per_week * 1.2)
    automation_maturity += 10 if env.tenancy.self_service_portal else -8
    automation_maturity = _clamp(automation_maturity)

    standardization = 45.0
    standardization += 8 if env.compute.hypervisor != "mixed" else -6
    standardization += 6 if env.network.segmentation != "mixed" else -4
    standardization += 8 if env.tenancy.rbac_maturity in {"role_based", "policy_as_code"} else -6
    standardization += 6 if env.control_plane.upgrade_strategy == "blue_green" else -4
    standardization = _clamp(standardization)

    return AssessmentScores(
        reliability_risk=round(reliability_risk, 1),
        operational_maturity=round(operational_maturity, 1),
        automation_maturity=round(automation_maturity, 1),
        standardization=round(standardization, 1),
    )
