# Telegram Cell Biology Quiz Bot
# 49 questions — Page 1 of the supplied PDF
# IMPORTANT: Never share your BOT_TOKEN publicly.

import json
import sqlite3
import os
import time
import urllib.parse
import urllib.request

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_FILE = "quiz_results.db"

QUESTIONS = [('कोशिका की खोज किसने की थी?', ['रॉबर्ट हुक', 'रुडोल्फ विरचो', 'रॉबर्ट ब्राउन', 'ल्यूवेनहॉक'], 0), ('रॉबर्ट हुक ने कोशिका की खोज कब की थी?', ['1831 ई.', '1665 ई.', '1855 ई.', '1900 ई.'], 1), ('जीवित कोशिका का प्रथम अवलोकन किसने किया?', ['रॉबर्ट हुक', 'एंटोनी वॉन ल्यूवेनहॉक', 'श्लाइडेन', 'रुडोल्फ विरचो'], 1), ('कोशिका सिद्धांत किसने दिया था?', ['श्लाइडेन और श्वान', 'हुक और ब्राउन', 'विरचो और हुक', 'सिंगर और निकोलसन'], 0), ('कोशिका सिद्धांत का विस्तार किसने किया?', ['रॉबर्ट ब्राउन', 'रुडोल्फ विरचो', 'रॉबर्ट हुक', 'ऑल्टमैन'], 1), ('सभी जीव किससे बने हैं?', ['ऊतकों से', 'अंगों से', 'कोशिकाओं से', 'प्रोटीन से'], 2), ('कोशिका को जीवन की क्या कहा जाता है?', ['ऊर्जा इकाई', 'संरचनात्मक एवं क्रियात्मक इकाई', 'आनुवंशिक इकाई', 'सुरक्षात्मक इकाई'], 1), ('सबसे छोटी स्वतंत्र रूप से जीवित कोशिका कौन-सी है?', ['बैक्टीरिया', 'माइकोप्लाज्मा', 'न्यूरॉन', 'अंडाणु'], 1), ('मानव शरीर की सबसे बड़ी कोशिका कौन-सी है?', ['न्यूरॉन', 'अंडाणु', 'माइकोप्लाज्मा', 'मांसपेशी कोशिका'], 1), ('मानव शरीर की सबसे लंबी कोशिका कौन-सी है?', ['अंडाणु', 'तंत्रिका कोशिका (न्यूरॉन)', 'लाल रक्त कोशिका', 'माइकोप्लाज्मा'], 1), ('सबसे बड़ी एकल कोशिका कौन-सी है?', ['मुर्गी का अंडा', 'शुतुरमुर्ग का अंडा', 'मानव अंडाणु', 'न्यूरॉन'], 1), ('प्रोकैरियोटिक कोशिका का उदाहरण क्या है?', ['पादप कोशिका', 'जंतु कोशिका', 'बैक्टीरिया', 'कवक कोशिका'], 2), ('यूकैरियोटिक कोशिका का उदाहरण क्या है?', ['बैक्टीरिया', 'पादप एवं जंतु कोशिका', 'माइकोप्लाज्मा', 'वायरस'], 1), ('क्या प्रोकैरियोटिक कोशिका में वास्तविक केंद्रक होता है?', ['हाँ', 'नहीं', 'केवल पौधों में', 'केवल जंतुओं में'], 1), ('यूकैरियोटिक कोशिका का केंद्रक कैसा होता है?', ['झिल्ली से घिरा हुआ', 'न्यूक्लॉयड में', 'बिना झिल्ली का', 'कोशिका भित्ति से घिरा'], 0), ('प्रोकैरियोटिक कोशिका का DNA कहाँ होता है?', ['केंद्रक में', 'न्यूक्लॉयड में', 'माइटोकॉन्ड्रिया में', 'राइबोसोम में'], 1), ('कोशिका का नियंत्रण केंद्र क्या है?', ['माइटोकॉन्ड्रिया', 'केंद्रक', 'साइटोप्लाज्म', 'कोशिका भित्ति'], 1), ('केंद्रक की खोज किसने की थी?', ['रॉबर्ट ब्राउन', 'रॉबर्ट हुक', 'श्वान', 'सिंगर'], 0), ('रॉबर्ट ब्राउन ने केंद्रक की खोज कब की?', ['1665 ई.', '1831 ई.', '1855 ई.', '1900 ई.'], 1), ('केंद्रक के अंदर क्या होता है?', ['क्रोमैटिन', 'सेलुलोज', 'काइटिन', 'पेप्टिडोग्लाइकन'], 0), ('क्रोमैटिन किससे बना होता है?', ['लिपिड और प्रोटीन', 'DNA और प्रोटीन', 'RNA और लिपिड', 'सेलुलोज और DNA'], 1), ('जीन क्या है?', ['प्रोटीन का भाग', 'DNA का भाग', 'RNA का भाग', 'कोशिका का भाग'], 1), ('DNA का पूरा नाम क्या है?', ['Deoxyribonucleic Acid', 'Ribonucleic Acid', 'Adenosine Triphosphate', 'Deoxyribose Nuclear Acid'], 0), ('RNA का पूरा नाम क्या है?', ['Ribonucleic Acid', 'Deoxyribonucleic Acid', 'Adenosine Triphosphate', 'Ribosomal Nuclear Acid'], 0), ('DNA का मुख्य कार्य क्या है?', ['ऊर्जा उत्पादन', 'आनुवंशिक सूचना का संचय एवं संचरण', 'कोशिका को आकार देना', 'प्रोटीन को तोड़ना'], 1), ('कोशिका का बाहरी आवरण क्या है?', ['कोशिका भित्ति', 'कोशिका झिल्ली', 'केंद्रक', 'साइटोप्लाज्म'], 1), ('कोशिका झिल्ली का दूसरा नाम क्या है?', ['प्लाज्मा झिल्ली', 'न्यूक्लियर झिल्ली', 'सेलुलोज झिल्ली', 'क्रोमैटिन झिल्ली'], 0), ('कोशिका झिल्ली कैसी होती है?', ['पूर्णतः पारगम्य', 'चयनात्मक पारगम्य', 'अपारगम्य', 'केवल जल के लिए पारगम्य'], 1), ('कोशिका झिल्ली के मुख्य घटक क्या हैं?', ['लिपिड और प्रोटीन', 'DNA और RNA', 'सेलुलोज और काइटिन', 'ATP और DNA'], 0), ('कोशिका झिल्ली का मॉडल कौन-सा है?', ['द्रव मोजेक मॉडल', 'लॉक-एंड-की मॉडल', 'डबल हेलिक्स मॉडल', 'कोशिका सिद्धांत'], 0), ('द्रव मोजेक मॉडल किसने दिया?', ['श्लाइडेन और श्वान', 'सिंगर और निकोलसन', 'हुक और ब्राउन', 'विरचो और ऑल्टमैन'], 1), ('कोशिका भित्ति किसमें होती है?', ['पादप कोशिका में', 'केवल मानव कोशिका में', 'केवल जंतु कोशिका में', 'न्यूरॉन में'], 0), ('पादप कोशिका भित्ति किसकी बनी होती है?', ['काइटिन', 'सेलुलोज', 'पेप्टिडोग्लाइकन', 'प्रोटीन'], 1), ('कवक कोशिका भित्ति किसकी बनी होती है?', ['सेलुलोज', 'काइटिन', 'पेप्टिडोग्लाइकन', 'लिपिड'], 1), ('बैक्टीरिया की कोशिका भित्ति किसकी बनी होती है?', ['सेलुलोज', 'काइटिन', 'पेप्टिडोग्लाइकन', 'DNA'], 2), ('पादप कोशिका भित्ति का कार्य क्या है?', ['ऊर्जा उत्पादन', 'सुरक्षा एवं आकार प्रदान करना', 'आनुवंशिक सूचना का संचय', 'प्रोटीन संश्लेषण'], 1), ('जेली जैसा पदार्थ क्या है?', ['केंद्रक', 'साइटोप्लाज्म', 'माइटोकॉन्ड्रिया', 'कोशिका भित्ति'], 1), ('साइटोप्लाज्म में क्या होता है?', ['केवल DNA', 'कोशिकांग', 'केवल RNA', 'केवल ATP'], 1), ('कोशिकांगों के अध्ययन को क्या कहते हैं?', ['कोशिका जीवविज्ञान', 'आनुवंशिकी', 'ऊतक विज्ञान', 'पारिस्थितिकी'], 0), ('कोशिका का ऊर्जा गृह किसे कहा जाता है?', ['केंद्रक', 'माइटोकॉन्ड्रिया', 'राइबोसोम', 'साइटोप्लाज्म'], 1), ('माइटोकॉन्ड्रिया की खोज किसने की?', ['रिचर्ड ऑल्टमैन', 'रॉबर्ट ब्राउन', 'रॉबर्ट हुक', 'सिंगर'], 0), ('माइटोकॉन्ड्रिया में मुख्य प्रक्रिया कौन-सी होती है?', ['प्रकाश संश्लेषण', 'कोशिकीय श्वसन', 'पाचन', 'विसरण'], 1), ('ATP का निर्माण मुख्यतः कहाँ होता है?', ['केंद्रक', 'माइटोकॉन्ड्रिया', 'कोशिका भित्ति', 'साइटोप्लाज्म'], 1), ('ATP का पूरा नाम क्या है?', ['Adenosine Triphosphate', 'Adenosine Diphosphate', 'Ribonucleic Acid', 'Deoxyribonucleic Acid'], 0), ('ATP को क्या कहा जाता है?', ['आनुवंशिक पदार्थ', 'ऊर्जा मुद्रा', 'कोशिका भित्ति', 'प्रोटीन'], 1), ('माइटोकॉन्ड्रिया में कितनी झिल्लियाँ होती हैं?', ['एक', 'दो', 'तीन', 'चार'], 1), ('माइटोकॉन्ड्रिया की आंतरिक झिल्ली की तहों को क्या कहते हैं?', ['क्रोमैटिन', 'क्रिस्टी', 'न्यूक्लॉयड', 'राइबोसोम'], 1), ('माइटोकॉन्ड्रिया का मैट्रिक्स कहाँ होता है?', ['बाहरी झिल्ली के बाहर', 'आंतरिक झिल्ली के अंदर', 'केंद्रक के अंदर', 'कोशिका भित्ति के बाहर'], 1), ('क्या माइटोकॉन्ड्रिया में अपना DNA होता है?', ['हाँ', 'नहीं', 'केवल पौधों में', 'केवल जंतुओं में'], 0)]

API = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def api(method, data=None):
    data = data or {}
    body = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(API + method, data=body)
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))

def db():
    con = sqlite3.connect(DB_FILE)
    con.execute("""CREATE TABLE IF NOT EXISTS polls(
        poll_id TEXT PRIMARY KEY,
        qno INTEGER NOT NULL
    )""")
    con.execute("""CREATE TABLE IF NOT EXISTS answers(
        poll_id TEXT,
        user_id INTEGER,
        name TEXT,
        username TEXT,
        qno INTEGER,
        option_id INTEGER,
        correct INTEGER,
        PRIMARY KEY(poll_id, user_id)
    )""")
    con.commit()
    return con

def send_quiz(chat_id):
    con = db()
    sent = 0
    for i, (question, options, correct) in enumerate(QUESTIONS, 1):
        payload = {
            "chat_id": chat_id,
            "question": f"{i}/{len(QUESTIONS)}. {question}",
            "options": json.dumps([{"text": x} for x in options], ensure_ascii=False),
            "type": "quiz",
            "is_anonymous": "false",
            "correct_option_ids": json.dumps([correct]),
            "explanation": f"सही उत्तर: {options[correct]}",
            "shuffle_options": "false",
            "allows_revoting": "false"
        }
        result = api("sendPoll", payload)
        if result.get("ok"):
            poll_id = result["result"]["poll"]["id"]
            con.execute("INSERT OR REPLACE INTO polls(poll_id,qno) VALUES(?,?)",
                        (poll_id, i))
            con.commit()
            sent += 1
        time.sleep(0.15)
    con.close()
    api("sendMessage", {
        "chat_id": chat_id,
        "text": f"✅ Quiz शुरू हो गया! कुल {sent} questions.\n\nहर participant अपना answer चुन सकता है। बाद में /result से अपना score और /results से admin पूरी list देख सकता है।"
    })

