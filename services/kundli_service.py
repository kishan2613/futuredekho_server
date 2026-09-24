from services.groq_service import generate_kundli_report


async def generate_complete_kundli(data):

    chart = {
        "name": data.name,
        "birth": {
            "date": data.date,
            "time": data.time,
            "latitude": data.latitude,
            "longitude": data.longitude,
            "timezone": data.timezone
        },

        "ascendant": "Leo",

        "moon_sign": "Cancer",

        "sun_sign": "Gemini",

        "nakshatra": "Pushya",

        "planets": [
            {
                "planet": "Sun",
                "sign": "Gemini",
                "house": 11
            },
            {
                "planet": "Moon",
                "sign": "Cancer",
                "house": 12
            },
            {
                "planet": "Mars",
                "sign": "Leo",
                "house": 1
            }
        ]
    }

    report = generate_kundli_report(chart)

    return {
        "chart": chart,
        "reading": report
    }