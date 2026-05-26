import pytest
from unittest.mock import patch, MagicMock
from matcher import get_relevant_resume_chunks, analyze_match

SAMPLE_RESUME = """
Data Analyst with 4 years of experience.
Built Power BI dashboards for financial reporting.
Used SQL to query large datasets.
Analyzed customer behavior using Python and pandas.
Created automated reports reducing manual work by 40%.
Presented findings to executive stakeholders.
"""

SAMPLE_JD = """
We are looking for a Data Analyst with SQL and Python skills.
Experience with dashboards and data visualization required.
Must be able to communicate insights to stakeholders.
"""


def test_get_relevant_chunks_returns_string():
    result = get_relevant_resume_chunks(SAMPLE_RESUME, SAMPLE_JD)
    assert isinstance(result, str)
    assert len(result) > 0


def test_get_relevant_chunks_filters_short_lines():
    resume_with_short_lines = "Hi\nOk\n" + SAMPLE_RESUME
    result = get_relevant_resume_chunks(resume_with_short_lines, SAMPLE_JD)
    assert "Hi" not in result


def test_analyze_match_returns_required_keys():
    mock_result = {
        "match_score": 75,
        "missing_keywords": ["SQL", "Python", "Tableau", "ETL", "reporting"],
        "bullet_rewrites": [
            {"original": "Did analysis", "rewritten": "Performed SQL-based analysis"},
            {"original": "Made dashboards", "rewritten": "Built Tableau dashboards"},
            {"original": "Wrote reports", "rewritten": "Automated reporting pipelines"},
        ],
        "gap_analysis": "Missing SQL and Python experience.",
    }

    with patch("matcher.client.messages.create") as mock_create, \
         patch("matcher.model.encode") as mock_encode:

        import numpy as np
        mock_encode.return_value = np.random.rand(10, 384)

        mock_response = MagicMock()
        mock_response.content[0].text = '{"match_score": 75, "missing_keywords": ["SQL", "Python", "Tableau", "ETL", "reporting"], "bullet_rewrites": [{"original": "Did analysis", "rewritten": "Performed SQL-based analysis"}, {"original": "Made dashboards", "rewritten": "Built Tableau dashboards"}, {"original": "Wrote reports", "rewritten": "Automated reporting pipelines"}], "gap_analysis": "Missing SQL and Python experience."}'
        mock_create.return_value = mock_response

        result = analyze_match(SAMPLE_JD, SAMPLE_RESUME)

        assert "match_score" in result
        assert "missing_keywords" in result
        assert "bullet_rewrites" in result
        assert "gap_analysis" in result
        assert isinstance(result["match_score"], int)
        assert len(result["missing_keywords"]) == 5
        assert len(result["bullet_rewrites"]) == 3