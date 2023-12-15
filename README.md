# Touhou-Pack
A medium sized mod that changes various things such as Prize drops, junk items, and alters the appearance, names & such of Drive Forms.

- Red P Tiles = HP Orbs
- Yellow Tiles = Munny
- Green Stars = Drive Orbs
- Pink Cherry Tiles = MP Orbs
- Blue Point Tiles = None. Haven't implemented them yet

Some drive forms have been altered visually. Here's a list of what's available

- Fairy Form (Wisdom Form) - A form based off of the Ice Fairy: Cirno
- Scarlet Form (Limit Form) - A form based off of Remilia Scarlet (Beta)

List of currently available/findable Fumo's:
- Reimu = Crystal Orb
- Alice = Seifer's Trophy
- Remilia = "The Struggle" Trophy
- Sanae = Namine's Sketches
- Cirno = Auron's Statue
- Utsuho = Cursed Medallion
- Marisa = Present
- Yuyuko = Decoy Presents
- Koishi = Poster
- Reisen = Extra
- Murasa = Extra
- Satori = Extra
- Aya = Extra
- Sakuya = Extra
- Seija = Extra


Regarding Randomizing Fumo's:

Within this mod there is now a program called "RandomizeFumos.exe". Running this program will shuffle the various fumos
that are within the mod. At the time of writing this, there's the initial 9 stated above and those there are labeled as "Extra".
These extra Fumo's can be discovered through the program. However, in the main directory of this mod there is a file called
"fumo_preferences.json". Within this file you can adjust the value for each fumo; ranging from 0-3. Below are the functions of
each number.

0 = Fumo's will be randomized with the possibility of them not showing up.
1 = Guarantee Randomization; Fumo's with this number will ALWAYS be randomized amongst the 9 potential fumo's.
2 = Don't Randomize; prevents said Fumo to not appear AT ALL.
3 = Default placement; this specifically pertains to the initial 9 fumo's. Placing this number into any of the Extra fumo's will
cause the program to crash.

Speaking of crashes, do not throw in more than 9 1's or the program will fail to randomize and throw an error message; the same can
be said if there aren't enough fumo's to be randomized if there are too many 2's.
