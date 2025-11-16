import pytest
from app.core.cleaning import DataCleaning


class TestDataCleaning:
    def test_clean_rating_valid(self):
        assert DataCleaning.clean_rating("4.5") == 4.5
        assert DataCleaning.clean_rating("3") == 3.0
        assert DataCleaning.clean_rating(None) == 0

    def test_clean_review_with_commas(self):
        assert DataCleaning.clean_review("1,234 reviews") == 1234

    def test_clean_review_with_extra_text(self):
        assert DataCleaning.clean_review("Rated by 456 people") == 456

    def test_clean_review_only_digits(self):
        assert DataCleaning.clean_review("789") == 789

    # def test_clean_review_empty_string(self):
    #     with pytest.raises(ValueError):
    #         DataCleaning.clean_review("")
