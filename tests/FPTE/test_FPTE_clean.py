import pytest
from FPTE.FPTE_clean import fpte_clean
from unittest import MagikMock

from hamcrest import assert_that, equal_to

mock.patch("FPTE_clean.fpte_clean", return_value=False)


class TESTFPTEClean():
    def test_if_cleans(self):
        assert_that(fpte_clean())


class Test(TestCase):
    def test_fpte_clean(self):
        self.fail()
