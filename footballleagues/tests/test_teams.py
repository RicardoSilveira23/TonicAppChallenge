from .base import *


class TeamResourceTest(ResourceTestCaseMixin, TestCase):
    def setUp(self):
        super(TeamResourceTest, self).setUp()
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

        team.league = league
        team.save()

        Team.objects.create(
            id=2,
            name="Atletico de Madrid",
            city="Madrid",
            coach="Simeone",
            championships_won=38,
            number_of_players=29,
        )

        Team.objects.create(
            id=3,
            name="Valencia FC",
            city="Valencia",
            coach="Coach",
            championships_won=2,
            number_of_players=29,
            league=league,
        )

        League.objects.create(
            id=1,
            name="La Liga 2",
            country="Spain",
            number_of_teams=20,
            is_deleted=True,
        )

        League.objects.create(
            id=2,
            name="La Liga 3",
            country="Spain",
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
        self.assertEqual(team["league"], "La Liga", "League name should be equal")

    def test_create_team(self):
        """
        Test POST Create Team
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
        self.assertEqual(
            league["most_championships"],
            "Real Madrid",
            "Most champions should be equal",
        )

        resp = self.api_client.post(
            TEAM_API_URL,
            format="json",
            data={
                "name": "FC Barcelona",
                "city": "Barcelona",
                "coach": "Ronald Koeman",
                "championships_won": 36,
                "league": 0,
            },
        )

        self.assertHttpOK(resp)
        team = resp.data["team"]
        self.assertEqual(team["name"], "FC Barcelona", "Name should be equal")
        self.assertEqual(team["city"], "Barcelona", "City should be equal")
        self.assertEqual(team["coach"], "Ronald Koeman", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 36, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 0, "Number of players should be equal"
        )
        self.assertEqual(team["league"], "La Liga", "League name should be equal")

        resp = self.api_client.get(TEAM_API_URL, format="json")
        self.assertHttpOK(resp)
        team = resp.data["teams"][3]
        self.assertEqual(team["name"], "FC Barcelona", "Name should be equal")
        self.assertEqual(team["city"], "Barcelona", "City should be equal")
        self.assertEqual(team["coach"], "Ronald Koeman", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 36, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 0, "Number of players should be equal"
        )
        self.assertEqual(team["league"], "La Liga", "League name should be equal")

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "La Liga", "Name should be equal")
        self.assertEqual(league["country"], "Spain", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 3, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"],
            "Real Madrid",
            "Current champion should be equal",
        )
        self.assertEqual(
            league["most_championships"],
            "FC Barcelona",
            "Most champions should be equal",
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

    def test_fail_create_team_with_deleted_league(self):
        """
        Test POST fail create Team
        """

        # Missing data parameter, serializer error
        resp = self.api_client.post(
            TEAM_API_URL,
            format="json",
            data={
                "name": "FC Barcelona",
                "city": "Barcelona",
                "coach": "Ronald Koeman",
                "championships_won": 34,
                "number_of_players": 33,
                "league": 1,
            },
        )

        self.assertHttpNotFound(resp)

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
        self.assertEqual(team["league"], "La Liga", "League name should be equal")

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
            TEAM_ID_API_URL + str(0),
            format="json",
            data={"championships_won": 36, "league": 2},
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
        self.assertEqual(team["league"], 2, "League name should be equal")

    def test_put_team_from_no_league_to_league(self):
        """
        TEST PUT insert team with no league into league
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
        self.assertEqual(
            league["most_championships"],
            "Real Madrid",
            "Most champions should be equal",
        )

        resp = self.api_client.put(
            TEAM_ID_API_URL + str(2),
            format="json",
            data={"league": 0},
        )
        self.assertHttpOK(resp)
        team = resp.data["team"]
        self.assertEqual(team["name"], "Atletico de Madrid", "Name should be equal")
        self.assertEqual(team["city"], "Madrid", "City should be equal")
        self.assertEqual(team["coach"], "Simeone", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 38, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 29, "Number of players should be equal"
        )
        self.assertEqual(team["league"], 0, "League name should be equal")

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(0), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "La Liga", "Name should be equal")
        self.assertEqual(league["country"], "Spain", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 3, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"],
            "Real Madrid",
            "Current champion should be equal",
        )
        self.assertEqual(
            league["most_championships"],
            "Atletico de Madrid",
            "Most champions should be equal",
        )

    def test_put_team_from_league_to_no_league(self):
        """
        TEST PUT take team off league
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
        self.assertEqual(
            league["most_championships"],
            "Real Madrid",
            "Most champions should be equal",
        )

        resp = self.api_client.put(
            TEAM_ID_API_URL + str(0),
            format="json",
            data={"league": None},
        )
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
        self.assertEqual(team["league"], None, "League name should be equal")

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
        self.assertEqual(
            league["most_championships"],
            "Valencia FC",
            "Most champions should be equal",
        )

    def test_put_team_from_league_to_another_league(self):
        """
        TEST PUT move team from one league to another
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
        self.assertEqual(
            league["most_championships"],
            "Real Madrid",
            "Most champions should be equal",
        )

        resp = self.api_client.put(
            TEAM_ID_API_URL + str(0),
            format="json",
            data={"league": 2},
        )
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
        self.assertEqual(team["league"], 2, "League name should be equal")

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
        self.assertEqual(
            league["most_championships"],
            "Valencia FC",
            "Most champions should be equal",
        )

        resp = self.api_client.get(LEAGUE_ID_API_URL + str(2), format="json")
        self.assertHttpOK(resp)
        league = resp.data["league"]
        self.assertEqual(league["name"], "La Liga 3", "Name should be equal")
        self.assertEqual(league["country"], "Spain", "Country should be equal")
        self.assertEqual(
            league["number_of_teams"], 1, "Number of teams should be equal"
        )
        self.assertEqual(
            league["current_champion"],
            None,
            "Current champion should be equal",
        )
        self.assertEqual(
            league["most_championships"],
            "Real Madrid",
            "Most champions should be equal",
        )

    def test_put_team_change_number_of_championships_but_same_league(self):
        """
        TEST PUT change number of championships of team
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
        self.assertEqual(
            league["most_championships"],
            "Real Madrid",
            "Most champions should be equal",
        )

        resp = self.api_client.put(
            TEAM_ID_API_URL + str(3),
            format="json",
            data={"championships_won": 45},
        )
        self.assertHttpOK(resp)
        team = resp.data["team"]
        self.assertEqual(team["name"], "Valencia FC", "Name should be equal")
        self.assertEqual(team["city"], "Valencia", "City should be equal")
        self.assertEqual(team["coach"], "Coach", "Coach should be equal")
        self.assertEqual(
            team["championships_won"], 45, "Number of championships should be equal"
        )
        self.assertEqual(
            team["number_of_players"], 29, "Number of players should be equal"
        )
        self.assertEqual(team["league"], 0, "League name should be equal")

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
        self.assertEqual(
            league["most_championships"],
            "Valencia FC",
            "Most champions should be equal",
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

    def test_fail_put_team_with_deleted_data(self):
        """
        Test PUT Team by id deleted data
        """

        resp = self.api_client.put(
            TEAM_ID_API_URL + str(0),
            format="json",
            data={"league": 1},
        )
        self.assertHttpBadRequest(resp)

    def test_delete_team_by_id(self):
        """
        Test DELETE Team by id
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
        self.assertEqual(
            league["most_championships"],
            "Real Madrid",
            "Most champions should be equal",
        )

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
        self.assertEqual(
            league["most_championships"],
            "Valencia FC",
            "Most champions should be equal",
        )
