import { reactive} from "vue"


const state = reactive({  
	// gamesList: {"1": {"gameID": "1", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "2": {"gameID": "2", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
	//           "5": {"gameID": "5", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "6": {"gameID": "6", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
	//           "8": {"gameID": "8", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "9": {"gameID": "2", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']},
	//           "10": {"gameID": "10", "started": "False", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}, "11": {"gameID": "11", "started": "True", "users": ['2304820348', '202308402834', '20384023840328', '2081023823048208', '20384023804']}
	// },
	gamesList: [],
	nextToken: null,

	// cards: {"1":{"runeVal":5,"spellVal":3,"runeType":"fire","spellType":1,"cost":{"wind":2,"fire":5,"earth":10,"water":2,"nature":3,"solar":8}},"2":{"runeVal":7,"spellVal":6,"runeType":"solar","spellType":2,"cost":{"wind":2,"solar":7,"water":3}},"3":{"runeVal":9,"spellVal":10,"runeType":"water","spellType":1,"cost":{"wind":2,"nature":10}},"4":{"runeVal":8,"spellVal":8,"runeType":"arcane","spellType":2,"cost":{"arcane":8,"solar":5,"water":3}},"5":{"runeVal":10,"spellVal":4,"runeType":"nature","spellType":1,"cost":{"earth":10,"water":3,"solar":5,"dark":6}},"6":{"runeVal":3,"spellVal":1,"runeType":"wind","spellType":1,"cost":{"dark":8,"water":11}},"7":{"runeVal":6,"spellVal":9,"runeType":"wind","spellType":1,"cost":{"wind":2}},"8":{"runeVal":4,"spellVal":5,"runeType":"wind","spellType":1,"cost":{"dark":10,"solar":5,"fire":11,"wind":2}}},
	// dragons: {"Deep-sea Dragon": {"cost": {"water": 20,"dark": 20},"icon": "Deep-sea_Dragon.png","shield": 8,"damage": 2}, "Nova Dragon": {"cost": {"fire": 20,"solar": 20},"icon": "Nova_Dragon.png","shield": 8,"damage": 2}, "Swamp Dragon": {"cost": {"water": 20,"nature": 20},"icon": "Swamp_Dragon.png","shield": 8,"damage": 2},"Cloud Dragon": {"cost": {"water": 20,"wind": 20},"icon": "Cloud_Dragon.png","shield": 8,"damage": 2},},
	// users: {"1822372397923":{"health":12,"shield":5,"shieldType":"fire","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80},"391234972397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "59123492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "15123492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "11113492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}, "2222492397":{"health":10,"shield":5,"shieldType":"water","runes":{"fire":1,"water":2,"earth":5,"arcane":3,"nature":3,"solar":6,"dark":2,"wind":2},"timer":80}},
	logs: [":arcane:", ":fire: runes", 'log2', 'log3', 'log4', 'log5 took a :fire: rune worth x6 affinity and played a card to deal x5 :solar: to everyone', 'log6', 'log7', 'log8', 'log9', 'log10', 'log11', 'log12', 'log13', 'log14',
	":fire: runes"],
	
	
	isTurn: true,
	turnSecond: '0',
	turnMinute: '0',
	turnHour: '0',
	turnDay: '0',
	countDate: null,
	timerId: null,
	current_game_card_shop: [{'card': {'rune': 'FIRE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}, {'card': {'rune': 'ARCANE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}, {'card': {'rune': 'ARCANE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}, {'card': {'rune': 'ARCANE', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}, {'card': {'rune': 'EARTH', 'type': 'SHIELD', 'affinity': 8, 'power': 4}, 'cost': {'NATURE': 2, 'DARK': 8, 'ARCANE': 7, 'SOLAR': 5}}],
	current_game_dragon_shop: [{'dragon': {'type': 'THORN', 'runes': ['NATURE', 'ARCANE']}, 'cost': {'NATURE': 20, 'ARCANE': 20}}],
  current_game_users: [
    {
      "sid": "WWxbPZRWHvr_L7lNAAAF",
      "hp": 10,
      "shield": {
        "rune": null,
        "power": 0
      },
      "runes": {
        "ARCANE": 0,
        "SOLAR": 2,
        "DARK": 0,
        "NATURE": 2,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "cards": [
        {
          "card": {
            "rune": "EARTH",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        }
      ],
      "affinities": {
        "ARCANE": 0,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 0,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "dragons": [
        {
          "dragon": {
            "type": "VOID",
            "runes": ["ARCANE", "DARK"]
          }
        },
        {
          "dragon": {
            "type": "CLOUD",
            "runes": ["WIND", "WATER"]
          }
        }
      ],
      "isDead": false,
      "vines": 0,
      "burn": 0,
      "display_name": "client-player"
    },
    {
      "sid": "other_sid1",
      "hp": 5,
      "shield": {
        "rune": null,
        "power": 0
      },
      "runes": {
        "ARCANE": 0,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 2,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "cards": [
        {
          "card": {
            "rune": "EARTH",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        }
      ],
      "affinities": {
        "ARCANE": 7,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 0,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "dragons": [],
      "isDead": true,
      "vines": 10,
      "burn": 1,
      "display_name": "other-player1"
    },
    {
      "sid": "other_sid2",
      "hp": 10,
      "shield": {
        "rune": null,
        "power": 0
      },
      "runes": {
        "ARCANE": 0,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 2,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "cards": [
        {
          "card": {
            "rune": "EARTH",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        },
        {
          "card": {
            "rune": "ARCANE",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        },
        {
          "card": {
            "rune": "ARCANE",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        }
      ],
      "affinities": {
        "ARCANE": 7,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 0,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "dragons": [],
      "isDead": false,
      "vines": 0,
      "display_name": "other-player2"
    },
    {
      "sid": "other_sid3",
      "hp": 10,
      "shield": {
        "rune": null,
        "power": 0
      },
      "runes": {
        "ARCANE": 0,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 2,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "cards": [
        {
          "card": {
            "rune": "EARTH",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        },
        {
          "card": {
            "rune": "ARCANE",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        },
        {
          "card": {
            "rune": "ARCANE",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        }
      ],
      "affinities": {
        "ARCANE": 7,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 0,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "dragons": [],
      "isDead": false,
      "vines": 0,
      "display_name": "other-player3"
    },
    {
      "sid": "other_sid4",
      "hp": 10,
      "shield": {
        "rune": null,
        "power": 0
      },
      "runes": {
        "ARCANE": 0,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 2,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "cards": [
        {
          "card": {
            "rune": "EARTH",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        },
        {
          "card": {
            "rune": "ARCANE",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        },
        {
          "card": {
            "rune": "ARCANE",
            "type": "ATTACK",
            "affinity": 7,
            "power": 7
          }
        }
      ],
      "affinities": {
        "ARCANE": 7,
        "SOLAR": 0,
        "DARK": 0,
        "NATURE": 0,
        "EARTH": 0,
        "WIND": 0,
        "WATER": 0,
        "FIRE": 0
      },
      "dragons": [],
      "isDead": false,
      "vines": 0,
      "display_name": "other-player4"
    }
  ],
	current_room_id: '0',
	ingame: false,
	gameStarted: false,
	userName: '',
	attacking: false,
	crafting: true,
	buyingDragonCards: false,
	buyingShopCards: false,
	showHand: false,
	showHandModal: false,
	showHandModalIndex: 0,
	currentTurnSid: 'WWxbPZRWHvr_L7lNAAAF', // the sid of the player whose turn it is
	sid: 'WWxbPZRWHvr_L7lNAAAF',
	showGameConfigModal: false,
	configShopSize: 5,
	configTotalDragons: 2,
	configRunesPerTurn: 5,
	configPlayerStartHealth: 10,
	configMaxPlayers: 8,
	configTurnTimer: 30,
	
	showChat: false,
	showSettings: false,
})

export default {
  state
}