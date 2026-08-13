from src.knowledge import search_documents


def _sources(query: str) -> list[str]:
    return [result.source for result in search_documents(query, top_k=3)]


def test_retrieves_emergency_access_policy():
    assert "production-access-policy.md" in _sources(
        "¿Cuánto dura el acceso privilegiado de emergencia?"
    )


def test_retrieves_sev2_policy():
    assert "incident-management.md" in _sources(
        "¿Cada cuánto se actualiza un incidente SEV-2?"
    )


def test_retrieves_escalation_policy():
    assert "service-escalation.md" in _sources(
        "¿Cuándo se escala al Incident Commander?"
    )
