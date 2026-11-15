"""Build the 'Kanji Top 100' Anki deck: 80 kanji, typed-meaning cards with fuzzy grading.

Run:  python build_deck.py   ->  kanji_top100.apkg
Model/deck IDs and note GUIDs are fixed, so re-running and re-importing updates the
same cards instead of duplicating them (needed later when we add a Reading card).
"""
import genanki

# kanji | display meaning | accepted keywords | readings | anchor word | anchor reading | anchor meaning
BATCHES = [
    ("Batch 1 - Basics", """
大|big|big,large,great,huge|On: ダイ・タイ · Kun: おお(きい)|大学|だいがく|university
本|book, main, origin|book,origin,main,root,true,counter,real,base,japan|On: ホン · Kun: もと|日本|にほん|Japan
五|five|five,5|On: ゴ · Kun: いつ(つ)|五時|ごじ|5 o'clock
八|eight|eight,8|On: ハチ · Kun: やっ(つ)|八時|はちじ|8 o'clock
六|six|six,6|On: ロク · Kun: むっ(つ)|六時|ろくじ|6 o'clock
子|child|child,kid,son,children|On: シ · Kun: こ|子ども|こども|child
金|money, gold|money,gold,metal,friday|On: キン · Kun: かね|お金|おかね|money
入|enter|enter,in,put in,insert,go in,come in,input,entry|On: ニュウ · Kun: はい(る)・い(れる)|入る|はいる|to enter
力|power|power,strength,force,ability,energy,strong|On: リョク・リキ · Kun: ちから|体力|たいりょく|stamina
来|come|come,next,coming,since|On: ライ · Kun: く(る)|来ました|きました|came
"""),
    ("Batch 2 - Time and place", """
時|time, hour|time,hour,when,clock|On: ジ · Kun: とき|時間|じかん|time, hours
分|minute, part|minute,part,divide,understand,portion,share,split,separate|On: フン・ブン · Kun: わ(かる)|何分|なんぷん|how many minutes
前|before, front|before,front,ago,previous,prior|On: ゼン · Kun: まえ|午前|ごぜん|a.m.
後|after, behind|after,behind,later,back,rear|On: ゴ・コウ · Kun: あと・うし(ろ)|午後|ごご|p.m.
間|interval, between|interval,between,space,gap,time,room,among,while|On: カン · Kun: あいだ・ま|一週間|いっしゅうかん|one week
長|long, chief|long,chief,head,leader,boss,length|On: チョウ · Kun: なが(い)|社長|しゃちょう|company president
出|exit, go out|exit,go out,leave,out,come out,appear,emerge|On: シュツ · Kun: で(る)・だ(す)|出口|でぐち|exit
外|outside|outside,out,external,foreign,other,except,exterior|On: ガイ · Kun: そと|外国|がいこく|foreign country
内|inside|inside,within,internal,interior,in,home|On: ナイ · Kun: うち|国内|こくない|domestic
東|east|east|On: トウ · Kun: ひがし|東京|とうきょう|Tokyo
"""),
    ("Batch 3 - Everyday verbs", """
会|meet, association|meet,meeting,association,society,party,club|On: カイ · Kun: あ(う)|会社|かいしゃ|company
見|see|see,look,watch,view,saw,seen|On: ケン · Kun: み(る)|見る|みる|to see
思|think|think,thought,feel,believe|On: シ · Kun: おも(う)|思います|おもいます|I think
開|open|open,hold,develop,start|On: カイ · Kun: あ(ける)・ひら(く)|開ける|あける|to open
問|question|question,ask,problem,inquire,issue|On: モン · Kun: と(う)|問題|もんだい|problem
決|decide|decide,decision,determine,settle|On: ケツ · Kun: き(める)|決める|きめる|to decide
動|move|move,motion,movement,moving|On: ドウ · Kun: うご(く)|動く|うごく|to move
通|pass, commute|pass,commute,traffic,through,way,street,via,road,go through|On: ツウ · Kun: とお(る)・かよ(う)|通う|かよう|to commute
回|times, turn|time,turn,round,revolve,rotate,return,episode|On: カイ · Kun: まわ(る)|一回|いっかい|once
選|choose|choose,elect,select,choice,pick|On: セン · Kun: えら(ぶ)|選ぶ|えらぶ|to choose
"""),
    ("Batch 4 - Places and work", """
店|shop|shop,store|On: テン · Kun: みせ|お店|おみせ|shop
駅|station|station|On: エキ|駅|えき|station
場|place|place,location,spot,field,scene,site|On: ジョウ · Kun: ば|場所|ばしょ|place
市|city, market|city,market,town|On: シ · Kun: いち|市役所|しやくしょ|city hall
地|ground, land|ground,earth,land,place,soil,area,region|On: チ・ジ|地図|ちず|map
部|section, part|section,part,department,club,division,portion,unit|On: ブ|全部|ぜんぶ|all
員|member|member,staff,employee,personnel,worker|On: イン|店員|てんいん|shop staff
者|person (-er)|person,someone,one who,people,er|On: シャ · Kun: もの|医者|いしゃ|doctor
業|business, industry|business,industry,work,profession,occupation,karma|On: ギョウ|授業|じゅぎょう|class, lesson
高|high, expensive|high,tall,expensive|On: コウ · Kun: たか(い)|高い|たかい|tall, expensive
"""),
    ("Batch 5 - High-use abstract", """
同|same|same,identical,equal,similar|On: ドウ · Kun: おな(じ)|同じ|おなじ|same
自|self|self,oneself,own,myself|On: ジ・シ · Kun: みずか(ら)|自分|じぶん|oneself
事|thing, matter|thing,matter,affair,fact,event,incident|On: ジ · Kun: こと|仕事|しごと|work, job
方|direction, way|direction,way,person,side,method|On: ホウ · Kun: かた|やり方|やりかた|way of doing
新|new|new,fresh|On: シン · Kun: あたら(しい)|新しい|あたらしい|new
全|whole, all|whole,all,entire,complete,total,full|On: ゼン · Kun: まった(く)|全然|ぜんぜん|not at all
最|most|most,utmost,extreme,best|On: サイ · Kun: もっと(も)|最初|さいしょ|first
当|hit, right, this|hit,this,appropriate,right,correct,current,win,suitable|On: トウ · Kun: あ(たる)|本当|ほんとう|true, really
実|real, fruit|real,truth,true,fruit,actual,reality,seed,result|On: ジツ · Kun: み|実は|じつは|actually
明|bright|bright,light,clear,obvious,tomorrow,dawn|On: メイ · Kun: あか(るい)|明るい|あかるい|bright
"""),
    ("Batch 6 - Study and ideas", """
意|mind, meaning|mind,meaning,intention,idea,thought,will,heart|On: イ|意味|いみ|meaning
理|reason, logic|reason,logic,principle,truth,science,theory|On: リ|料理|りょうり|cooking
体|body|body,shape,form,style|On: タイ · Kun: からだ|体|からだ|body
化|change, -ization|change,transform,ization,convert,chemi,disguise|On: カ・ケ · Kun: ば(ける)|文化|ぶんか|culture
主|main, master|main,master,lord,owner,chief,principal,husband|On: シュ · Kun: ぬし・おも|主人|しゅじん|husband, master
題|topic, title|topic,title,subject,theme,problem|On: ダイ|宿題|しゅくだい|homework
代|generation, fee|generation,fee,charge,replace,substitute,era,period,age,price|On: ダイ・タイ · Kun: か(わる)|時代|じだい|era
約|approx., promise|approx,about,promise,around,agreement,roughly,contract|On: ヤク|約束|やくそく|promise
定|fix, decide|fix,decide,determine,set,settle,establish,constant,regular|On: テイ・ジョウ · Kun: さだ(める)|予定|よてい|plan
表|surface, express|surface,express,table,chart,front,show,outside,list|On: ヒョウ · Kun: おもて・あらわ(す)|発表|はっぴょう|presentation
"""),
    ("Batch 7 - Useful mid-tier", """
現|present, appear|present,appear,actual,current,real,existing,now|On: ゲン · Kun: あらわ(れる)|現在|げんざい|now, currently
調|investigate, tune|investigate,tune,check,research,tone,examine,look up,condition,adjust|On: チョウ · Kun: しら(べる)|調べる|しらべる|to look up
関|relation|relation,connect,barrier,gate,checkpoint,concern,involve|On: カン · Kun: せき|関係|かんけい|relationship
合|fit, join|fit,join,match,combine,suit,together,unite|On: ゴウ・ガッ · Kun: あ(う)|試合|しあい|match, game
円|yen, circle|yen,circle,round|On: エン · Kun: まる(い)|百円|ひゃくえん|100 yen
京|capital|capital,kyoto,tokyo|On: キョウ・ケイ|京都|きょうと|Kyoto
相|mutual, minister|mutual,together,minister,each other,phase,aspect,appearance,partner|On: ソウ・ショウ · Kun: あい|相手|あいて|partner, opponent
法|law, method|law,method,rule,way,legal|On: ホウ|方法|ほうほう|method
首|neck, head|neck,head,chief,prime,leader|On: シュ · Kun: くび|首|くび|neck
連|connect, take along|connect,link,join,group,companion,chain,take along,bring|On: レン · Kun: つ(れる)|連絡|れんらく|contact
"""),
    ("Batch 8 - News cluster", """
政|politics|politic,government,govern,administration|On: セイ・ショウ|政治|せいじ|politics
議|discussion|discuss,deliberat,debate,consult,parliament,assembly,proposal|On: ギ|会議|かいぎ|meeting
民|people, nation|people,nation,citizen,folk,public|On: ミン · Kun: たみ|国民|こくみん|citizens
党|political party|party,faction|On: トウ|政党|せいとう|political party
発|depart, emit|depart,emit,discharge,shoot,start,launch,issue|On: ハツ・ホツ|出発|しゅっぱつ|departure
対|versus, opposite|versus,vs,opposite,against,toward,pair,oppose,respond,compare|On: タイ・ツイ|反対|はんたい|opposition
戦|war, battle|war,battle,fight,combat,match|On: セン · Kun: たたか(う)|戦争|せんそう|war
経|pass through, economy|pass,econom,through,sutra,manage,longitude,via,experience|On: ケイ・キョウ · Kun: へ(る)|経済|けいざい|economy
氏|Mr., family name|mr,mrs,ms,family,clan,surname,name|On: シ · Kun: うじ|氏名|しめい|full name
米|rice, America|rice,america,usa,us,meter,metre|On: ベイ・マイ · Kun: こめ|お米|おこめ|rice
"""),
]

