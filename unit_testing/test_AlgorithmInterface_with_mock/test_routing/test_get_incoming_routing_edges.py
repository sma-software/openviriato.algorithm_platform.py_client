import unittest
from unittest import mock

import unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.SessionMockFactory as APISessionMock
from AIDMClasses import AIDM_classes
from AlgorithmInterface import AlgorithmInterfaceFactory
from unit_testing.test_AlgorithmInterface_with_mock.unit_testing_requisites.unit_testing_with_mock_helpers import \
    get_api_url, SessionMockTestBase


class TestGetIncomingRoutingEdges(unittest.TestCase):
    class GetIncomingRoutingEdgesTestSessionMock(SessionMockTestBase):
        def get(self, request, params):
            self.__last_request = request
            self.__last_body = params

            if params["EndNodeTrackID"] is None:
                json_string = ("{\n"
                               "\"incomingEdges\": [\n"
                               "    {\n"
                               "        \"nodeID\": \"161\",\n"
                               "        \"endNodeTrack\": \"162\",\n"
                               "        \"startSectionTrack\": \"885\"\n"
                               "    },\n"
                               "    {\n"
                               "        \"nodeID\": \"161\",\n"
                               "        \"endNodeTrack\": \"163\",\n"
                               "        \"startSectionTrack\": \"885\"\n"
                               "    },\n"
                               "    {\n"
                               "        \"nodeID\": \"161\",\n"
                               "        \"endNodeTrack\": \"162\",\n"
                               "        \"startSectionTrack\": \"886\"\n"
                               "    },\n"
                               "    {\n"
                               "        \"nodeID\": \"161\",\n"
                               "        \"endNodeTrack\": \"163\",\n"
                               "        \"startSectionTrack\": \"886\"\n"
                               "    },\n"
                               "    {\n"
                               "        \"nodeID\": \"161\",\n"
                               "        \"endNodeTrack\": \"162\",\n"
                               "        \"startSectionTrack\": \"887\"\n"
                               "    },\n"
                               "    {\n"
                               "        \"nodeID\": \"161\",\n"
                               "        \"endNodeTrack\": \"163\",\n"
                               "        \"startSectionTrack\": \"887\"\n"
                               "    }\n"
                               "]\n"
                               "            }")
            else:
                json_string = (" {\n"
                                 " \"incomingEdges\": [\n"
                                 "                        {\n"
                                 "                            \"nodeID\": \"161\",\n"
                                 "                            \"endNodeTrack\": \"162\",\n"
                                 "                            \"startSectionTrack\": \"885\"\n"
                                 "                        },\n"
                                 "                        {\n"
                                 "                            \"nodeID\": \"161\",\n"
                                 "                            \"endNodeTrack\": \"162\",\n"
                                 "                            \"startSectionTrack\": \"886\"\n"
                                 "                        },\n"
                                 "                        {\n"
                                 "                            \"nodeID\": \"161\",\n"
                                 "                            \"endNodeTrack\": \"162\",\n"
                                 "                            \"startSectionTrack\": \"887\"\n"
                                 "                        }\n"
                                 "                    ]\n"
                                 "                }")

            return APISessionMock.create_response_mock(json_string, 200)

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def setUp(self, mocked_get_obj):
        self.interface_to_viriato = AlgorithmInterfaceFactory.create(get_api_url())

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def test_get_incoming_routing_edges_request(self, mocked_get_obj):
        routing_point = AIDM_classes.RoutingPoint(nodeID=1, nodeTrackID=12)

        self.interface_to_viriato.get_incoming_routing_edges(routing_point=routing_point)

        session_obj = self.interface_to_viriato._AlgorithmicPlatformInterface__communication_layer.currentSession
        self.assertEqual(session_obj._GetIncomingRoutingEdgesTestSessionMock__last_request, get_api_url() +
                         "/vehicles/formations/1828")
        self.assertDictEqual(session_obj._GetIncomingRoutingEdgesTestSessionMock__last_body, {"nodeTrackID": "12"})

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def test_get_incoming_routing_edges_response_only_node_id(self, mocked_get_obj):
        routing_point = AIDM_classes.RoutingPoint(nodeID=1)

        routing_edges = self.interface_to_viriato.get_incoming_routing_edges(routing_point)
        # FIXME Is not implemented due to a bug in the Documentation
        raise NotImplementedError

    def test_get_incoming_routing_edges_response_node_id_and_node_track_id(self, mocked_get_obj):
        routing_point = AIDM_classes.RoutingPoint(nodeID=1, nodeTrackID=21)

        routing_edges = self.interface_to_viriato.get_incoming_routing_edges(routing_point)
        # FIXME Is not implemented due to a bug in the Documentation
        raise NotImplementedError

    @mock.patch('requests.Session', side_effect=GetIncomingRoutingEdgesTestSessionMock)
    def tearDown(self, mocked_get_obj) -> None:
        self.interface_to_viriato.__exit__(None, None, None)


if __name__ == '__main__':
    unittest.main()
