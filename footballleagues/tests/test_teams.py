from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from ..models import *

TEAM_API_URL = "/api/v1/team"
TEAM_ID_API_URL = "/api/v1/team/"


class TeamResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(TeamResourceTest, self).setUp()

        Team.objects.create(
            id=0,
            name="Real Madrid",
            city="Madrid",
            coach="Zidane",
            championships_won=35,
            number_of_players=32,
        )

    def test_get_teams(self):
        """
        Test GET Teams
        """

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][0]
        self.assertEqual(team["name"], "Real Madrid", "Name should be equal")
        self.assertEqual(team["city"], "Madrid", "City should be equal")
        self.assertEqual(team["coach"], "Zidane", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 35, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 32, "Number of players should be equal"
        )

    def test_create_team(self):
        """
        Test POST Create Team
        """
        resp = self.api_client.post(
            TEAM_API_URL,
            format="json",
            data={
                "name": "FC Barcelona",
                "city": "Barcelona",
                "coach": "Ronald Koeman",
                "championships_won": 34,
                "number_of_players": 33,
            },
        )

        self.assertHttpOK(resp)
        team = resp.data["team"]
        self.assertEqual(team["name"], "FC Barcelona", "Name should be equal")
        self.assertEqual(team["city"], "Barcelona", "City should be equal")
        self.assertEqual(team["coach"], "Ronald Koeman", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 34, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 33, "Number of players should be equal"
        )

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(team["name"], "FC Barcelona", "Name should be equal")
        self.assertEqual(team["city"], "Barcelona", "City should be equal")
        self.assertEqual(team["coach"], "Ronald Koeman", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 34, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 33, "Number of players should be equal"
        )

    def test_fail_create_team(self):
        """
        Test POST fail create Team
        """

        # Missing data parameter, serializer error
        resp = self.api_client.post(
            TEAM_API_URL,
            format="json",
            data={
                "city": "Barcelona",
                "coach": "Ronald Koeman",
                "championships_won": 34,
            },
        )

        self.assertHttpBadRequest(resp)

    def test_get_team_by_id(self):
        """
        Test GET Team by id
        """

        resp = self.api_client.get(TEAM_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        team = resp.data["team"]
        self.assertEqual(team["name"], "Real Madrid", "Name should be equal")
        self.assertEqual(team["city"], "Madrid", "City should be equal")
        self.assertEqual(team["coach"], "Zidane", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 35, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 32, "Number of players should be equal"
        )

    def test_fail_get_team_by_non_existent_id(self):
        """
        Test GET fail get team by id
        """

        resp = self.api_client.get(TEAM_ID_API_URL + str(10), format="json")
        self.assertHttpBadRequest(resp)
        message = resp.data["message"]
        self.assertEqual("Team ID is not valid", message, "Message should be equal")

    def test_put_team_by_id(self):
        """
        Test PUT Team by id
        """

        resp = self.api_client.put(
            TEAM_ID_API_URL + str(0), format="json", data={"championships_won": 36}
        )
        self.assertHttpOK(resp)
        team = resp.data["team"]
        self.assertEqual(team["name"], "Real Madrid", "Name should be equal")
        self.assertEqual(team["city"], "Madrid", "City should be equal")
        self.assertEqual(team["coach"], "Zidane", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 36, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 32, "Number of players should be equal"
        )

    def test_fail_put_team_by_id(self):
        """
        Test PUT Team by id without data
        """

        resp = self.api_client.put(TEAM_ID_API_URL + str(0), format="json", data={})
        self.assertHttpNotFound(resp)

    def test_fail_put_team_with_bad_data(self):
        """
        Test PUT Team by id bad data
        """

        resp = self.api_client.put(
            TEAM_ID_API_URL + str(0),
            format="json",
            data={"championships_won": "FCPorto"},
        )
        self.assertHttpBadRequest(resp)

    def test_delete_team_by_id(self):
        """
        Test DELETE Team by id
        """

        resp = self.api_client.delete(TEAM_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        message = resp.data["message"]
        self.assertEqual(
            "Team deleted with success", message, "Message should be equal"
        )

        resp = self.api_client.get(TEAM_ID_API_URL + str(0), format="json")
        self.assertHttpNotFound(resp)
        message = resp.data["message"]
        self.assertEqual("Team doesn't exist", message, "Message should be equal")