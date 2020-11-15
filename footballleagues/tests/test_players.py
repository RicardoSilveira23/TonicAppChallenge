from .base import *


class PlayerResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(PlayerResourceTest, self).setUp()
        team = Team.objects.create(
            id=0,
            name="Juventus",
            city="Torino",
            coach="Coach",
            championships_won=70,
        )

        league = League.objects.create(
            id=0,
            name="Scudeto",
            country="Italy",
            current_champion=team,
        )

        team.league = league
        team.save()

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
            league=league,
        )

        Player.objects.create(
            id=0,
            name="Cristiano Ronaldo",
            age=38,
            position="Forward",
            appearances=450,
            team=team,
        )

        Player.objects.create(
            id=2, name="Robinho", age=45, position="Forward", appearances=650
        )

        Player.objects.create(
            id=3,
            name="Dibala",
            age=25,
            position="Forward",
            appearances=350,
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

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 2, "Number of players should be equal"
        )

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
        player = resp.data["players"][3]
        self.assertEqual(player["name"], "Deco", "Name should be equal")
        self.assertEqual(player["age"], 52, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 540, "Appearances should be equal")

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 3, "Number of players should be equal"
        )
        self.assertEqual(team["league"], "Scudeto", "League name should be equal")

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"], "Deco", "Most appearances should be equal"
        )

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
        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 2, "Number of players should be equal"
        )

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(0),
            format="json",
            data={"appearances": 300, "team": 2},
        )
        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Cristiano Ronaldo", "Name should be equal")
        self.assertEqual(player["age"], 38, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 300, "Appearances should be equal")
        self.assertEqual(player["team"], 2, "Team id should be equal")

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 30, "Number of players should be equal"
        )
        team = resp.data["teams"][0]
        self.assertEqual(
            team["number_of_players"], 1, "Number of players should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"],
            "Dibala",
            "Most appearances should be equal",
        )

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(0),
            format="json",
            data={"appearances": 540, "team": None},
        )
        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Cristiano Ronaldo", "Name should be equal")
        self.assertEqual(player["age"], 38, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 540, "Appearances should be equal")
        self.assertEqual(player["team"], None, "Team id should be equal")

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 29, "Number of players should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"],
            "Dibala",
            "Most appearances should be equal",
        )

    def test_put_player_by_id_without_team(self):
        """
        Test PUT Player by id from no team to team
        """
        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 2, "Number of players should be equal"
        )

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(2),
            format="json",
            data={"team": 2},
        )
        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Robinho", "Name should be equal")
        self.assertEqual(player["age"], 45, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 650, "Appearances should be equal")
        self.assertEqual(player["team"], 2, "Team id should be equal")

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 30, "Number of players should be equal"
        )
        self.assertEqual(
            team["name"], "Inter Milan", "Number of players should be equal"
        )

    def test_put_player_from_no_team_to_team_with_league(self):

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 2, "Number of players should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"],
            "Cristiano Ronaldo",
            "Most appearances should be equal",
        )

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(2),
            format="json",
            data={"team": 2},
        )
        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Robinho", "Name should be equal")
        self.assertEqual(player["age"], 45, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 650, "Appearances should be equal")
        self.assertEqual(player["team"], 2, "Team id should be equal")

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 30, "Number of players should be equal"
        )
        self.assertEqual(
            team["name"], "Inter Milan", "Number of players should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"], "Robinho", "Most appearances should be equal"
        )

    def test_put_player_from_team_to_no_team_with_league(self):

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 2, "Number of players should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"],
            "Cristiano Ronaldo",
            "Most appearances should be equal",
        )

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(0),
            format="json",
            data={"team": None},
        )
        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Cristiano Ronaldo", "Name should be equal")
        self.assertEqual(player["age"], 38, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 450, "Appearances should be equal")
        self.assertEqual(player["team"], None, "Team name should be equal")

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 1, "Number of players should be equal"
        )
        self.assertEqual(team["name"], "Juventus", "Number of players should be equal")

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"], "Dibala", "Most appearances should be equal"
        )

    def test_put_player_change_team_in_same_league(self):
        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 2, "Number of players should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"],
            "Cristiano Ronaldo",
            "Most appearances should be equal",
        )

        resp = self.api_client.put(
            PLAYER_ID_API_URL + str(0),
            format="json",
            data={"team": 2},
        )
        self.assertHttpOK(resp)
        player = resp.data["player"]
        self.assertEqual(player["name"], "Cristiano Ronaldo", "Name should be equal")
        self.assertEqual(player["age"], 38, "Age should be equal")
        self.assertEqual(player["position"], "Forward", "Position should be equal")
        self.assertEqual(player["appearances"], 450, "Appearances should be equal")
        self.assertEqual(player["team"], 2, "Team name should be equal")

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 30, "Number of players should be equal"
        )
        self.assertEqual(
            team["name"], "Inter Milan", "Number of players should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"],
            "Cristiano Ronaldo",
            "Most appearances should be equal",
        )

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

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 2, "Number of players should be equal"
        )

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

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][1]
        self.assertEqual(
            team["number_of_players"], 1, "Number of players should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Scudeto", "Name should be equal")
        self.assertEqual(league["country"], "Italy", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], "Juventus", "Current champion should be equal"
        )
        self.assertEqual(
            league["most_appearances"], "Dibala", "Most appearances should be equal"
        )
