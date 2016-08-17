# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest


@pytest.fixture(scope='session')
def session_capabilities(session_capabilities):
    session_capabilities.setdefault('tags', []).append('socorro')
    return session_capabilities


@pytest.yield_fixture
def eyes():
    from applitools.eyes import Eyes
    eyes = Eyes()
    eyes.api_key = 'foo'
    yield eyes
    eyes.close()


@pytest.fixture
def selenium(request, eyes, selenium):
    selenium = eyes.open(
        driver=selenium,
        app_name='Socorro',
        test_name=request.node.nodeid,
        viewport_size={'width': 1024, 'height': 768})
    return selenium
