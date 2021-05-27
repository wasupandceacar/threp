from collections import defaultdict

skeys = ['○', '↑', '↓',  '↓',  '←',  '↖',   '↙',    '↖',    '→',  '↗',   '↘',    '↗',    '←',    '↖',      '↙',      '↖']
kkeys = ['○', '↑', '↓', '↑↓', '←', '↑←', '↓←', '↑↓←', '→', '↑→', '↓→', '↑↓→', '←→', '↑←→', '↓←→', '←↓←→']

oldwork_magicnumber_flc = {
    0x50523654: '06',
    0x50523754: '07',
    0x50523854: '08',
    0x50523954: '09'
}

week_array=("Sun.", "Mon.", "Tues.", "Wed.", "Thrs.", "Fri.", "Sat.")

work_attr_array={
           '10':[0x72303174, 0x4c, 0x50, 0x54, 0x58, 0x5c, 0x64, 0x1c4, 0x10, 0x400, 0xaa, 0xe1, 0x80, 0x3d, 0x7a, 0x0, 10, 0x48, 0xc],
           '11':[0x72313174, 0x58, 0x5c, 0x60, 0x64, 0x68, 0x70, 0x90, 0x14, 0x800, 0xaa, 0xe1, 0x40, 0x3d, 0x7a, 0x0, 10, 0x54, 0xc],
           '12':[0x72323174, 0x58, 0x5c, 0x60, 0x64, 0x68, 0x70, 0xa0, 0x14, 0x800, 0x5e, 0xe1, 0x40, 0x7d, 0x3a, 0x0, 10, 0x54, 0xc],
           '13':[0x72333174, 0x58, 0x5c, 0x60, 0x64, 0x68, 0x84, 0xc4, 0x14, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x10, 10, 0x54, 0xc],
           '14':[0x72333174, 0x78, 0x7c, 0x80, 0x84, 0x88, 0xa4, 0xdc, 0x14, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x10, 10, 0x74, 0xc],
           '15':[0x72353174, 0x88, 0x8c, 0x90, 0x94, 0x98, 0xc8, 0x238, 0x14, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a,  -0x24, 10, 0x84, 0xc],
           '16':[0x72363174, 0x80, 0x84, 0x9c, 0x8c, 0x90, 0xc8, 0x294, 0x14, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x28, 10, 0x7c, 0xc],
           '128':[0x72383231, 0x58, 0x5c, 0x60, 0x64, 0x68, 0x70, 0x90, 0x14, 0x800, 0x5e, 0xe7, 0x80, 0x7d, 0x36, 0x0, 10, 0x54, 0xc],
           '125':[0x35323174, 0x54, 0x58, 0x60, 0x64, 0x68, 0x70, 0xa0, 0x14, 0x800, 0x5e, 0xe1, 0x40, 0x7d, 0x3a, -0x8, 1, 0x54, 0xc],
           '143':[0x33343174, 0x80, 0x84, 0x88, 0x8c, 0x90, 0xa4, 0x10c, 0x1c, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, 0x4, 10, 0x7c, 0x14],
           '95':[0x72353974, 0x4c, 0x50, 0x2, 0x3, 0x64, 0xe8, 0x10, 0x14, 0x400, 0xaa, 0xe1, 0x80, 0x3d, 0x7a, 0x0, 1, 0xe0, 0x10],
           '165':[0x36353174, 0x90, 0xff, 0x90, 0x8c, 0xff, 0x98, 0x08, 0x1c, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, 0x08, 1, 0xff, 0x14],
           '17':[0x72373174, 0x84, 0x88, 0x8c, 0x90, 0x94, 0xc8, 0x158, 0x18, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x28, 10, 0x80, 0x10],
           '18':[0x72383174, 0xa8, 0xac, 0xb0, 0xb4, 0xb8, 0x144, 0x126c, 0x18, 0x400, 0x5c, 0xe1, 0x100, 0x7d, 0x3a, -0x7c, 10, 0xa4, 0x10]}

work_attr = defaultdict(dict)

work_attr_key = ['magic_number', 'stage', 'character', 'ctype', 'rank',
                 'clear', 'stagedata', 'replaydata_offset', 'totalscoredata',
                 'decode_var1', 'decode_var2', 'decode_var3', 'decode_var4',
                 'decode_var5', 'decode_var6', 'stagedata_offset',
                 'score_rate', 'slowrate', 'date']

for key, value in work_attr_array.items():
    for idx, attr_key in enumerate(work_attr_key):
        work_attr[key][attr_key] = value[idx]

types_dic = {
    '10': {
        'character': ["Reimu", "Marisa"],
        'ctype': ["A", "B", "C"],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    },
    '11': {
        'character': ["Reimu", "Marisa"],
        'ctype': ["A", "B", "C"],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    },
    '12': {
        'character': ["Reimu", "Marisa", "Sanae"],
        'ctype': ["A", "B"],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    },
    '13': {
        'character': ["Reimu", "Marisa", "Sanae", "Youmu"],
        'ctype': [],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra", "overdrive"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    },
    '14': {
        'character': ["Reimu", "Marisa", "Sakuya"],
        'ctype': ["A", "B"],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    },
    '15': {
        'character': ["Reimu", "Marisa", "Sanae", "Reisen"],
        'ctype': [],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    },
    '16': {
        'character': ["Reimu", "Cirno", "Aya", "Marisa"],
        'ctype': ["Spring", "Summer", "Autumn", "Winter", "Full"],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    },
    '128': {
        'character': ["A1", "A2", "B1", "B2", "C1", "C2", "Extra"],
        'ctype': [],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': ['dummy', 'A1-1','A1-2','A1-3','A2-2','A2-3','B1-1','B1-2','B1-3','B2-2','B2-3','C1-1','C1-2','C1-3','C2-2','C2-3','Extra','All','All','All','All','All','All','All']
    },
    '125': {
        'character': ["Aya", "Hatate"],
        'ctype': [f"{i+1}" for i in range(12)] + ["EX", "SP"],
        'rank': [f"{i+1}" for i in range(9)],
        'clear': []
    },
    '143': {
        'character': [],
        'ctype': [f"{i+1}" for i in range(10)],
        'rank': [f"{i+1}" for i in range(10)],
        'clear': []
    },
    '95': {
        'character': [],
        'ctype': [f"{i+1}" for i in range(10)] + ["EX"],
        'rank': [f"{i+1}" for i in range(8)],
        'clear': []
    },
    '165': {
        'character': ["Usami"],
        'ctype': [f"{i+1}" for i in range(6)],
        'rank': [week_array[i % 7] for i in range(7)] + [f"Inner-{week_array[i % 7]}" for i in range(7, 14)] + [f"Nightmare-{week_array[i % 7]}" for i in range(14, 21)],
        'clear': []
    },
    '17': {
        'character': ["Reimu", "Marisa", "Youmu"],
        'ctype': ["Wolf", "Otter", "Eagle"],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    },
    '18': {
        'character': ["Reimu", "Marisa", "Sakuya", "Sanae"],
        'ctype': [],
        'rank': ["Easy", "Normal", "Hard", "Lunatic", "Extra"],
        'clear': [f"Stage {i}" for i in range(7)] + ["Extra", "All"]
    }
}