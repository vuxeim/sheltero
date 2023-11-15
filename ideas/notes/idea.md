# SAVE FILE

__name: "desc" /class/__

- vault_name: vault's name /str/
- creation_date: save's creation date /datetime/
- balance: currency held /int/
- play_time: time spent in game /deltatime/
- invoked_commands: number of invoked commands /int/
- denizens: vault's inhabitants /list/
    - name: denizen's name /str/
    - surname: denizen's surname /str/
    - level: denizen's level /float/
    - adult: if they are an adult /boolean/
    - expedition: if they are on an expedition /boolean/
    - weapon: assigned weapon /item/
    - cloth: assigned cloth /item/
    - attributes: attributes of each denizen /list/ (https://fallout.fandom.com/wiki/Fallout_Shelter_SPECIAL)
        - strength: /int/
        - perception: /int/
        - endurance: /int/
        - charisma: /int/
        - intelligence: /int/
        - agility: /int/
        - luck: /int/
- storage:  /list/
    - space
        - capacity: available space (taken+free) /int/
        - taken: taken space /int/
    - items
        - name: item's name /str/
        - size: how much space it takes /int/

---

# STAGES
- main menu
- gamestage (input commands etc) (the main view)
- inventory
- map

---

# COMMANDS

__name: - desc /available_in_stages(list)/__

- ? - commands list (w/o description) /[game, inventory, map]/
- ?? - commands list (w/ description) /[game, inventory, map]/
- info - game save statistics /[game, inventory, map]/
- exit - exit save /[game, inventory, map]/
- help - tells that ? and ?? are for help /[game, inventory, map]/
- inv - opens inventory /[game]/

---

# ITEMS


## WEAPONS

__name: / size | damage | cooldown / desc__

- pistol / 2 | 1 | 1 / base pistol

## CLOTHES

__name: / size | attributes_bonus(list) / desc__

- vest / 2 | [2,0,0,0,0,0,0] / gives +2 to strength attribute

## JUNK

(https://fallout.fandom.com/wiki/Fallout_Shelter_junk_items)

__name: / size | tier /__

- duct tape: / 3 | common /

---

# RESOURCES
- water
- power
- food

---

# ITEM TIERS
color | tier
--: | ---
gray | weak
green | common
blue | uncommon
purple | rare
gold | legendary

###### OR

color | name | craft | finding difficulty | source | % | aditional info
:-: | :-: | ---: | --- | :-- | :-: | ---
brown | cursed | craftable | easy | mobs | 15 | gives negative effects, debuff
gray | broken | uncraftable | very easy | mobs | 20 | destroyed, unusable
white | common | craftable | easy | events, mobs | 15 | common in early game
blue | magic | craftable | pretty easy | mobs | 10 | alchemy stuff, potions
green | uncommon | craftable | hard | events, mobs | 5 | less common in early game
red | rare | craftable | very hard | events, mobs, boss | 1 | common in mid game
purple | epic | uncraftable | extremely hard | events, boss | 0,5 | gives magic effects
gold | legendary | uncraftable | impossibly hard | boss | 0,1 | common in late game

###### OR

tier | %
--: | ---
common | 60%
rare | 25%
epic | 10%
super rare | 4%
legendary | 1%

---

# OTHER

nasze zapasy złota kurczą się panie
tam gdzie mieszkam to psy są
"jawed" me at the san diego zoo
if your bones are wet then you're alive