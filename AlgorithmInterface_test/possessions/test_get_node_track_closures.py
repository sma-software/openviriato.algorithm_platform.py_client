import datetime
import unittest
from unittest import mock

import AIDMClasses.AIDM_TimeWindow_classes
import AIDMClasses.AIDM_TrackClosure_classes
import AlgorithmInterface.AlgorithmInterface
import AlgorithmInterface_test.test_helper.SessionMockFactory as SessionMockFactory
from AlgorithmInterface import AlgorithmInterfaceFactory
from AlgorithmInterface_test.test_helper.SessionMockTestBase import \
    get_api_url, \
    SessionMockTestBase


class TestGetNodeTrackClosures(unittest.TestCase):
    class GetNodeTrackClosuresTestMockSession(SessionMockTestBase):
        def get(self, request, params):
            self.__last_body = params
            self.__last_request = request
            json_string = ("[\n"
                           "  {\n"
                           "    \"DebugString\": \"nodetrackclosure:85ZMUS 24\",\n"
                           "    \"node_id\": 621,\n"
                           "    \"node_track_id\": 622,\n"
                           "    \"closure_time_window\": {\n"
                           "      \"from_time\": \"2003-05-01T08:00:00\",\n"
                           "      \"to_time\": \"2003-05-02T10:00:00\"\n"
                           "    }\n"
                           "  },\n"
                           "  {\n"
                           "    \"DebugString\": \"nodetrackclosure:85ZMUS 23\",\n"
                           "    \"node_id\": 621,\n"
                           "    \"node_track_id\": 623,\n"
                           "    \"closure_time_window\": {\n"
                           "      \"from_time\": \"2003-05-01T08:00:00\",\n"
                           "      \"to_time\": \"2003-05-02T10:00:00\"\n"
                           "    }\n"
                           "  }\n"
                           "]")

            return SessionMockFactory.create_response_mock(json_string, 200)

    interface_to_viriato: AlgorithmInterface.AlgorithmInterface.AlgorithmInterface

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def test_get_node_track_closures_request(self, mocked_get_obj):
        requested_time_window = AIDMClasses.AIDM_TimeWindow_classes.TimeWindow(
            from_time=datetime.datetime(2003, 5, 1, 0, 0),
            to_time=datetime.datetime(2003, 5, 12, 0, 0))

        self.interface_to_viriato.get_node_track_closures(time_window=requested_time_window)

        session_obj = self.interface_to_viriato._AlgorithmInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetNodeTrackClosuresTestMockSession__last_request,
                         get_api_url() + "/possessions/node-track-closures")
        self.assertDictEqual(session_obj._GetNodeTrackClosuresTestMockSession__last_body,
                             dict(FromTime='2003-05-01T00:00:00', ToTime='2003-05-12T00:00:00'))

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def test_get_node_track_closures_response(self, mocked_get_obj):
        requested_time_window = AIDMClasses.AIDM_TimeWindow_classes.TimeWindow(
            from_time=datetime.datetime(2003, 5, 1, 0, 0),
            to_time=datetime.datetime(2003, 5, 12, 0, 0))

        list_of_section_track_closure = self.interface_to_viriato.get_node_track_closures(requested_time_window)

        self.assertIsInstance(list_of_section_track_closure, list)
        self.assertIsInstance(list_of_section_track_closure[0],
                              AIDMClasses.AIDM_TrackClosure_classes.AlgorithmNodeTrackClosure)
        self.assertIsInstance(list_of_section_track_closure[0].closure_time_window,
                              AIDMClasses.AIDM_TimeWindow_classes.TimeWindow)
        self.assertEqual(list_of_section_track_closure[0].debug_string, "nodetrackclosure:85ZMUS 24")
        self.assertEqual(list_of_section_track_closure[0].closure_time_window.from_time,
                         datetime.datetime(2003, 5, 1, 8, 0))

    @mock.patch('requests.Session', side_effect=GetNodeTrackClosuresTestMockSession)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)
