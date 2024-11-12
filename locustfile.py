import time
import random
from locust import HttpUser, task, between
from datetime import datetime

class User(HttpUser):
    wait_time = between(1, 3)

    payloads = [
        {
            "first_name": "Tameka",
            "last_name": "Combs",
            "email": "tamekacombs@cablam.com"
        },
        {
            "first_name": "Cain",
            "last_name": "Glenn",
            "email": "cainglenn@cablam.com"
        },
        {
            "first_name": "Robert",
            "last_name": "Raymond",
            "email": "robertraymond@cablam.com"
        },
        {
            "first_name": "Kelly",
            "last_name": "Ramirez",
            "email": "kellyramirez@cablam.com"
        },
        {
            "first_name": "Benson",
            "last_name": "Ellis",
            "email": "bensonellis@cablam.com"
        },
        {
            "first_name": "Newman",
            "last_name": "Frank",
            "email": "newmanfrank@cablam.com"
        },
        {
            "first_name": "Katheryn",
            "last_name": "Gamble",
            "email": "katheryngamble@cablam.com"
        },
        {
            "first_name": "Vega",
            "last_name": "Green",
            "email": "vegagreen@cablam.com"
        },
        {
            "first_name": "Glenda",
            "last_name": "Waller",
            "email": "glendawaller@cablam.com"
        },
        {
            "first_name": "Riddle",
            "last_name": "Rios",
            "email": "riddlerios@cablam.com"
        },
        {
            "first_name": "Trisha",
            "last_name": "Owen",
            "email": "trishaowen@cablam.com"
        },
        {
            "first_name": "Wall",
            "last_name": "Franco",
            "email": "wallfranco@cablam.com"
        },
        {
            "first_name": "Merrill",
            "last_name": "Clark",
            "email": "merrillclark@cablam.com"
        },
        {
            "first_name": "Adkins",
            "last_name": "Ratliff",
            "email": "adkinsratliff@cablam.com"
        },
        {
            "first_name": "Enid",
            "last_name": "Hobbs",
            "email": "enidhobbs@cablam.com"
        },
        {
            "first_name": "Leta",
            "last_name": "Head",
            "email": "letahead@cablam.com"
        },
        {
            "first_name": "Lucia",
            "last_name": "Chapman",
            "email": "luciachapman@cablam.com"
        },
        {
            "first_name": "Kim",
            "last_name": "Rosa",
            "email": "kimrosa@cablam.com"
        },
        {
            "first_name": "Camacho",
            "last_name": "Winters",
            "email": "camachowinters@cablam.com"
        },
        {
            "first_name": "Antonia",
            "last_name": "Perry",
            "email": "antoniaperry@cablam.com"
        },
        {
            "first_name": "Etta",
            "last_name": "Dickson",
            "email": "ettadickson@cablam.com"
        },
        {
            "first_name": "Pennington",
            "last_name": "Beasley",
            "email": "penningtonbeasley@cablam.com"
        },
        {
            "first_name": "Lorie",
            "last_name": "Bradshaw",
            "email": "loriebradshaw@cablam.com"
        },
        {
            "first_name": "Allison",
            "last_name": "Cummings",
            "email": "allisoncummings@cablam.com"
        },
        {
            "first_name": "Reba",
            "last_name": "Haley",
            "email": "rebahaley@cablam.com"
        },
        {
            "first_name": "Gabrielle",
            "last_name": "Norman",
            "email": "gabriellenorman@cablam.com"
        },
        {
            "first_name": "Kirby",
            "last_name": "Nielsen",
            "email": "kirbynielsen@cablam.com"
        },
        {
            "first_name": "Harrell",
            "last_name": "Houston",
            "email": "harrellhouston@cablam.com"
        },
        {
            "first_name": "Castillo",
            "last_name": "Carlson",
            "email": "castillocarlson@cablam.com"
        },
        {
            "first_name": "Allison",
            "last_name": "Brennan",
            "email": "allisonbrennan@cablam.com"
        },
        {
            "first_name": "Addie",
            "last_name": "Lynn",
            "email": "addielynn@cablam.com"
        },
        {
            "first_name": "Ava",
            "last_name": "Briggs",
            "email": "avabriggs@cablam.com"
        },
        {
            "first_name": "Sadie",
            "last_name": "Cain",
            "email": "sadiecain@cablam.com"
        },
        {
            "first_name": "Latasha",
            "last_name": "Monroe",
            "email": "latashamonroe@cablam.com"
        },
        {
            "first_name": "Dee",
            "last_name": "Everett",
            "email": "deeeverett@cablam.com"
        },
        {
            "first_name": "Bond",
            "last_name": "Lucas",
            "email": "bondlucas@cablam.com"
        },
        {
            "first_name": "Ingrid",
            "last_name": "Blake",
            "email": "ingridblake@cablam.com"
        },
        {
            "first_name": "Lucy",
            "last_name": "Griffith",
            "email": "lucygriffith@cablam.com"
        },
        {
            "first_name": "Vicky",
            "last_name": "Schwartz",
            "email": "vickyschwartz@cablam.com"
        },
        {
            "first_name": "Arnold",
            "last_name": "Vazquez",
            "email": "arnoldvazquez@cablam.com"
        },
        {
            "first_name": "Mable",
            "last_name": "Garrett",
            "email": "mablegarrett@cablam.com"
        },
        {
            "first_name": "Hines",
            "last_name": "Guy",
            "email": "hinesguy@cablam.com"
        },
        {
            "first_name": "Morin",
            "last_name": "Kaufman",
            "email": "morinkaufman@cablam.com"
        },
        {
            "first_name": "Hubbard",
            "last_name": "Alford",
            "email": "hubbardalford@cablam.com"
        },
        {
            "first_name": "Chapman",
            "last_name": "Peck",
            "email": "chapmanpeck@cablam.com"
        },
        {
            "first_name": "Castaneda",
            "last_name": "Vasquez",
            "email": "castanedavasquez@cablam.com"
        },
        {
            "first_name": "Wendy",
            "last_name": "Leon",
            "email": "wendyleon@cablam.com"
        },
        {
            "first_name": "Roach",
            "last_name": "Sharp",
            "email": "roachsharp@cablam.com"
        },
        {
            "first_name": "Weiss",
            "last_name": "Foster",
            "email": "weissfoster@cablam.com"
        },
        {
            "first_name": "Parker",
            "last_name": "Spears",
            "email": "parkerspears@cablam.com"
        },
        {
            "first_name": "Keith",
            "last_name": "Walls",
            "email": "keithwalls@cablam.com"
        },
        {
            "first_name": "Moody",
            "last_name": "Gregory",
            "email": "moodygregory@cablam.com"
        },
        {
            "first_name": "Leslie",
            "last_name": "Schroeder",
            "email": "leslieschroeder@cablam.com"
        },
        {
            "first_name": "Warner",
            "last_name": "Conley",
            "email": "warnerconley@cablam.com"
        },
        {
            "first_name": "Stewart",
            "last_name": "Greene",
            "email": "stewartgreene@cablam.com"
        },
        {
            "first_name": "Nina",
            "last_name": "Tate",
            "email": "ninatate@cablam.com"
        },
        {
            "first_name": "Underwood",
            "last_name": "Bryant",
            "email": "underwoodbryant@cablam.com"
        },
        {
            "first_name": "Garcia",
            "last_name": "Gill",
            "email": "garciagill@cablam.com"
        },
        {
            "first_name": "Sallie",
            "last_name": "Salinas",
            "email": "salliesalinas@cablam.com"
        },
        {
            "first_name": "Stone",
            "last_name": "Blankenship",
            "email": "stoneblankenship@cablam.com"
        },
        {
            "first_name": "Sophie",
            "last_name": "Mckenzie",
            "email": "sophiemckenzie@cablam.com"
        },
        {
            "first_name": "Earnestine",
            "last_name": "Roberson",
            "email": "earnestineroberson@cablam.com"
        },
        {
            "first_name": "Conway",
            "last_name": "Harrington",
            "email": "conwayharrington@cablam.com"
        },
        {
            "first_name": "Neva",
            "last_name": "Reyes",
            "email": "nevareyes@cablam.com"
        },
        {
            "first_name": "Julie",
            "last_name": "Morton",
            "email": "juliemorton@cablam.com"
        },
        {
            "first_name": "Jenkins",
            "last_name": "Harrison",
            "email": "jenkinsharrison@cablam.com"
        },
        {
            "first_name": "Estes",
            "last_name": "Short",
            "email": "estesshort@cablam.com"
        },
        {
            "first_name": "Tasha",
            "last_name": "Perkins",
            "email": "tashaperkins@cablam.com"
        },
        {
            "first_name": "Holman",
            "last_name": "Bass",
            "email": "holmanbass@cablam.com"
        },
        {
            "first_name": "Cindy",
            "last_name": "Pace",
            "email": "cindypace@cablam.com"
        },
        {
            "first_name": "Middleton",
            "last_name": "Barnett",
            "email": "middletonbarnett@cablam.com"
        },
        {
            "first_name": "Gracie",
            "last_name": "Flores",
            "email": "gracieflores@cablam.com"
        },
        {
            "first_name": "Solomon",
            "last_name": "Horne",
            "email": "solomonhorne@cablam.com"
        },
        {
            "first_name": "England",
            "last_name": "Stanton",
            "email": "englandstanton@cablam.com"
        },
        {
            "first_name": "Catalina",
            "last_name": "Boyle",
            "email": "catalinaboyle@cablam.com"
        },
        {
            "first_name": "Terry",
            "last_name": "Morgan",
            "email": "terrymorgan@cablam.com"
        },
        {
            "first_name": "Sherrie",
            "last_name": "House",
            "email": "sherriehouse@cablam.com"
        },
        {
            "first_name": "Pugh",
            "last_name": "Craig",
            "email": "pughcraig@cablam.com"
        },
        {
            "first_name": "Sharpe",
            "last_name": "Nicholson",
            "email": "sharpenicholson@cablam.com"
        },
        {
            "first_name": "Hahn",
            "last_name": "Fitzpatrick",
            "email": "hahnfitzpatrick@cablam.com"
        },
        {
            "first_name": "Rochelle",
            "last_name": "Stein",
            "email": "rochellestein@cablam.com"
        },
        {
            "first_name": "Delores",
            "last_name": "Chang",
            "email": "deloreschang@cablam.com"
        },
        {
            "first_name": "Marcy",
            "last_name": "Parsons",
            "email": "marcyparsons@cablam.com"
        },
        {
            "first_name": "Yang",
            "last_name": "Chan",
            "email": "yangchan@cablam.com"
        },
        {
            "first_name": "White",
            "last_name": "Newton",
            "email": "whitenewton@cablam.com"
        },
        {
            "first_name": "Carson",
            "last_name": "Gibbs",
            "email": "carsongibbs@cablam.com"
        },
        {
            "first_name": "Rhodes",
            "last_name": "Anderson",
            "email": "rhodesanderson@cablam.com"
        },
        {
            "first_name": "Allie",
            "last_name": "Edwards",
            "email": "allieedwards@cablam.com"
        },
        {
            "first_name": "Douglas",
            "last_name": "Dale",
            "email": "douglasdale@cablam.com"
        },
        {
            "first_name": "Lorraine",
            "last_name": "Woods",
            "email": "lorrainewoods@cablam.com"
        },
        {
            "first_name": "Teri",
            "last_name": "Daugherty",
            "email": "teridaugherty@cablam.com"
        },
        {
            "first_name": "Workman",
            "last_name": "Ashley",
            "email": "workmanashley@cablam.com"
        },
        {
            "first_name": "Rosie",
            "last_name": "Howe",
            "email": "rosiehowe@cablam.com"
        },
        {
            "first_name": "Kathryn",
            "last_name": "Olson",
            "email": "kathrynolson@cablam.com"
        },
        {
            "first_name": "Nannie",
            "last_name": "Mccray",
            "email": "nanniemccray@cablam.com"
        },
        {
            "first_name": "Mckay",
            "last_name": "Avery",
            "email": "mckayavery@cablam.com"
        },
        {
            "first_name": "Sara",
            "last_name": "Franks",
            "email": "sarafranks@cablam.com"
        },
        {
            "first_name": "Viola",
            "last_name": "Gardner",
            "email": "violagardner@cablam.com"
        },
        {
            "first_name": "Kendra",
            "last_name": "Hendricks",
            "email": "kendrahendricks@cablam.com"
        },
        {
            "first_name": "Warren",
            "last_name": "Love",
            "email": "warrenlove@cablam.com"
        },
        {
            "first_name": "Carolyn",
            "last_name": "Weaver",
            "email": "carolynweaver@cablam.com"
        },
        {
            "first_name": "Bernadette",
            "last_name": "Price",
            "email": "bernadetteprice@cablam.com"
        },
        {
            "first_name": "Claudia",
            "last_name": "Parrish",
            "email": "claudiaparrish@cablam.com"
        },
        {
            "first_name": "Brady",
            "last_name": "Wright",
            "email": "bradywright@cablam.com"
        },
        {
            "first_name": "Ruth",
            "last_name": "Ferguson",
            "email": "ruthferguson@cablam.com"
        }
    ]

    @task
    def create_user(self):
        payload = random.choice(self.payloads)
        with self.client.post("/users", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status code: {response.status_code}")