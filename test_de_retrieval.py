"""
Unit tests for Data Engineering retrieval services.
"""

from unittest.mock import MagicMock, patch
import pytest

from disclosure_check import check_disclosure
from shared_model import get_shared_model


def test_shared_model_singleton():
    model1 = get_shared_model()
    model2 = get_shared_model()
    assert model1 is model2
    emb = model1.encode("Test sentence")
    assert len(emb) == 384


def test_disclosure_check_present():
    document_chunks = [
        "We offer high growth potential.",
        "Past performance does not guarantee future results. Investments are subject to risk.",
    ]
    required_disclosure = "Past performance does not guarantee future results."

    res = check_disclosure(document_chunks, "DISC-001", required_disclosure, threshold=0.5)
    assert res["disclosure_id"] == "DISC-001"
    assert res["present"] is True
    assert res["similarity_score"] >= 0.5
    assert res["matched_chunk_id"] == "CHUNK-1"


def test_disclosure_check_missing():
    document_chunks = [
        "We offer high growth potential.",
        "Fees are 2% annually.",
    ]
    required_disclosure = "Past performance does not guarantee future results."

    res = check_disclosure(document_chunks, "DISC-001", required_disclosure, threshold=0.7)
    assert res["disclosure_id"] == "DISC-001"
    assert res["present"] is False
    assert res["matched_chunk_id"] is None


def test_rule_lookup_with_mock_db():
    from rule_lookup import find_matching_rules

    mock_db_results = [
        ("RULE-001", "Prohibition of Guaranteed Returns", 0.12),
        ("RULE-002", "Misleading Claims", 0.25),
    ]

    with patch("db.get_connection") as mock_conn_func:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_db_results
        mock_conn.cursor.return_value = mock_cursor
        mock_conn_func.return_value = mock_conn

        matches = find_matching_rules("Guaranteed 20% profit every year", top_n=2)
        assert len(matches) == 2
        assert matches[0]["rule_id"] == "RULE-001"
        assert matches[0]["rule_text"] == "Prohibition of Guaranteed Returns"
        assert matches[0]["similarity_score"] > 0


def test_precedent_search_with_mock_db():
    from precedent_search import find_precedents

    mock_db_results = [
        (101, "Guaranteed 15% return document excerpt", 0.15),
        (102, "Another reviewed marketing piece", 0.30),
        (103, "Third precedent excerpt", 0.45),
    ]

    with patch("db.get_connection") as mock_conn_func:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_db_results
        mock_conn.cursor.return_value = mock_cursor
        mock_conn_func.return_value = mock_conn

        precedents = find_precedents("Investment strategy review", top_n=3)
        assert len(precedents) == 3
        assert precedents[0]["chunk_id"] == "CHUNK-101"
        assert precedents[0]["document_id"] == "DOC-EXISTING"
        assert precedents[0]["similarity_score"] > 0
