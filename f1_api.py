import requests
from typing import Dict, Optional, List

# Base URL for the Ergast API, without trailing slash
base_url = "https://api.jolpi.ca/ergast/f1"

# ordinal number converter
ordinal = lambda n: "%d%s" % (
    n,
    "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4],
)

# constructor name to constructor ID
constructor_name_to_id = {
    "mercedes": "AMG",
    "red_bull": "RBR",
    "mclaren": "MCL",
    "aston_martin": "AMR",
    "alpine": "ALP",
    "ferrari": "FER",
    "alpha_tauri": "ATR",
    "alfa": "ALF",
    "haas": "HAS",
    "williams": "WIL",
}

# favourites
favourite_drivers = ["hamilton", "max_verstappen"]
favourite_teams = ["mercedes", "red_bull"]


def get_driver_by_id(driver_id: str) -> Dict[str, str]:
    """
    Get a specific driver by their driver ID

    Parameters:
    driver_id (str): The ID of the driver

    Returns:
    Driver (dict): The details of the specified driver
        - driverId (str): A unique identifier for the driver
        - permanentNumber (str): The permanent number of the driver
        - code (str): The three letter code of the driver
        - url (str): The URL of the driver
        - givenName (str): The given name of the driver
        - familyName (str): The family name of the driver
        - dateOfBirth (str): The date of birth of the driver
        - nationality (str): The nationality of the driver
    """
    url = f"{base_url}/drivers/{driver_id}/"
    response = requests.get(url)
    driver: Dict[str, str] = response.json()["MRData"]["DriverTable"]["Drivers"][0]
    return driver


def get_driver_standings(
    season: Optional[str] = "current",
    round: Optional[str] = None,
    position: Optional[str] = None,
) -> List[Dict]:
    """
    Get the driver standings for a given season and round. Optionally filter by position (e.g. get the driver in 3rd place).
    Defaults to the current season and last round. And all positions if not specified.

    If no driver standings are available for the given round (due to data not beimg updated or race not happened yet)
    the function will attempt to get the standings for the previous round.

    Parameters:
    season (str): The year of the season
    round (str): The round number of the season
    position (str): The position of the driver in the standings

    Returns:
    DriverStandings (dict): A table of driver standings for the given season and round
        - position (str): The position of the driver in the standings
        - positionText (str): The position of the driver in the standings (as text)
        - points (str): The number of points the driver has scored
        - wins (str): The number of wins the driver has achieved
        - Driver (object): The driver details
            - driverId (str): A unique identifier for the driver
            - url (str): The URL of the driver
            - givenName (str): The given name of the driver
            - familyName (str): The family name of the driver
            - dateOfBirth (str): The date of birth of the driver
            - nationality (str): The nationality of the driver
        - Constructors (object): The constructor details
            - constructorId (str): A unique identifier for the constructor
            - url (str): The URL of the constructor
            - name (str): The name of the constructor
            - nationality (str): The nationality of the constructor
    """
    url = f"{base_url}/{season}"
    if round:
        url += f"/{round}"

    url += "/driverStandings/"

    if position:
        if not round:
            raise ValueError("Cannot filter by position without specifying a round")
        url += f"{position}/"

    print(url)

    response = requests.get(url)

    if response.status_code == 200:
        # fmt: off
        round = response.json()["MRData"]["StandingsTable"]["round"]
        standings_lists: List[Dict] = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
        # fmt: on

        if not standings_lists:
            # No standings for the given round, try to get the previous round
            return get_driver_standings(season, str(int(round) - 1), position)

        return standings_lists[0]


