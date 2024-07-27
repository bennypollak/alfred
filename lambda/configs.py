import json

echo_device_map = {
    "amzn1.ask.device.AMA6SNV7ZV7UGFBNWNIETNX7QQGECL34YVRGDCZWMDVJP5OORNHBIGCNLAHEBTRS625BU7J3GFUXWWGNVOT5RM3DEUVRTEWSPJFHIBK6LDBUPNRSOL427OWPOVZVIV2IPE4RZ7KLVBJ3DCDC55E3XRRLKKVQS5ZXCUZH6UTGPVPBGEU7AB2KILZM7BJB54C64BCETAMMIGBRJBSD": "livingroom",
    "amzn1.ask.device.AMAXBAW7JBUZYYPMO6WS4DQCGGCX7PWI63LRD626DQJMJXEDRHPM7FA3DUNXIQUHFSX57ZPXYCI5AFM7RHDHVIATSKHCURO4ETXQXNHTYNV4WSQV4DB2TZWCIPSCF6UF2JGNJRQF2L5W4AYRBJD2MO6P4TH2VLN4SK67D2EFYGO4TX3BKUNXGIHXKTDZIS62ROMBW": "retired",
    "amzn1.ask.device.AMATH75Q4RFEKCXKEU4GLKJEGJ2BEDAVFUWKMIU3LHHVUVGK2NBKJUOO447U55GIUJMLOMJPS7ED6FSQ2GTYQE4LI5CO3PHCYSNTVCGI4ORL5YN2MFY76SSTVL22TYQORFDC2445S3SHZEQAMAO556QQLSCRHZXF3OJJ4DVAQHCXMAQRQSGY2BIIUMVEEVOKLM4CNGV7RD77Z2KP": "bedroom",
    "amzn1.ask.device.AMAXJAPA4OTSER5H6YZ2LVKHQAKL4FTPBEWPSFMKEDCT5Z7UF3EYUREQ7O7F2SHLZJPYFRY3HY4E2DAFNUZYRUD6PUSGNN7ZWAH4MPOJL2UGRFSGEHVTSKVLHFISTGH3UFYSVAIOGHG4ONSE6IIJVYWAUWZRQW2SOWTRHLOTBEVTWSFRRNQA646J7VHEH3D2GDHI22DYP2YX6KI": "kitchen",
    "amzn1.ask.device.AMA5R44WCBSXEWTJ4ILRVBZNPLXHB24I5FTG5E6EQ5P5KB2GDX3IISOHCN6TNXLCSNPNWITESBC4J7DGJDIEN62D2XOVG3U4XRVGP4P6M2YFUEFNDLLGHPMULKO43KM7J5H75ZEB5GPJ77TVQUF7VRGRPRUSBUYXVJ2BP6TY5XTYENYJY733MLJ3NHTDAUD7SKZDWJD6NPJL3CQ": "test",
    "amzn1.ask.device.AMA4UBAJ5A3XUSANPNJWCEHQIYC5FWEARFWN3VKIKUQIV7Q72FXGYLCOXAS56FRTSP2FBYLJKBBYTOLZRX35YKQNJ6QEU7QFWDIXATZTYECP2VYOGV46OHHW35GEOGKOIUS536EVP4NOZ55R5JW7CKKAO4IEZNCXAV3YVT6ARRESWAGAQTRXG65VXYWJGYITC2ABLGONYSMCDLYH": "iphone",
    "amzn1.ask.device.AMAZ5FPGYM43LH3SO7RAQX7UEJFN4Y5IWUVHSMZDNEKHBKUXYG3VOTJAHFHSH3ENLDNHZQINHBCTVYFBLCRWRZKKWASCBORGOILNEMF5WMZ4NTUBF5FW4FK7SFLVJ6G2GQ3TKHXUEPHKI7NYCZXZUY6L3DIZQ6UFJRUSNQVRITLLHSN2YH3QDZ36DM2UJ32NVPPQJH2ANYSFY363": "returned desk",
    "amzn1.ask.device.AMA2NLYQJQFUCVD4HMIEXOBRYCOIHBPLIBH3QJ522I7S347GV5GBHTOEXHPOGIGXPUZDF6ZWBJQVOLZNMCWOISQNZ62ECRXBBQ62JHXBBMAJ7WTDXNFCBYEDWQHOBF6R5FYAXI3T6HCZWNCGCNKMM4SQ6CW7XSXAIYDERZ4ODUQJQUU4GNGM3MZWQ4VJ7LOYFQ3KUBVMF7ARZGL7": "santiago livingroom",
    "amzn1.ask.device.AMA6LNNAK4WOQMHNWVJ5TRDYEJGQBB5YPKJNUUE5FCGC4TIOUZKF5TXXLVVBX5UDAEZERB4UZ5EZYFI6LYWYOLBMXBYTKWENFU5XRDWGZXC3ZU4UOIUTLPYMSQPEBHZZWRL7RIJXPVM5MEUZDAZWQXHZ44LC5QRFVKL322U7EW3HVRZQTQADJQKEVXRIUCEO7QKTEZDI4KWVTKA": "desk"
}
room_map = {'small': 'small', 'bedroom': 'small', 'big': 'big', 'livingroom': 'big', 'testdesk': 'big'}
valid_devices = ['tv', 'tivo']
station_to_channel_map = {
    "cnn": 600, "abc": 507, "nbc": 504, "cbs": 502, "fox": 505, "espn": 570, "hbo": 899, "showtime": 865, "tmc": 230,
    "tiny": 4, "huge": 1000
}
device_names_map = {
    "tv": { "small": "stv", "big": "btv" },
    "tivo": { "small": "st", "big": "bt" }
}
commands_map = {
        "last": { "device": "tivo"  },
        "guide": { "device": "tivo"  },
        "record": { "device": "tivo"  },
        "aspect": { "device": "tivo"  },
        "up": { "device": "tivo", "command": "direction-up" },
        "down": { "device": "tivo", "command": "direction-down" },
        "left": { "device": "tivo", "command": "direction-left" },
        "right": { "device": "tivo", "command": "direction-right" },
        "page up": { "device": "tivo", "command": "page-up" },
        "page down": { "device": "tivo", "command": "page-down" },

        "tivo": { "device": "tivo"  },
        "select": { "device": "tivo"  },
        "live": { "device": "tivo"  },
        "channel": { "device": "tivo"  },
        "skip forward": { "device": "tivo", "command": "skip-forward" },
        "skip backward": { "device": "tivo", "command": "skip-backward" },
        "channel up": { "device": "tivo", "command": "channel-up" },
        "channel down": { "device": "tivo", "command": "channel-down" },
        "play": { "device": "tivo", "command": "play" },
        "skip commercials": { "device": "tivo", "command": "channel-up" },
        "back": { "device": "tivo", "command": "back" },
        "forward": { "device": "tivo", "command": "skip-forward" },
        "tv-power": { "device": "tv", "command": "power-toggle" },
        "mute": { "device": "tv", "command": "mute" },
        "pause": { "device": "tivo", "command": "pause" },
        "speed": [  { "device": "tivo", "command": "play" },
                    { "device": "tivo", "command": "direction-up" },
                    { "device": "tivo", "command": "select" }
                ],
        "resume": [
                    { "device": "tivo", "command": "direction-left" },
                    { "device": "tivo", "command": "select" }
                ],
        "louder": {
            "device": "tv", "command": "volume-up", "count": 5
        },
        "softer": {
            "device": "tv", "command": "volume-down", "count": 5
        },
        "sleep more": { "device": "url", "command": {
            "small": "https://maker.ifttt.com/trigger/small%20sleep%20more/json/with/key/4ZBybdFfJlCXRCC3gXzZ-",
            "big": "https://maker.ifttt.com/trigger/small%20sleep%20start/json/with/key/4ZBybdFfJlCXRCC3gXzZ-",
        }},
        "sleep": { "device": "url", "command": {
            "small": "https://maker.ifttt.com/trigger/small%20sleep%20start/json/with/key/4ZBybdFfJlCXRCC3gXzZ-",
            "big": "https://maker.ifttt.com/trigger/small%20sleep%20start/json/with/key/4ZBybdFfJlCXRCC3gXzZ-",
        }},
        "fire tv": {
            "device": "tv",
            "command": {
                "big": "inputhdmi3", "small": "inputhdmi1"
            }
        },
        "cable": {
            "device": "tv",
            "command": {
                "big": "inputhdmi2v2", "small": "inputhdmi3"
            }
        }
    }
