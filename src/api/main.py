"""FastAPI application for framework services."""

from __future__ import annotations

from fastapi import FastAPI

from src.monitoring.kpi_tracker import KPITracker

app = FastAPI(title="AI-Native Development Framework API", version="1.0.0")

kpi_tracker = KPITracker()
learning_state = {
    "status": "idle",
    "proposals": [],
    "current_iteration": 0,
}


@app.get("/health")
async def health() -> dict:
    """Health check endpoint."""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/dashboard")
async def dashboard() -> dict:
    """Return dashboard summary."""
    return kpi_tracker.dashboard_summary()


@app.post("/kpis/sprint")
async def record_sprint(kpis: dict) -> dict:
    """Record sprint KPIs."""
    from src.monitoring.kpi_tracker import SprintKPIs

    sprint_kpis = SprintKPIs(**kpis)
    kpi_tracker.record_sprint(sprint_kpis)
    return {"status": "recorded", "sprint_id": sprint_kpis.sprint_id}


@app.get("/learning/status")
async def learning_status() -> dict:
    """Return current learning loop status."""
    return learning_state


@app.get("/learning/proposals")
async def learning_proposals() -> dict:
    """Return pending and historical proposals."""
    return {"proposals": learning_state["proposals"]}


@app.post("/learning/proposals/{proposal_id}/approve")
async def approve_proposal(proposal_id: str, approval: dict) -> dict:
    """Approve a learning proposal."""
    for proposal in learning_state["proposals"]:
        if proposal.get("proposal_id") == proposal_id:
            proposal["status"] = "approved"
            proposal["approved_by"] = approval.get("approver", "unknown")
            return {"status": "approved", "proposal_id": proposal_id}
    return {"status": "not_found", "proposal_id": proposal_id}


@app.post("/learning/proposals/{proposal_id}/reject")
async def reject_proposal(proposal_id: str) -> dict:
    """Reject a learning proposal."""
    for proposal in learning_state["proposals"]:
        if proposal.get("proposal_id") == proposal_id:
            proposal["status"] = "rejected"
            return {"status": "rejected", "proposal_id": proposal_id}
    return {"status": "not_found", "proposal_id": proposal_id}


@app.get("/learning/impact")
async def learning_impact() -> dict:
    """Return learning impact summary."""
    return {
        "sprint_count": len(kpi_tracker.sprints),
        "latest_trends": kpi_tracker.get_trends(),
        "proposals": learning_state["proposals"],
    }