FIELDS = ["Kanji", "Meaning", "Accepted", "Readings", "AnchorWord", "AnchorReading", "AnchorMeaning"]

CSS = """
.card { font-family: "Noto Sans JP", "Yu Gothic", "Hiragino Sans", sans-serif; text-align: center;
        font-size: 18px; color: #222; background: #fafaf8; padding: 16px; }
.nightMode.card, .night_mode .card { color: #eee; background: #1e1e1e; }
.kanji { font-size: 110px; line-height: 1.15; margin: 12px 0 18px; }
#ans { font-size: 20px; padding: 8px 12px; width: 80%; max-width: 360px; border-radius: 8px;
       border: 1px solid #bbb; text-align: center; background: transparent; color: inherit; }
.hint { font-size: 13px; color: #888; margin-top: 8px; }
.verdict { display: inline-block; font-size: 18px; padding: 6px 14px; border-radius: 8px; margin: 4px 0 8px; }
.ok { background: #e3f2df; color: #27500a; }
.bad { background: #fcebeb; color: #791f1f; }
.nightMode .ok, .night_mode .ok { background: #27500a; color: #e3f2df; }
.nightMode .bad, .night_mode .bad { background: #791f1f; color: #fcebeb; }
.you { font-size: 15px; color: #888; margin-bottom: 4px; }
.meaning { font-size: 26px; margin: 10px 0; }
.anchor { font-size: 22px; margin: 8px 0; }
.anchor .r { color: #888; font-size: 17px; }
.readings { font-size: 15px; color: #888; margin-top: 10px; }
hr { border: none; border-top: 1px solid #ccc; margin: 14px 0; }
"""

