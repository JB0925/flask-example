import logging
import sys

from logging import Logger

import pytest

from utils.errors import InvalidRequestBodyError, InvalidTypesError
from utils.helpers import check_for_correct_types, validate_json


logging.basicConfig(
   format='%(levelname)s - %(asctime)s: %(message)s ',
   level=logging.INFO,
   stream=sys.stdout
)

logger: Logger = logging.getLogger(__name__)


def test_check_for_correct_types(types_to_validate) -> None:
    """Test that the check_for_correct_types function works as expected."""
    for animal in types_to_validate[:3]:
        assert check_for_correct_types(**animal)

    for animal in types_to_validate[3:5]:
        assert not check_for_correct_types(**animal)


def test_validate_json(types_to_validate) -> None:
    """Test that the validate_json function works as expected."""
    for animal in types_to_validate[:3]:
        validate_json(animal, logger)

    for animal in types_to_validate[3:5]:
        with pytest.raises(InvalidTypesError) as err:
            validate_json(animal, logger)

        assert "One or more of the following values are of the wrong type: " in str(err.value)

    with pytest.raises(InvalidRequestBodyError) as err:
        validate_json(types_to_validate[5], logger)
    
    assert "One or more of the following values are missing: " in str(err.value)