def save_answer(update):
    pa = update.get("poll_answer")
    if not pa or not pa.get("user"):
        return
    poll_id = pa["poll_id"]
    option_ids = pa.get("option_ids", [])
    con = db()
    row = con.execute("SELECT qno FROM polls WHERE poll_id=?", (poll_id,)).fetchone()
    if not row or not option_ids:
        con.close()
        return
    qno = row[0]
    # Correctness is derived from the question key stored locally.
    correct_idx = QUESTIONS[qno-1][2]
    opt = option_ids[0]
    user = pa["user"]
    name = (user.get("first_name","") + " " + user.get("last_name","")).strip()
    username = user.get("username","")
    con.execute(
        """INSERT OR REPLACE INTO answers
        (poll_id,user_id,name,username,qno,option_id,correct)
        VALUES(?,?,?,?,?,?,?)""",
        (poll_id, user["id"], name, username, qno, opt, int(opt == correct_idx))
    )
    con.commit()
    con.close()

def user_result(user_id):
    con = db()
    row = con.execute(
        """SELECT COUNT(*), COALESCE(SUM(correct),0)
           FROM answers WHERE user_id=?""", (user_id,)
    ).fetchone()
    con.close()
    answered, correct = row
    total = len(QUESTIONS)
    percent = round(correct * 100 / total, 1) if total else 0
    return answered, correct, total, percent

