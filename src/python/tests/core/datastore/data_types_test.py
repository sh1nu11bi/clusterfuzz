# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""data_types tests."""
import unittest

from datastore import data_types
from tests.test_libs import test_utils


@test_utils.with_cloud_emulators('datastore')
class TestcaseTest(unittest.TestCase):
  """Test Testcase."""

  def test_put(self):
    """Test put(). It should tokenize certain fields."""
    testcase = data_types.Testcase()
    testcase.crash_state = 'state'
    testcase.crash_type = 'type'
    testcase.fuzzer_name = 'fuzzer'
    testcase.overridden_fuzzer_name = 'Overfuzzer'
    testcase.job_type = 'job'
    testcase.bug_information = '333'
    testcase.group_id = 1234
    testcase.group_bug_information = 999
    testcase.impact_stable_version = 's.1'
    testcase.impact_beta_version = 'b.3'
    testcase.platform_id = 'windows'
    testcase.project_name = 'chromium'
    testcase.one_time_crasher_flag = False
    testcase.is_impact_set_flag = True
    testcase.put()

    testcase = testcase.key.get()

    self.assertSetEqual(
        set(['state', 'type', 'job', 'fuzzer', 'overfuzzer', 'windows']),
        set(testcase.keywords))
    self.assertSetEqual(set(['333', '999']), set(testcase.bug_indices))
    self.assertTrue(testcase.has_bug_flag)
    self.assertSetEqual(
        set(['fuzzer', 'overfuzzer']), set(testcase.fuzzer_name_indices))
    self.assertSetEqual(
        set(['s', 's.1']), set(testcase.impact_stable_version_indices))
    self.assertSetEqual(
        set(['b', 'b.3']), set(testcase.impact_beta_version_indices))
    self.assertSetEqual(
        set(['s', 's.1', 'b', 'b.3', 'stable', 'beta']),
        set(testcase.impact_version_indices))

  def test_put_head(self):
    """Tests put() when the impact is head."""
    testcase = data_types.Testcase()
    testcase.impact_stable_version = ''
    testcase.impact_beta_version = ''
    testcase.project_name = 'chromium'
    testcase.one_time_crasher_flag = False
    testcase.is_impact_set_flag = True
    testcase.put()

    testcase = testcase.key.get()

    self.assertSetEqual(set(['head']), set(testcase.impact_version_indices))

  def test_non_chromium(self):
    """Test put(). It should tokenize certain fields."""
    testcase = data_types.Testcase()
    testcase.impact_version_indices = ['head']
    testcase.impact_stable_version = '4.5.6'
    testcase.impact_beta_version = '1.2.3'
    testcase.impact_stable_version_indices = ['s']
    testcase.impact_beta_version_indices = ['b']
    testcase.impact_stable_version_likely = True
    testcase.impact_beta_version_likely = True
    testcase.is_impact_set_flag = True
    testcase.project_name = 'cobalt'
    testcase.put()

    testcase = testcase.key.get()

    self.assertEqual([], testcase.impact_stable_version_indices)
    self.assertEqual([], testcase.impact_beta_version_indices)
    self.assertEqual([], testcase.impact_version_indices)
    # We only clear the indices. The original data is kept.
    self.assertEqual('1.2.3', testcase.impact_beta_version)
    self.assertEqual('4.5.6', testcase.impact_stable_version)
    self.assertTrue(testcase.is_impact_set_flag)
    self.assertTrue(testcase.impact_stable_version_likely)
    self.assertTrue(testcase.impact_beta_version_likely)