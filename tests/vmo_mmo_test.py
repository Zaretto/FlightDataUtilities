import unittest

import numpy as np


class TestVMO(unittest.TestCase):
    def test_get_vmo_mmo_array__vmo(self):
        from flightdatautilities.vmo_mmo import VMO

        vmo_mapping = VMO(vmo=234)

        pres_alt = np.ma.arange(10000, 15000, dtype=np.float)
        res = vmo_mapping.get_vmo_mmo_arrays(pres_alt)
        res_vmo = res[0]
        res_mmo = res[1]

        self.assertFalse(np.ma.is_masked(res_vmo))
        self.assertTrue(np.ma.is_masked(res_mmo))

        self.assertTrue(np.ma.all(res_vmo == 234))

    def test_get_vmo_mmo_array__mmo(self):
        from flightdatautilities.vmo_mmo import VMO

        vmo_mapping = VMO(mmo=0.89)

        pres_alt = np.ma.arange(10000, 15000, dtype=np.float)
        res = vmo_mapping.get_vmo_mmo_arrays(pres_alt)
        res_vmo = res[0]
        res_mmo = res[1]

        self.assertFalse(np.ma.is_masked(res_mmo))
        self.assertTrue(np.ma.is_masked(res_vmo))

        self.assertTrue(np.ma.all(res_mmo == 0.89))


class TestVMOL382(unittest.TestCase):
    def test_get_vmo_mmo(self):
        from flightdatautilities.vmo_mmo import VMOL382

        vmo_mapping = VMOL382()

        # First band is below 17500
        res = vmo_mapping.get_vmo_mmo(10000)
        self.assertEqual(res, (250 + (10000 * 4 / 17500), None))

        # Second band is 17500:32500
        res = vmo_mapping.get_vmo_mmo(30000)
        self.assertEqual(res, (254 - ((30000 - 17500) * 52 / 15000), None))

        # Third band is above 32500
        res = vmo_mapping.get_vmo_mmo(33000)
        self.assertEqual(res, (202, None))

    def test_get_vmo_mmo_array(self):
        from flightdatautilities.vmo_mmo import VMOL382

        vmo_mapping = VMOL382()

        pres_alt = np.ma.arange(9000, 35000, dtype=np.float)
        res = vmo_mapping.get_vmo_mmo_arrays(pres_alt)
        res_vmo = res[0]
        res_mmo = res[1]

        self.assertFalse(np.ma.is_masked(res_vmo))
        self.assertTrue(np.ma.is_masked(res_mmo))


class TestVMOGlobalExpress(unittest.TestCase):
    def test_get_vmo_mmo(self):
        from flightdatautilities.vmo_mmo import VMOGlobalExpress

        vmo_mapping = VMOGlobalExpress()

        # First band is below 8000
        res = vmo_mapping.get_vmo_mmo(7000)
        self.assertEqual(res, (300, None))

        # Second band is 8000:30267
        res = vmo_mapping.get_vmo_mmo(30000)
        self.assertEqual(res, (340, None))

        # Third band is 30267:35000
        res = vmo_mapping.get_vmo_mmo(34000)
        self.assertEqual(res, (None, 0.89))

        # Fourth band is 35000:41400
        res = vmo_mapping.get_vmo_mmo(40000)
        self.assertEqual(res, (None, 0.88))

        # Fifth band is 41400:47000
        res = vmo_mapping.get_vmo_mmo(45000)
        self.assertEqual(res, (None, 0.858))

        # Sixth band is above 47000
        res = vmo_mapping.get_vmo_mmo(50000)
        self.assertEqual(res, (None, 0.842))

    def test_get_vmo_mmo_array(self):
        from flightdatautilities.vmo_mmo import VMOGlobalExpress

        vmo_mapping = VMOGlobalExpress()

        pres_alt = np.ma.arange(7000, 50001, dtype=np.float)
        res = vmo_mapping.get_vmo_mmo_arrays(pres_alt)
        expected_vmo = np.ma.array(
            [300] * 1001 +
            [340] * (30267 - 8000)
        )
        expected_mmo = np.ma.array(
            [0.89] * (35000 - 30267) +
            [0.88] * (41400 - 35000) +
            [0.858] * (47000 - 41400) +
            [0.842] * (50000 - 47000)
        )
        res_vmo = res[0]
        res_mmo = res[1]

        self.assertTrue(np.ma.is_masked(res_vmo[pres_alt > 30267]))
        np.testing.assert_array_equal(res_vmo[pres_alt <= 30267], expected_vmo)

        self.assertTrue(np.ma.is_masked(res_mmo[pres_alt <= 30267]))
        np.testing.assert_array_equal(res_mmo[pres_alt > 30267], expected_mmo)


##############################################################################
# vim:et:ft=python:nowrap:sts=4:sw=4:ts=4