from .base import *


class LeagueResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(LeagueResourceTest, self).setUp()

        team = Team.objects.create(
            id=0,
            name="Real Madrid",
            city="Madrid",
            coach="Zidane",
            championships_won=35,
            number_of_players=32,
        )

        league = League.objects.create(
            id=0,
            name="La Liga",
            country="Spain",
            current_champion=team,
        )

        league2 = League.objects.create(
            id=2,
            name="Bundesliga",
            country="Germany",
        )

        team.league = league
        team.save()

        Team.objects.create(
            id=1,
            name="FC Barcelona",
            city="Barcelona",
            coach="Ronald Koeman",
            championships_won=35,
            league=league,
        )

        Team.objects.create(
            id=2,
            name="FC Bayern",
            city="Munich",
            coach="Coach",
            championships_won=45,
            is_deleted=True,
        )

        Team.objects.create(
            id=3,
            name="Atletico Madrid",
            city="Madrid",
            coach="Simeone",
            championships_won=25,
            league=league,
            is_deleted=True,
        )

        Team.objects.create(
            id=4,
            name="Borussia Dortmund",
            city="Dortmund",
            coach="Coach 2",
            championships_won=15,
            league=league2,
        )

    def test_get_leagues(self):
        """
        Test GET Leagues
        """

        resp = self.api_client.get(LEAGUE_API_URL, format="json")
        self.assertHttpOK(resp)
        league = resp.data["leagues"][0]
        self.assertEqual(league["name"], "La Liga", "Name should be equal")
        self.assertEqual(league["country"], "Spain", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"],
            "Real Madrid",
            "Current champion should be equal",
        )

    def test_create_league(self):
        """
        Test POST Create League
        """
        resp = self.api_client.post(
            LEAGUE_API_URL,
            format="json",
            data={
                "name": "Ligue 1",
                "country": "France",
            },
        )

        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Ligue 1", "Name should be equal")
        self.assertEqual(league["country"], "France", "City should be equal")
        self.assertEqual(
            league["number_of_teams"], 0, "Number of teams should be equal"
        )

    def test_fail_create_league(self):
        """
        Test POST fail create League
        """

        # Missing data parameter, serializer error
        resp = self.api_client.post(
            LEAGUE_API_URL,
            format="json",
            data={"name": "Bundesliga", "current_champion": 0},
        )

        self.assertHttpBadRequest(resp)

    def test_fail_create_league_with_deleted_champion(self):
        """
        Test POST fail create Team
        """

        # Missing data parameter, serializer error
        resp = self.api_client.post(
            LEAGUE_API_URL,
            format="json",
            data={"name": "Bundesliga2", "country": "Germany", "current_champion": 2},
        )

        self.assertHttpNotFound(resp)

    def test_get_league_by_id(self):
        """
        Test GET League by id
        """

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "La Liga", "Name should be equal")
        self.assertEqual(league["country"], "Spain", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"],
            "Real Madrid",
            "Current champion should be equal",
        )

        resp = self.api_client.put(
            TEAM_ID_API_URL + str(0),
            format="json",
            data={"league": 2},
        )
        self.assertHttpOK(resp)

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "La Liga", "Name should be equal")
        self.assertEqual(league["country"], "Spain", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 1, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"],
            "Real Madrid",
            "Current champion should be equal",
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(2), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Bundesliga", "Name should be equal")
        self.assertEqual(league["country"], "Germany", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )

    def test_fail_get_league_by_non_existent_id(self):
        """
        Test GET fail get league by id
        """

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(10), format="json")
        self.assertHttpBadRequest(resp)
        message = resp.data["message"]
        self.assertEqual("League ID is not valid", message, "Message should be equal")

    def test_put_league_by_id(self):
        """
        Test PUT League by id
        """

        resp = self.api_client.put(
            LEAGUE_ID_API_URL + str(0),
            format="json",
            data={"name": "Liga Espanhola", "current_champion": 1},
        )
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "Liga Espanhola", "Name should be equal")
        self.assertEqual(league["country"], "Spain", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 2, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"], 1, "Current champion id should be equal"
        )

    def test_fail_put_team_by_id(self):
        """
        Test PUT League by id without data
        """

        resp = self.api_client.put(LEAGUE_ID_API_URL + str(0), format="json", data={})
        self.assertHttpNotFound(resp)

    def test_fail_put_league_with_bad_data(self):
        """
        Test PUT League by id bad data
        """

        resp = self.api_client.put(
            LEAGUE_ID_API_URL + str(0),
            format="json",
            data={"number_of_teams": "Ten"},
        )
        self.assertHttpBadRequest(resp)

    def test_fail_put_league_with_deleted_data(self):
        """
        Test PUT League by id deleted data
        """

        resp = self.api_client.put(
            LEAGUE_ID_API_URL + str(0),
            format="json",
            data={"current_champion": 3},
        )
        self.assertHttpBadRequest(resp)

    def test_fail_put_league_with_invalid_data(self):
        """
        Test PUT League by id invalid data
        """

        resp = self.api_client.put(
            LEAGUE_ID_API_URL + str(0),
            format="json",
            data={"current_champion": 4},
        )
        self.assertHttpBadRequest(resp)

    def test_delete_team_by_id(self):
        """
        Test DELETE League by id
        """

        resp = self.api_client.delete(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        message = resp.data["message"]
        self.assertEqual(
            "League deleted with success", message, "Message should be equal"
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpNotFound(resp)
        message = resp.data["message"]
        self.assertEqual("League doesn't exist", message, "Message should be equal")
