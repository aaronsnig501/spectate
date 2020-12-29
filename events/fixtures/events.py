EVENT_TO_BE_CREATED = {
    "message": "NewEvent",
    "id": 8622032232038284220,
    "name": "Real Madrid vs Barcelona",
    "startTime": "2018-06-20 10:30:00",
    "sport": {"id": 221, "name": "Football"},
    "markets": [
        {
            "id": 385086549360973392,
            "name": "Winner",
            "selections": [
                {"id": 8003902714083343527, "name": "Real Madrid", "odds": 1.01},
                {"id": 5007661888266680774, "name": "Barcelona", "odds": 1.01},
            ],
        },
    ],
}

DUPLICATE_EVENT = {
    "message": "NewEvent",
    "id": 8622032232038284220,
    "name": "Real Madrid vs Barcelona",
    "startTime": "2018-06-20 10:30:00",
    "sport": {"id": 221, "name": "Football"},
    "markets": [
        {
            "id": 385086549360973392,
            "name": "Winner",
            "selections": [
                {"id": 8003902714083343527, "name": "Real Madrid", "odds": 1.01},
                {"id": 5007661888266680774, "name": "Barcelona", "odds": 1.01},
            ],
        },
    ],
}


EVENT_TO_UPDATE = {
    "message": "UpdateOdds",
    "id": 8661032232038284220,
    "name": "Real Madrid vs Barcelona",
    "startTime": "2018-06-20 10:30:00",
    "sport": {"id": 221, "name": "Football"},
    "markets": [
        {
            "id": 385086549360973392,
            "name": "Winner",
            "selections": [
                {"id": 8243901714083343527, "name": "Real Madrid", "odds": 10},
                {"id": 5737666888266680774, "name": "Barcelona", "odds": 5.55},
            ],
        },
    ],
}

EVENT_WITH_NO_MESSAGE = {
    "id": 994839351740,
    "name": "Real Madrid vs Barcelona",
    "startTime": "2018-06-20 10:30:00",
    "sport": {"id": 221, "name": "Football"},
    "markets": [
        {
            "id": 385086549360973392,
            "name": "Winner",
            "selections": [
                {"id": 8003902714083343527, "name": "Real Madrid", "odds": 1.01},
                {"id": 5007661888266680774, "name": "Barcelona", "odds": 1.01},
            ],
        },
    ],
}

EVENT_WITH_UNKNOWN_MESSAGE = {
    "message": "UnknownMessage",
    "id": 994839351740,
    "name": "Real Madrid vs Barcelona",
    "startTime": "2018-06-20 10:30:00",
    "sport": {"id": 221, "name": "Football"},
    "markets": [
        {
            "id": 385086549360973392,
            "name": "Winner",
            "selections": [
                {"id": 8003902714083343527, "name": "Real Madrid", "odds": 1.01},
                {"id": 5007661888266680774, "name": "Barcelona", "odds": 1.01},
            ],
        },
    ],
}