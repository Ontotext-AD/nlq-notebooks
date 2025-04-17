import json

import pytest
from ttyg.graphdb import GraphDB
from ttyg.tools import AutocompleteSearchTool

GRAPHDB_BASE_URL = "http://localhost:7200/"
GRAPHDB_REPOSITORY_ID = "starwars"


@pytest.fixture
def graphdb():
    yield GraphDB(
        base_url=GRAPHDB_BASE_URL,
        repository_id=GRAPHDB_REPOSITORY_ID,
    )


def test_run(graphdb: GraphDB) -> None:
    autocomplete_search_tool = AutocompleteSearchTool(
        graph=graphdb,
        limit=5,
    )
    results = autocomplete_search_tool._run(
        query="Skywalker", predicate="http://www.w3.org/2000/01/rdf-schema#label"
    )
    assert 5 == len(json.loads(results)["results"]["bindings"])

    results = autocomplete_search_tool._run(
        query="Skywalker",
        predicate="http://www.w3.org/2000/01/rdf-schema#label",
        result_class="https://swapi.co/vocabulary/Aleena"
    )
    assert 0 == len(json.loads(results)["results"]["bindings"])

    results = autocomplete_search_tool._run(
        query="Skywalker",
        predicate="http://www.w3.org/2000/01/rdf-schema#label",
        result_class="https://swapi.co/vocabulary/Human"
    )
    assert 5 == len(json.loads(results)["results"]["bindings"])

    with pytest.raises(ValueError) as exc:
        autocomplete_search_tool._run(
            query="Skywalker",
            predicate="http://www.w3.org/2000/01/rdf-schema#label",
            result_class="https://swapi.co/voc/Human"
        )
    assert "The following IRIs are not used in the data stored in GraphDB: <https://swapi.co/voc/Human>" == str(exc.value)

    with pytest.raises(ValueError) as exc:
        autocomplete_search_tool._run(
            query="Skywalker",
            predicate="http://www.w3.org/2000/01/rdf-schema#label",
            result_class="unknown:Human"
        )
    assert "The following IRIs are not used in the data stored in GraphDB: <unknown:Human>" == str(exc.value)

    with pytest.raises(ValueError) as exc:
        autocomplete_search_tool._run(
            query="Skywalker",
            predicate="unknown:label",
        )
    assert "The following IRIs are not used in the data stored in GraphDB: <unknown:label>" == str(exc.value)
