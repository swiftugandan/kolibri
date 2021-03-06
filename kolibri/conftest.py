import os
import shutil

import pytest

# referenced in pytest.ini
TEMP_KOLIBRI_HOME = "./.pytest_kolibri_home"


@pytest.fixture(scope="session", autouse=True)
def global_fixture():
    yield  # wait until the test ended
    if os.path.exists(TEMP_KOLIBRI_HOME):
        shutil.rmtree(TEMP_KOLIBRI_HOME)
