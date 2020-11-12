# TonicAppChallenge

## Objectives

The goal of the challenge is to build an API that allows managing the football leagues. This API will have to interact with either web or mobile applications, with the following requirements:

* You should use the Django REST framework;
* The data should be saved in a PostgreSQL database;
* The data should have the following structure:
  * **Leagues:** name, country, number of teams, the current champion, most championships and most appearances. Example:
    * **name:** Premier League
    * **country:** England
    * **number of teams:** 20
    * **current champion:** Liverpool Football Club
    * **most championships:** Manchester United
    * **most appearances:** Gareth Bale
  * **Teams:** name, city, championships won, coach name and number of players. Example:
    * **name:** Liverpool Football Club
    * **city:** Liverpool
    * **championships won:** 19
    * **coach:** Jürgen Klopp
    * **number of players:** 30
  * **Players:** name, age, position, appearances. Example:
    * **name:** Virgil van Dijk
    * **age:** 29
    * **position:** Defender
    * **appearances:** 95
* Allow filtering teams by name, city, championships won, coach name and the number of players.
* Allow filtering leagues by the name of a player
* Allow pagination

## Delivery

* The code should be written as production-ready code;
* The code should be easy to grow and easy to add new functionality;
* Tests should be present yet the level or the type of testing is up to you;
* Document your API according to OpenAPI specifications.
