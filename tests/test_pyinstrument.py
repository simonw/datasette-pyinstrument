from datasette.app import Datasette
import pytest


@pytest.mark.asyncio
async def test_plugin_is_installed():
    datasette = Datasette([], memory=True)
    response = await datasette.client.get("/-/plugins.json")
    assert response.status_code == 200
    installed_plugins = {p["name"] for p in response.json()}
    assert "datasette-pyinstrument" in installed_plugins


@pytest.mark.asyncio
@pytest.mark.parametrize("on", (True, False))
async def test_pyinstrument(on):
    datasette = Datasette([], memory=True)
    response = await datasette.client.get(
        "/_memory?sql=select+255" + ("&_pyinstrument=1" if on else "")
    )
    assert response.status_code == 200
    html = response.text
    expected_if_on = 'window.profileSession = {"start_time"'
    expected_if_off = "<title>_memory: select 255</title>"
    if on:
        assert expected_if_on in html
        assert expected_if_off not in html
    else:
        assert expected_if_on not in html
        assert expected_if_off in html
