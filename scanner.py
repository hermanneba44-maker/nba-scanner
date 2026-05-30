import requests, schedule, time
from datetime import datetime

TOKEN = "8698830339:AAHpdpizzC-T387_eATBIwosKeOTRk6-P50"
CHAT = "5304818625"
KEY = "12ed9fa2b7453e962298eda712b13275"

def send(msg):
    try:
        requests.post("https://api.telegram.org/bot"+TOKEN+"/sendMessage", json={"chat_id":CHAT,"text":msg}, timeout=10)
    except Exception as e:
        print("Error:",e)

def scan():
    print("Scanning...", datetime.now().strftime("%H:%M:%S"))
    try:
        r = requests.get("https://api.the-odds-api.com/v4/sports/basketball_nba/odds", params={"apiKey":KEY,"regions":"us","markets":"totals","oddsFormat":"american"}, timeout=10)
        games = r.json()
        if not games:
            print("No games today")
            return
        for g in games:
            home = g["home_team"]
            away = g["away_team"]
            lines = []
            for b in g.get("bookmakers",[]):
                for m in b.get("markets",[]):
                    if m["key"]=="totals":
                        for o in m["outcomes"]:
                            if o["name"]=="Over":
                                lines.append(o["point"])
            if lines:
                avg = round(sum(lines)/len(lines),1)
                high = max(lines)
                low = min(lines)
                diff = round(high-low,1)
                if diff >= 0:
                    lean = "OVER" if lines.count(high) > lines.count(low) else "UNDER"
                    msg = f"NBA VALUE ALERT\n\n{away} @ {home}\n\nLine: {avg}\nLean: {lean}\nBest OVER: {high}\nBest UNDER: {low}\nBook spread: {diff} pts\nBooks checked: {len(lines)}\n\nVerify before betting"
                    send(msg)
    except Exception as e:
        print("Scan error:",e)

send("NBA Scanner started - 24/7 Mode")
scan()
schedule.every(5).minutes.do(scan)
while True:
    schedule.run_pending()
    time.sleep(30)
