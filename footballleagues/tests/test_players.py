from django.test import TestCase
from tastypie.test import ResourceTestCaseMixin

from ..models import *

PLAYER_API_URL = "/api/v1/player"
PLAYER_ID_API_URL = "/api/v1/player/"


class PlayerResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(PlayerResourceTest, self).setUp()
        team = Team.objects.create(
            id=0,
            name="Juventus",
            city="Torino",
            coach="Coach",
            championships_won=70,
            number_of_players=27,
        )
        Team.objects.create(
            id=1,
            name="AC Milan",
            city="Milan",
            coach="Coach 2",
            championships_won=45,
            number_of_players=29,
            is_deleted=True,
        )

        Team.objects.create(
            id=2,
            name="Inter Milan",
            city="Milan",
            coach="Coach 3",
            championships_won=40,
            number_of_players=29,
        )

        Player.objects.create(
            id=0,
            name="Cristiano Ronaldo",
            age=38,
            position="Forward",
            appearances=450,
            team=team,
        )

    def test_get_players(self):
        """
        Test GET Players
        """

        resp = self.api_client.get(PLAYER_API_URL, format="json")
        self.assertHttpOK(resp)
        player = resp.data["players"][0]
        self.assertEqual(player["name"], "Cristiano Ronaldo", "Name should be equal")
        self.assertEqual(player["age"], 38, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 450, "Appearances should be equal")
        self.assertEqual(player["team"], "Juventus", "Team name should be equal")

    def test_create_player(self):
        """
        Test POST Create Player
        """
        resp = self.api_client.post(
            PLAYER_API_URL,
            format="json",
            data={
                "name": "Deco",
                "age": 52,
                "position": "Forward",
                "appearances": 540,
                "team": 0,
            },
        )

        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Deco", "Name should be equal")
        self.assertEqual(player["age"], 52, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 540, "Appearances should be equal")

        resp = self.api_client.get(PLAYER_API_URL, format="json")
        self.assertHttpOK(resp)
        player = resp.data["players"][1]
        self.assertEqual(player["name"], "Deco", "Name should be equal")
        self.assertEqual(player["age"], 52, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 540, "Appearances should be equal")

    def test_fail_create_player(self):
        """
        Test POST fail create Player
        """

        # Missing data parameter, serializer error
        resp = self.api_client.post(
            PLAYER_API_URL,
            format="json",
            data={"name": "Deco", "age": 52, "position": "Forward"},
        )

        self.assertHttpBadRequest(resp)

    def test_fail_create_player_with_deleted_team(self):
        """
        Test POST fail create Player
        """

        # Missing data parameter, serializer error
        resp = self.api_client.post(
            PLAYER_API_URL,
            format="json",
            data={
                "name": "Deco",
                "age": 52,
                "position": "Forward",
                "appearances": 540,
                "team": 1,
            },
        )

        self.assertHttpNotFound(resp)

    def test_get_player_by_id(self):
        """
        Test GET Player by id
        """

        resp = self.api_client.get(PLAYER_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Cristiano Ronaldo", "Name should be equal")
        self.assertEqual(player["age"], 38, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 450, "Appearances should be equal")

    def test_fail_get_player_by_non_existent_id(self):
        """
        Test GET fail get player by id
        """

        resp = self.api_client.get(PLAYER_ID_API_URL + str(10), format="json")
        self.assertHttpBadRequest(resp)
        message = resp.data["message"]
        self.assertEqual("Player ID is not valid", message, "Message should be equal")

    def test_put_player_by_id(self):
        """
        Test PUT Player by id
        """

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(0),
            format="json",
            data={"appearances": 540, "team": 2},
        )
        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Cristiano Ronaldo", "Name should be equal")
        self.assertEqual(player["age"], 38, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 540, "Appearances should be equal")
        self.assertEqual(player["team"], 2, "Team id should be equal")

    def test_fail_put_player_by_id(self):
        """
        Test PUT Player by id without data
        """

        resp = self.api_client.put(PLAYER_ID_API_URL + str(0), format="json", data={})
        self.assertHttpNotFound(resp)

    def test_fail_put_player_with_bad_data(self):
        """
        Test PUT Player by id bad data
        """

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(0), format="json", data={"team": 3}
        )
        self.assertHttpBadRequest(resp)

    def test_fail_put_player_with_deleted_data(self):
        """
        Test PUT Player by id deleted data
        """

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(0), format="json", data={"team": 1}
        )
        self.assertHttpBadRequest(resp)

    def test_delete_player_by_id(self):
        """
        Test DELETE Player by id
        """

        resp = self.api_client.delete(PLAYER_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        message = resp.data["message"]
        self.assertEqual(
            "Player deleted with success", message, "Message should be equal"
        )

        resp = self.api_client.get(PLAYER_ID_API_URL + str(0), format="json")
        self.assertHttpNotFound(resp)
        message = resp.data["message"]
        self.assertEqual("Player doesn't exist", message, "Message should be equal")
