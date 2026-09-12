import httpx
import pytest
import respx

from foresportia import ForesportiaClient, MatchSummary, MatchDetail

BASE = "https://api.foresportia.com"
MATCH_ID = "fsm:v1:" + "a" * 64


@pytest.mark.parametrize("method,path,kwargs,response", [
    ("list_today_matches", "/v1/matches/today", {}, {"matches": []}),
    ("list_today_picks", "/v1/picks/today", {}, {"matches": []}),
    ("list_league_matches", "/v1/leagues/LIGUE_1/matches", {"league_code": "LIGUE_1"}, {"matches": []}),
    ("list_league_history", "/v1/leagues/LIGUE_1/matches", {"league_code": "LIGUE_1"}, {"matches": []}),
    ("get_match", "/v1/matches/" + MATCH_ID, {"match_id": MATCH_ID}, {"reliability": False, "reliability_context": ["elo_unreliable"]}),
    ("get_matches_bulk", "/v1/matches/bulk", {"match_ids": [MATCH_ID]}, {"results": [], "errors": []}),
])
@respx.mock
def test_opt_in_serialized_only_when_explicit(method, path, kwargs, response):
    route = respx.route(method="POST" if method == "get_matches_bulk" else "GET", url=BASE + path).mock(
        return_value=httpx.Response(200, json=response))
    with ForesportiaClient(api_key="test-key") as client:
        getattr(client, method)(**kwargs)
        assert "include_unreliable" not in route.calls[-1].request.url.params
        getattr(client, method)(**kwargs, include_unreliable=True)
        assert route.calls[-1].request.url.params["include_unreliable"] == "true"


def test_typed_reliability_does_not_infer_missing_flags():
    payload = {"id": MATCH_ID, "reliability": False, "reliability_context": ["elo_unreliable"]}
    summary = MatchSummary.from_dict(payload)
    detail = MatchDetail(raw=payload)
    assert summary.reliability is detail.reliability is False
    assert summary.reliability_context == detail.reliability_context == ["elo_unreliable"]
    assert MatchSummary.from_dict({"id": MATCH_ID}).reliability is None
    assert MatchDetail(raw={}).reliability is None
