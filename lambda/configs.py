echo_device_map = {
    "amzn1.ask.device.AMA6SNV7ZV7UGFBNWNIETNX7QQGECL34YVRGDCZWMDVJP5OORNHBIGCNLAHEBTRS625BU7J3GFUXWWGNVOT5RM3DEUVRTEWSPJFHIBK6LDBUPNRSOL427OWPOVZVIV2IPE4RZ7KLVBJ3DCDC55E3XRRLKKVQS5ZXCUZH6UTGPVPBGEU7AB2KILZM7BJB54C64BCETAMMIGBRJBSD": "livingroom",
    "amzn1.ask.device.AMAXBAW7JBUZYYPMO6WS4DQCGGCX7PWI63LRD626DQJMJXEDRHPM7FA3DUNXIQUHFSX57ZPXYCI5AFM7RHDHVIATSKHCURO4ETXQXNHTYNV4WSQV4DB2TZWCIPSCF6UF2JGNJRQF2L5W4AYRBJD2MO6P4TH2VLN4SK67D2EFYGO4TX3BKUNXGIHXKTDZIS62ROMBW": "retired",
    "amzn1.ask.device.AMATH75Q4RFEKCXKEU4GLKJEGJ2BEDAVFUWKMIU3LHHVUVGK2NBKJUOO447U55GIUJMLOMJPS7ED6FSQ2GTYQE4LI5CO3PHCYSNTVCGI4ORL5YN2MFY76SSTVL22TYQORFDC2445S3SHZEQAMAO556QQLSCRHZXF3OJJ4DVAQHCXMAQRQSGY2BIIUMVEEVOKLM4CNGV7RD77Z2KP": "bedroom",
    "amzn1.ask.device.AMAXJAPA4OTSER5H6YZ2LVKHQAKL4FTPBEWPSFMKEDCT5Z7UF3EYUREQ7O7F2SHLZJPYFRY3HY4E2DAFNUZYRUD6PUSGNN7ZWAH4MPOJL2UGRFSGEHVTSKVLHFISTGH3UFYSVAIOGHG4ONSE6IIJVYWAUWZRQW2SOWTRHLOTBEVTWSFRRNQA646J7VHEH3D2GDHI22DYP2YX6KI": "kitchen",
    "amzn1.ask.device.AMA5R44WCBSXEWTJ4ILRVBZNPLXHB24I5FTG5E6EQ5P5KB2GDX3IISOHCN6TNXLCSNPNWITESBC4J7DGJDIEN62D2XOVG3U4XRVGP4P6M2YFUEFNDLLGHPMULKO43KM7J5H75ZEB5GPJ77TVQUF7VRGRPRUSBUYXVJ2BP6TY5XTYENYJY733MLJ3NHTDAUD7SKZDWJD6NPJL3CQ": "test",
    "amzn1.ask.device.AMA4UBAJ5A3XUSANPNJWCEHQIYC5FWEARFWN3VKIKUQIV7Q72FXGYLCOXAS56FRTSP2FBYLJKBBYTOLZRX35YKQNJ6QEU7QFWDIXATZTYECP2VYOGV46OHHW35GEOGKOIUS536EVP4NOZ55R5JW7CKKAO4IEZNCXAV3YVT6ARRESWAGAQTRXG65VXYWJGYITC2ABLGONYSMCDLYH": "iphone",
    "amzn1.ask.device.AMAZ5FPGYM43LH3SO7RAQX7UEJFN4Y5IWUVHSMZDNEKHBKUXYG3VOTJAHFHSH3ENLDNHZQINHBCTVYFBLCRWRZKKWASCBORGOILNEMF5WMZ4NTUBF5FW4FK7SFLVJ6G2GQ3TKHXUEPHKI7NYCZXZUY6L3DIZQ6UFJRUSNQVRITLLHSN2YH3QDZ36DM2UJ32NVPPQJH2ANYSFY363": "desk"
}
room_map = {'small': 'small', 'bedroom': 'small', 'big': 'big', 'livingroom': 'big', 'desk': 'big'}
valid_devices = ['tv', 'tivo']
station_to_channel_map = {
    "cnn": 600, "abc": 507, "nbc": 502, "cbs": 502, "fox": 505, "espn": 570, "hbo": 899, "showtime": 865,
    "tiny": 4, "huge": 1000
}
intents_command_map = {
    "ScreenPowerIntent": {
        "device": "tv",
    },
    "ChannelIntent": {
        "device": "tivo",
    },
    "ScreenActionIntent": {
        "device": None,
        "action_device_map": {
            "power": [ "tv", "power-toggle" ],
            "mute": [ "tv", "mute" ],
            "roku": [ "tv", "roku" ],
            "pause": ["tivo", "pause"],
            "fire tv": [ "tv", {"big": "inputhdmi3", "small": "inputhdmi1"} ],
            "cable": [ "tv", {"big": "inputhdmi2v2", "small": "inputhdmi3"} ],
        }
    }
}
device_names_map = {
    "tv": {
        "small": {
            "device": "bedroom-tv",
            "short": "stv"
        },
        "big": {
            "device": "living-room-tv",
            "short": "btv"
        }
    },
    "tivo": {
        "small": {
            "device": "bedroom-tivo",
            "short": "st"
        },
        "big": {
            "device": "living-room-tivo",
            "short": "bt"
        }
    }
}