# Front: typed answer is stashed in window + sessionStorage + localStorage so the back
# side can read it on desktop, AnkiDroid and AnkiMobile alike.
FRONT = """
<div class="kanji">{{Kanji}}</div>
<input id="ans" type="text" placeholder="meaning in English" autocomplete="off" autocapitalize="off" spellcheck="false">
<div class="hint">Type the meaning, then Enter / Show answer</div>
<script>
(function () {
  var el = document.getElementById('ans');
  function save(v) {
    window.__kanjiTyped = v;
    try { sessionStorage.setItem('kanjiTyped', v); } catch (e) {}
    try { localStorage.setItem('kanjiTyped', v); } catch (e) {}
  }
  save('');
  el.addEventListener('input', function () { save(el.value); });
  el.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault(); save(el.value);
      if (typeof pycmd !== 'undefined') { pycmd('ans'); }
      else if (typeof showAnswer === 'function') { showAnswer(); }
    }
  });
  setTimeout(function () { el.focus(); }, 60);
})();
</script>
"""

BACK = """
<div class="kanji">{{Kanji}}</div>
<div class="you" id="you"></div>
<div id="verdict"></div>
<hr>
<div class="meaning">{{Meaning}}</div>
<div class="anchor">{{AnchorWord}} <span class="r">【{{AnchorReading}}】</span> {{AnchorMeaning}}</div>
<div class="readings">{{Readings}}</div>
<div id="acc" style="display:none">{{Accepted}}</div>
<script>
(function () {
  var typed = window.__kanjiTyped;
  if (!typed) { try { typed = sessionStorage.getItem('kanjiTyped'); } catch (e) {} }
  if (!typed) { try { typed = localStorage.getItem('kanjiTyped'); } catch (e) {} }
  typed = (typed || '').trim();
  var kw = document.getElementById('acc').textContent.toLowerCase().split(',')
             .map(function (s) { return s.trim(); }).filter(Boolean);
  function grade(inp) {
    var n = inp.toLowerCase().replace(/[^a-z0-9 ]/g, ' ').replace(/\\s+/g, ' ').trim();
    if (!n) return false;
    var t = n.split(' ');
    return kw.some(function (w) {
      if (w.indexOf(' ') >= 0) return n.indexOf(w) >= 0;
      return t.some(function (x) {
        return x === w || (w.length >= 4 && x.indexOf(w) === 0) || (x.length >= 4 && w.indexOf(x) === 0);
      });
    });
  }
  var v = document.getElementById('verdict');
  var you = document.getElementById('you');
  if (!typed) {
    you.textContent = 'You typed nothing';
    v.innerHTML = '<span class="verdict bad">No answer → press Again</span>';
  } else {
    var ok = grade(typed);
    you.textContent = 'You typed: ' + typed;
    v.innerHTML = ok ? '<span class="verdict ok">Correct → Good</span>'
                     : '<span class="verdict bad">Not quite → Again (unless it\\'s a real synonym)</span>';
  }
})();
</script>
"""

MODEL = genanki.Model(
    1738201601,
    "Kanji Top100 (typed meaning)",
    fields=[{"name": f} for f in FIELDS],
    templates=[{"name": "Meaning", "qfmt": FRONT, "afmt": BACK}],
    css=CSS,
)

PARENT = "Kanji Top 100"


def build(out="kanji_top100.apkg"):
    decks, total = [], 0
    for i, (name, block) in enumerate(BATCHES):
        deck = genanki.Deck(1738201700 + i, f"{PARENT}::{name}")
        for line in block.strip().splitlines():
            parts = line.split("|")
            assert len(parts) == 7, line
            note = genanki.Note(model=MODEL, fields=parts, tags=[f"batch{i + 1}", "top100"],
                                guid=genanki.guid_for(parts[0], "kanji-top100"))
            deck.add_note(note)
            total += 1
        decks.append(deck)
    genanki.Package(decks).write_to_file(out)
    return total


if __name__ == "__main__":
    print(build(), "notes written")
