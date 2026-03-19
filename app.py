from flask import Flask, render_template, request, jsonify
 
app = Flask(__name__)
 
RESPONSES = {
    "bowlers": """Great choice! Here are your Bowler options 🎯
 
 Left-Hand Pacers: Zaheer Khan, Trent Boult, Mitchell Starc, Arshdeep Singh
 Right-Hand Fast: Jasprit Bumrah, Pat Cummins, Kagiso Rabada, Mohammed Shami
 Off-Spinners: Ravichandran Ashwin, Nathan Lyon, Moeen Ali
 Leg-Spinners: Yuzvendra Chahal, Adam Zampa, Rashid Khan
 Left-Arm Spin: Ravindra Jadeja, Axar Patel, Shakib Al Hasan
 
Who would you like to add to your XI?""",
 
    "batsmen": """Here are top Batsmen for your Playing XI 🏏
 
Openers: Rohit Sharma, Shubman Gill, David Warner, KL Rahul
 Top-3: Virat Kohli, Steve Smith, Kane Williamson, Babar Azam
 Middle Order: Suryakumar Yadav, Glenn Maxwell, Shreyas Iyer
 Finishers: MS Dhoni, Hardik Pandya, Rinku Singh, Tim David
 
Which position would you like to fill?""",
 
    "allrounders": """Excellent! All-Rounders who can change the game ⚡
 
 Premium: Ben Stokes, Shakib Al Hasan, Ravindra Jadeja
 Bat-first: Marcus Stoinis, Glenn Maxwell, Hardik Pandya
 Bowl-first: Chris Woakes, Mitchell Marsh, Shardul Thakur
 T20 Specialists: Andre Russell, Sam Curran, Axar Patel
 
Select based on your format — T20, ODI, or Test!""",
 
    "wicketkeepers": """Top Wicket-Keepers for your XI 🧤
 
 All-Time Legend: MS Dhoni (MSD) — The Captain Cool
 Current India: Rishabh Pant (aggressive), KL Rahul (steady)
 Global Best: Jos Buttler, Quinton de Kock, Heinrich Klaasen
 Test Specialist: Ben Foakes, Alex Carey
 
MS Dhoni remains the gold standard.
Shall I build a full XI around your WK choice?""",
 
    "t20": """Balanced T20 Playing XI 🔥
 
1️⃣  Rohit Sharma (C) — Aggressive opener
2️⃣  Shubman Gill — Elegant top-order
3️⃣  Virat Kohli — Chase master
4️⃣  Suryakumar Yadav — 360° destructor
5️⃣  Hardik Pandya — All-round powerhouse
6️⃣  Rinku Singh — Clutch finisher
7️⃣  MS Dhoni (WK) — Ice-cold closer
8️⃣  Ravindra Jadeja — Bat + Spin + Field
9️⃣  Jasprit Bumrah — Death-over specialist
🔟  Kuldeep Yadav — Wicket-taking spinner
1️⃣1️⃣ Arshdeep Singh — Left-arm swing
 
Strong batting depth + varied bowling attack!""",
 
    "odi": """Perfect ODI Playing XI 🏆
 
1️⃣  Rohit Sharma (C) — 250+ ODI fifties
2️⃣  Shubman Gill — Young sensation
3️⃣  Virat Kohli — ODI GOAT
4️⃣  Shreyas Iyer — Middle-order anchor
5️⃣  KL Rahul (WK) — Versatile bat + keep
6️⃣  Hardik Pandya — All-round X-factor
7️⃣  Ravindra Jadeja — Bat/Bowl/Field
8️⃣  Kuldeep Yadav — Tournament wicket-taker
9️⃣  Jasprit Bumrah — Best death bowler
🔟  Mohammed Shami — Swing + seam lethal
1️⃣1️⃣ Arshdeep Singh — L-Arm swing maestro""",
 
    "test": """Classic Test Playing XI ⚔️
 
1️⃣  Rohit Sharma (C) — Solid opener
2️⃣  Shubman Gill — Emerging Test star
3️⃣  Virat Kohli — Test cricket's heart
4️⃣  Cheteshwar Pujara — The Wall
5️⃣  Ajinkya Rahane — Composed No.5
6️⃣  Rishabh Pant (WK) — Match-winner
7️⃣  Ravindra Jadeja — Best allrounder
8️⃣  Ravichandran Ashwin — GOAT off-spinner
9️⃣  Jasprit Bumrah — Red-ball genius
🔟  Mohammed Shami — First-class swing
1️⃣1 Mohammed Siraj — Seam & hostility""",
}
 
 
def get_reply(msg):
    m = msg.lower()
    if "bowl" in m:
        return RESPONSES["bowlers"]
    if "bats" in m or "bat" in m:
        return RESPONSES["batsmen"]
    if "all" in m and "round" in m:
        return RESPONSES["allrounders"]
    if any(w in m for w in ["keep", "wicket", "msd", "dhoni", "pant"]):
        return RESPONSES["wicketkeepers"]
    if "t20" in m or "twenty" in m:
        return RESPONSES["t20"]
    if "odi" in m or "one day" in m:
        return RESPONSES["odi"]
    if "test" in m or "red ball" in m:
        return RESPONSES["test"]
    if "rohit" in m:
        return "Rohit Sharma is India's captain and best T20 opener. He averages 30+ in T20Is with a 140+ strike rate. Perfect for the top of the order in all formats! 🏏"
    if "virat" in m or "kohli" in m:
        return "Virat Kohli — arguably the greatest run-scorer in modern cricket. 50+ international centuries, exceptional in all formats, especially in chases. A must-pick! 🔥"
    if "bumrah" in m:
        return "Jasprit Bumrah is the world's best bowler right now. Unplayable death bowling, exceptional yorkers, and phenomenal in T20, ODI, and Test cricket. Lock him in first! 🎯"
    if "jadeja" in m:
        return "Ravindra Jadeja is arguably the world's best all-rounder. Left-arm spin, hard-hitting batting in the lower order, and exceptional fielding. Essential in any format! ⚡"
    return "I'm your Playing XI assistant! Try asking:\n• \"Build me a T20 team\"\n• \"Best ODI Playing XI\"\n• \"Who should open for me?\"\n• \"Suggest spinners\"\n• \"Best all-rounder?\" 🏏"
 
 
@app.route("/")
def index():
    return render_template("index.html")
 
 
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").strip()
    if not user_msg:
        return jsonify({"reply": "Please enter a message."})
    return jsonify({"reply": get_reply(user_msg)})
 
 
@app.route("/quick", methods=["POST"])
def quick():
    data = request.get_json()
    category = data.get("category", "")
    reply = RESPONSES.get(category, "Unknown category.")
    return jsonify({"reply": reply})
 
 
if __name__ == "__main__":
    app.run(debug=True)
 