def prettify_driver_standings(standing_lists: List[Dict]) -> str:
    """
    Prettify the driver standings into a human readable format

    Parameters:
    driver_standings (List[Dict[str, str]]): The driver standings to prettify

    Returns:
    str: The prettified driver standings
    """

    # Form title of the standings
    title = f"Driver Standings for {standing_lists[0]['season']} - Round {standing_lists[0]['round']}"
    if len(standing_lists[0]["DriverStandings"]) == 1:
        position = standing_lists[0]["DriverStandings"][0]["positionText"]
        title += f" - {ordinal(int(position))} place"

    standings = []
    for driver in standing_lists[0]["DriverStandings"]:
        position = driver["positionText"]
        name = f"{driver['Driver']['givenName']} {driver['Driver']['familyName']}"
        if driver["Driver"]["driverId"].lower() in favourite_drivers:
            name = f"★ {name}"
        points = driver["points"]
        wins = driver["wins"]
        team = driver["Constructors"][0]["name"]

        standings.append(f"{position}. {name} ({team}) - {points} points, {wins} wins")

    return title + "\n" + "\n".join(standings)


def get_constructor_standings(
    season: Optional[str] = "current",
    round: Optional[str] = None,
    position: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Get the constructor standings for a given season and round. Optionally filter by position (e.g. get the constructor in 3rd place).
    Defaults to the current season and last round. And all positions if not specified.

    If no constructor standings are available for the given round (due to data not beimg updated
    """

    url = f"{base_url}/{season}"
    if round:
        url += f"/{round}"

    url += "/constructorStandings/"

    if position:
        if not round:
            raise ValueError("Cannot filter by position without specifying a round")
        url += f"{position}/"

    print(url)

    response = requests.get(url)

    if response.status_code == 200:
        # fmt: off
        round = response.json()["MRData"]["StandingsTable"]["round"]
        standings_lists: List[Dict] = response.json()["MRData"]["StandingsTable"]["StandingsLists"]
        # fmt: on

        if not standings_lists:
            # No standings for the given round, try to get the previous round
            return get_constructor_standings(season, str(int(round) - 1), position)

        return standings_lists[0]


def prettify_constructor_standings(constructor_standings: List[Dict[str, str]]) -> str:
    """
    Prettify the constructor standings into a human readable format

    Parameters:
    constructor_standings (List[Dict[str, str]]): The constructor standings to prettify

    Returns:
    str: The prettified constructor standings
    """

    # Form title of the standings
    title = f"Constructor Standings for {constructor_standings[0]['season']} - Round {constructor_standings[0]['round']}"
    if len(constructor_standings[0]["ConstructorStandings"]) == 1:
        position = constructor_standings[0]["ConstructorStandings"][0]["positionText"]
        title += f" - {ordinal(int(position))} place"

    standings = []
    for constructor in constructor_standings[0]["ConstructorStandings"]:
        position = constructor["positionText"]
        name = constructor["Constructor"]["name"]
        if constructor["Constructor"]["constructorId"].lower() in favourite_teams:
            name = f"★ {name}"
        points = constructor["points"]
        wins = constructor["wins"]

        standings.append(f"{position}. {name} - {points} points, {wins} wins")

    return title + "\n" + "\n".join(standings)

import ui_models




if __name__ == "__main__":
    # t = get_driver_standings()
    # print(t)

    # t = get_driver_standings("2021")
    # print(prettify_driver_standings(t))

    # t = get_driver_standings("2021", "1")
    # print(prettify_driver_standings(t))

    # t = get_driver_standings("2021", "1", "1")
    # print(prettify_driver_standings(t))

    # t = get_constructor_standings()
    # print((t))

    # t = get_constructor_standings("2021")
    # print(prettify_constructor_standings(t))

    # t = get_constructor_standings("2021", "1")
    # print(prettify_constructor_standings(t))

    # t = get_constructor_standings("2021", "1", "5")
    
    
    top_3_drivers = get_driver_standings()['DriverStandings'][:3]
    top_3_drivers_codes = list(map(lambda driver: driver['Driver']['code'], get_driver_standings()['DriverStandings'][:3]))

    print(top_3_drivers_codes)

    print(top_3_drivers)