ac_actions = {
  "one_off": "thermo/one/0",
  "one_cycle_off": "cycle/one/0",
  "one_set": "thermo/set/one",
  "one_warmer": "thermo/one/0.4",
  "one_colder": "thermo/one/-0.3",

  "two_off": "wemo/thermo/two/0",
  "two_cycle_off": "wemo/cycle/two/0",
  "two_set": "wemo/set/two",
  "two_warmer": "wemo/thermo/two/0.6",
  "two_colder": "wemo/thermo/two/-0.3"
}
device_types = {
  "kitchen":{"type":"wemo"},
  "three":{"type":"wemo"},
  "bookshelf":{"type":"wemo"},
  "one":{"type":"wemo"},
  "blinds":{"type":"wemo"},
  "two":{"type":"wemo"},
  "hallway":{"type":"hue"},
  "bathroom":{"type":"hue"},
  "dining room":{"type":"hue"},
  "living room":{"type":"hue"},
  "lamp":{"type":"hue"},
  "unknown":{"type":"unknown"}
}

say_request_responses = {
    "JustSayWhyAlfredIntent": {
        "text": "In the movie \"The Demon Seed,\" the machine the protagonist speaks to at home is named Alfred. Alfred is the home computer system that becomes controlled by the artificial intelligence Proteus IV.",
        "next_text": "Would you like to know more about Alfred?",
        "next_intent": "JustSayWhyAlfredMoreIntent"
    },
    "JustSayWhyAlfredMoreIntent": {
        "text": "At the end of the movie, Alfred impregnates the female protagonist with a demon seed. You don't want to hear more."
    },
    "JustSayMorningRoutineIntent": {
        "text": "Ok Google,,, Set alarm for 30 minutes and play WNYC"
    },
    "JustSayTestIntent": {
        "text": "Just testing"
    }
}
if __name__ == "__main__":
    intents = {}
