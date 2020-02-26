import unittest
from unittest import mock

from AIDM_module import AIDM_classes
import AlgorithmPlatformPyClient
import unit_testing_with_mock.SessionMockFactory as SessionMockFactory
import unit_testing_with_mock.unit_testing_helpers
from unit_testing_with_mock.unit_testing_helpers import get_url_str


class TestCloneTrain(unittest.TestCase):
    class CloneTrainTestMockSession(unit_testing_with_mock.unit_testing_helpers.SessionMockTestBase):
        # to replace session.post:
        def post(self, request, json):
            self.__last_body = json
            self.__last_request = request
            json_string = ('{  "ID": 11037,  "TrainPathNodes": [\n'
                           '    {\n'
                           '      "ID": 11038,\n'
                           '      "SectionTrackID": null,\n'
                           '      "NodeID": 18,\n'
                           '      "NodeTrackID": null,\n'
                           '      "FormationID": 1187,\n'
                           '      "ArrivalTime": "2003-05-01T00:05:00",\n'
                           '      "DepartureTime": "2003-05-01T00:05:00",\n'
                           '      "MinimumRunTime": null,\n'
                           '      "MinimumStopTime": "P0D",\n'
                           '      "StopStatus": "commercialStop",\n'
                           '      "SequenceNumber": 0\n'
                           '    },\n'
                           '    {\n'
                           '      "ID": 11039,\n'
                           '      "SectionTrackID": 1171,\n'
                           '      "NodeID": 10,\n'
                           '      "NodeTrackID": null,\n'
                           '      "FormationID": null,\n'
                           '      "ArrivalTime": "2003-05-01T00:10:00",\n'
                           '      "DepartureTime": "2003-05-01T00:10:00",\n'
                           '      "MinimumRunTime": "PT5M",\n'
                           '      "MinimumStopTime": "P0D",\n'
                           '      "StopStatus": "commercialStop",\n'
                           '      "SequenceNumber": 1\n'
                           '    }\n'
                           '  ],\n'
                           '  "DebugString": "CloneTrainTestMockSession"\n'
                           '}')
            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmPlatformPyClient.AlgorithmicPlatformInterface

    @mock.patch('requests.Session', side_effect=CloneTrainTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str())

    @mock.patch('requests.Session', side_effect=CloneTrainTestMockSession)
    def test_clone_train_request(self, mocked_get_obj):
        test_dict = dict(TrainID=2060)
        self.interface_to_viriato.clone_train(test_dict['TrainID'])
        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._CloneTrainTestMockSession__last_request, get_url_str() + '/clone-train')
        self.assertEqual(session_obj._CloneTrainTestMockSession__last_body, test_dict)

    @mock.patch('requests.Session', side_effect=CloneTrainTestMockSession)
    def test_clone_train_response(self, mocked_get_obj):
        test_cloned_algorithm_train = self.interface_to_viriato.clone_train(2060)
        self.assertIsInstance(test_cloned_algorithm_train, AIDM_classes.AlgorithmTrain)
        self.assertEqual(11037, test_cloned_algorithm_train.ID)
        self.assertEqual('CloneTrainTestMockSession', test_cloned_algorithm_train.DebugString)
        self.assertIsInstance(test_cloned_algorithm_train.TrainPathNodes[0], AIDM_classes.TrainPathNode)
        self.assertEqual(11038, test_cloned_algorithm_train.TrainPathNodes[0].ID)

    def test_clone_train_string_param(self):
        with self.assertRaises(AssertionError):
            with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.clone_train('str instead of int')

    def test_clone_train_double_param(self):
        with self.assertRaises(AssertionError):
            with AlgorithmPlatformPyClient.AlgorithmicPlatformInterface(get_url_str()) as interface_to_viriato:
                interface_to_viriato.clone_train(1.5)

    @mock.patch('requests.Session', side_effect=CloneTrainTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