def all_results():
    con = db()
    rows = con.execute(
        """SELECT user_id,name,username,COUNT(*) AS answered,
                  SUM(correct) AS correct
           FROM answers GROUP BY user_id
           ORDER BY correct DESC, answered DESC, name"""
    ).fetchall()
    con.close()
    return rows

def is_admin(chat_id, user_id):
    try:
        r = api("getChatMember", {"chat_id": chat_id, "user_id": user_id})
        return r.get("ok") and r["result"]["status"] in ("creator", "administrator")
    except Exception:
        return False

def handle_message(msg):
    text = (msg.get("text") or "").strip()
    chat = msg.get("chat", {})
    chat_id = chat.get("id")
    user = msg.get("from", {})
    user_id = user.get("id")

    if text.startswith("/start"):
        api("sendMessage", {
            "chat_id": chat_id,
            "text": "Cell Biology Quiz Bot तैयार है. Admin /quiz से 49 questions भेजें।"
        })
    elif text.startswith("/quiz"):
        if is_admin(chat_id, user_id):
            send_quiz(chat_id)
        else:
            api("sendMessage", {"chat_id": chat_id, "text": "यह command केवल group admin चला सकता है।"})
    elif text.startswith("/result"):
        answered, correct, total, percent = user_result(user_id)
        api("sendMessage", {
            "chat_id": chat_id,
            "text": f"📊 आपका Result\nAnswered: {answered}/{total}\nCorrect: {correct}\nScore: {percent}%"
        })
    elif text.startswith("/results"):
        if not is_admin(chat_id, user_id):
            api("sendMessage", {"chat_id": chat_id, "text": "यह command केवल group admin के लिए है।"})
            return
        rows = all_results()
        if not rows:
            api("sendMessage", {"chat_id": chat_id, "text": "अभी कोई result नहीं आया।"})
            return
        lines = ["📊 All Participants Results", ""]
        for n, (uid, name, username, answered, correct) in enumerate(rows, 1):
            pct = round(correct * 100 / len(QUESTIONS), 1)
            tag = f"@{username}" if username else name
            lines.append(f"{n}. {tag} — {correct}/{len(QUESTIONS)} ({pct}%) — answered {answered}")
        api("sendMessage", {"chat_id": chat_id, "text": "\n".join(lines)})

def main():
    if not BOT_TOKEN:
        raise SystemExit("Render Environment में BOT_TOKEN सेट करें।")
    db()
    offset = None
    print("Bot running...")
    while True:
        try:
            params = {"timeout": 50, "allowed_updates": json.dumps(["message","poll_answer"])}
            if offset is not None:
                params["offset"] = offset
            r = api("getUpdates", params)
            if not r.get("ok"):
                time.sleep(2)
                continue
            for update in r.get("result", []):
                offset = update["update_id"] + 1
                if "poll_answer" in update:
                    save_answer(update)
                elif "message" in update:
                    handle_message(update["message"])
        except Exception as e:
            print("Error:", e)
            time.sleep(3)

if __name__ == "__main__":
    main()
