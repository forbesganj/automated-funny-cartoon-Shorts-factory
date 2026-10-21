import json, random, datetime, sys

# Broad, family-friendly comedy topics. A deterministic daily seed makes the
# selected topic reproducible for a given date.
STORIES = [
    {"category":"Everyday Life","title":"Five More Minutes","scenes":[
        {"start":0,"end":5,"action":"look","caption":"ALARM: 7:00 AM"},
        {"start":5,"end":11,"action":"shake","caption":"JUST FIVE MORE MINUTES"},
        {"start":11,"end":17,"action":"look","caption":"SOMEHOW... 9:47 AM"},
        {"start":17,"end":24,"action":"enter","caption":"GET READY IN 30 SECONDS"},
        {"start":24,"end":30,"action":"help","caption":"TOMORROW I'LL WAKE UP EARLY"}],
     "dialogue":[{"time":6,"text":"Five more minutes."},{"time":13,"text":"WHAT YEAR IS IT?"},{"time":25,"text":"Tomorrow. Definitely."}]},
    {"category":"School & College","title":"Exam Hall Genius","scenes":[
        {"start":0,"end":5,"action":"enter","caption":"I STUDIED EVERYTHING"},
        {"start":5,"end":11,"action":"look","caption":"QUESTION 1: EXPLAIN YOURSELF"},
        {"start":11,"end":17,"action":"shake","caption":"BRAIN: LOADING..."},
        {"start":17,"end":24,"action":"pose","caption":"WRITE THE DATE VERY NEATLY"},
        {"start":24,"end":30,"action":"help","caption":"SIR, CAN I GET PARTIAL MARKS?"}],
     "dialogue":[{"time":6,"text":"I know this. I KNOW this."},{"time":13,"text":"404: MEMORY NOT FOUND"},{"time":25,"text":"At least my handwriting passed."}]},
    {"category":"Office & Money","title":"Salary Day","scenes":[
        {"start":0,"end":5,"action":"pose","caption":"SALARY JUST ARRIVED"},
        {"start":5,"end":11,"action":"enter","caption":"I'M FINALLY RICH"},
        {"start":11,"end":17,"action":"look","caption":"RENT. BILLS. EMIs."},
        {"start":17,"end":24,"action":"shake","caption":"BALANCE: EMOTIONAL DAMAGE"},
        {"start":24,"end":30,"action":"help","caption":"WHO WANTS TO SPLIT ONE SAMOSA?"}],
     "dialogue":[{"time":6,"text":"Tonight, we celebrate!"},{"time":13,"text":"Rent has entered the chat."},{"time":25,"text":"I accept UPI."}]},
    {"category":"Relationships","title":"The Three Dots","scenes":[
        {"start":0,"end":5,"action":"look","caption":"THEY'RE TYPING..."},
        {"start":5,"end":11,"action":"pose","caption":"IT'S A LONG MESSAGE"},
        {"start":11,"end":17,"action":"shake","caption":"THEY STOPPED TYPING"},
        {"start":17,"end":24,"action":"look","caption":"REPLAY EVERY CONVERSATION"},
        {"start":24,"end":30,"action":"help","caption":"THE MESSAGE: OK"}],
     "dialogue":[{"time":6,"text":"This is it. The big confession."},{"time":13,"text":"Why did they stop? WHY?"},{"time":25,"text":"Just... OK?"}]},
    {"category":"Friends","title":"The Helpful Friend","scenes":[
        {"start":0,"end":5,"action":"enter","caption":"BRO, I NEED ADVICE"},
        {"start":5,"end":11,"action":"pose","caption":"I'M ALWAYS HERE FOR YOU"},
        {"start":11,"end":17,"action":"look","caption":"SO I QUIT MY JOB..."},
        {"start":17,"end":24,"action":"shake","caption":"WAIT. YOU DID WHAT?"},
        {"start":24,"end":30,"action":"help","caption":"I'M HERE EMOTIONALLY. NOT FINANCIALLY."}],
     "dialogue":[{"time":6,"text":"Tell me everything."},{"time":13,"text":"I quit yesterday."},{"time":25,"text":"Have you tried updating your resume?"}]},
    {"category":"Gaming & Tech","title":"One Percent Battery","scenes":[
        {"start":0,"end":5,"action":"look","caption":"BATTERY: 1%"},
        {"start":5,"end":11,"action":"enter","caption":"CHARGER: SOMEWHERE IN THE HOUSE"},
        {"start":11,"end":17,"action":"shake","caption":"SCREEN DIMMING..."},
        {"start":17,"end":24,"action":"squat","caption":"SPRINT LIKE AN OLYMPIAN"},
        {"start":24,"end":30,"action":"help","caption":"FOUND IT. WRONG CABLE."}],
     "dialogue":[{"time":6,"text":"Stay with me, buddy."},{"time":13,"text":"Don't you dare turn off!"},{"time":25,"text":"It's USB... something."}]},
    {"category":"Family","title":"Guests Are Coming","scenes":[
        {"start":0,"end":5,"action":"look","caption":"MOM: GUESTS IN 5 MINUTES"},
        {"start":5,"end":11,"action":"shake","caption":"THE HOUSE IS A DISASTER"},
        {"start":11,"end":17,"action":"enter","caption":"HIDE EVERYTHING IN ONE ROOM"},
        {"start":17,"end":24,"action":"pose","caption":"LOOKS PERFECT FROM HERE"},
        {"start":24,"end":30,"action":"help","caption":"PLEASE DON'T OPEN THAT DOOR"}],
     "dialogue":[{"time":6,"text":"FIVE MINUTES?!"},{"time":13,"text":"Put it all in my room!"},{"time":25,"text":"That's the storage room now."}]},
    {"category":"Gym","title":"The Tiny Dumbbell","scenes":[
        {"start":0,"end":5,"action":"enter","caption":"FIRST DAY AT THE GYM"},
        {"start":5,"end":11,"action":"lift","caption":"LIGHT WEIGHT. BIG DREAMS."},
        {"start":11,"end":17,"action":"shake","caption":"WHY IS IT SO HEAVY?"},
        {"start":17,"end":24,"action":"pose","caption":"ACT NATURAL."},
        {"start":24,"end":30,"action":"help","caption":"NEED HELP?"}],
     "dialogue":[{"time":5.5,"text":"Easy. I've got this."},{"time":13,"text":"Is this one made of iron?"},{"time":25,"text":"NEED HELP?"}]},
    {"category":"Food","title":"Midnight Snack Mission","scenes":[
        {"start":0,"end":5,"action":"look","caption":"2:00 AM. EVERYONE ASLEEP."},
        {"start":5,"end":11,"action":"enter","caption":"SNEAK TO THE FRIDGE"},
        {"start":11,"end":17,"action":"shake","caption":"THE FLOORBOARD SQUEAKS"},
        {"start":17,"end":24,"action":"look","caption":"DAD: WHAT ARE YOU DOING?"},
        {"start":24,"end":30,"action":"help","caption":"JUST CHECKING THE TEMPERATURE"}],
     "dialogue":[{"time":6,"text":"Operation Sandwich."},{"time":13,"text":"WHY IS THIS HOUSE SO LOUD?"},{"time":25,"text":"Food safety, dad."}]},
    {"category":"Social Awkwardness","title":"Wrong Person Wave","scenes":[
        {"start":0,"end":5,"action":"pose","caption":"SOMEONE WAVED AT ME!"},
        {"start":5,"end":11,"action":"pose","caption":"WAVE BACK. BE FRIENDLY."},
        {"start":11,"end":17,"action":"look","caption":"THEY WERE WAVING BEHIND ME"},
        {"start":17,"end":24,"action":"shake","caption":"COMMIT TO THE WAVE"},
        {"start":24,"end":30,"action":"help","caption":"NOW IT'S A FULL BODY WAVE"}],
     "dialogue":[{"time":6,"text":"Oh hey! You!"},{"time":13,"text":"...they know someone behind me."},{"time":25,"text":"Just stretching my arm."}]},
    {"category":"Online Shopping","title":"The Delivery Tracker","scenes":[
        {"start":0,"end":5,"action":"look","caption":"ORDER PLACED"},
        {"start":5,"end":11,"action":"enter","caption":"OUT FOR DELIVERY"},
        {"start":11,"end":17,"action":"look","caption":"ARRIVING TODAY"},
        {"start":17,"end":24,"action":"shake","caption":"DELIVERY PARTNER: 2 STREETS AWAY"},
        {"start":24,"end":30,"action":"help","caption":"DELIVERED. TO THE WRONG HOUSE."}],
     "dialogue":[{"time":6,"text":"I shall track every second."},{"time":13,"text":"They're so close!"},{"time":25,"text":"Who is Mr. Sharma?"}]},
    {"category":"Pets","title":"The Cat's Owner","scenes":[
        {"start":0,"end":5,"action":"pose","caption":"I AM THE OWNER"},
        {"start":5,"end":11,"action":"enter","caption":"I BUY THE FOOD"},
        {"start":11,"end":17,"action":"look","caption":"I CLEAN THE LITTER"},
        {"start":17,"end":24,"action":"shake","caption":"THE CAT IGNORES ME"},
        {"start":24,"end":30,"action":"help","caption":"I LIVE HERE AS STAFF"}],
     "dialogue":[{"time":6,"text":"This is my house."},{"time":13,"text":"I pay for everything!"},{"time":25,"text":"Meow."}]},
]

def make_story(seed=None):
    if seed is None:
        seed = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
    rng = random.Random(seed)
    story = dict(rng.choice(STORIES))
    story["date"] = seed
    story["seed"] = seed
    story["scenes"] = [dict(x) for x in story["scenes"]]
    story["dialogue"] = [dict(x) for x in story["dialogue"]]
    return story

if __name__ == "__main__":
    seed = sys.argv[1] if len(sys.argv) > 1 else None
    out = sys.argv[2] if len(sys.argv) > 2 else "script.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(make_story(seed), f, indent=2, ensure_ascii=False)
    print(f"Wrote {out}")
