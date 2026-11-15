"""Build the 'PL Terms' Anki deck (programming-language terminology, HW1.1)."""
import html
import genanki

MODEL_ID = 1730000001
DECK_ID = 1730000002

# ---------- code rendering ----------
def code(s, hl=None):
    """Render a code line; wrap the substring `hl` in a highlight span."""
    if hl is None:
        return f'<pre class="code">{html.escape(s)}</pre>'
    i = s.index(hl)
    pre, mid, post = s[:i], s[i:i + len(hl)], s[i + len(hl):]
    return (f'<pre class="code">{html.escape(pre)}'
            f'<span class="hl">{html.escape(mid)}</span>{html.escape(post)}</pre>')

LINE = "{ int x = 5 + y; }"

# ---------- content ----------
# Definition -> term. (prompt, term, grammar hint, code html, plain meaning, trigger, trap)
DEFS = [
    ("declaration which also provides an initial value for the declared object",
     "initialization", "action / event", code("int x = 5;"),
     "Announce the box <b>and</b> fill it in one go.", "initial",
     "declaration = no value yet · assignment = changing it later"),
    ("storing or updating a value in an object, typically as a side effect of expression evaluation",
     "assignment", "action / event", code("x = 7;"),
     "Putting a new value into a box that already exists.", "storing / updating",
     "initialization = the <i>first</i> value, at birth"),
    ("procedure which also produces an output value so it may be called as an expression",
     "function", "thing", code("y = sqrt(9);", "sqrt(9)"),
     "A recipe that hands you back a result.", "output value",
     "procedure = does a task, returns nothing"),
    ("named, reusable block of code that may accept input values and performs a specific task",
     "procedure", "thing", code("printReport();"),
     "A named recipe that just does steps.", "performs a task",
     "function = also returns a value"),
    ("a word reserved by the language with a fixed meaning; it cannot be used as a name",
     "keyword", "thing", code(LINE, "int"),
     "Words the language owns: if, while, int, return.", "reserved",
     "identifier = a name <i>you</i> choose"),
    ("a named data object or storage location that may be used as an operand in expressions",
     "variable", "thing", code(LINE, "x"),
     "The named box.", "named · storage location",
     "value = what's inside · identifier = just the name"),
    ("a single data element; the result of evaluating an expression",
     "value", "thing", code(LINE, "5"),
     "The thing inside the box.", "single data element · result",
     "variable = the box itself"),
    ("determines the size, structure, and interpretation of a value stored in a variable or produced by an expression",
     "type", "rule / property", code(LINE, "int"),
     "What kind of thing fits in the box, and how big.", "size, structure, interpretation",
     "keyword = the reserved word (int is both)"),
    ("rules for how words and groups of words may be arranged to form meaningful statements",
     "syntax", "rule / property", code("if (x > 0) { ... }"),
     "Grammar: where the ; and { } must go.", "rules · arranged",
     "semantics = what it <i>means</i>"),
    ("the meaning of code: what a syntactically valid program actually does",
     "semantics", "rule / property", code("x = x + 1;"),
     "Meaning: \"add one to x\".", "meaning",
     "syntax = how it must be <i>written</i>"),
    ("the association between a name and the thing it refers to, or between an operator and its operands",
     "binding", "action / event", code(LINE, "x"),
     "The link: name ↔ thing.", "association",
     "assignment = putting a value in (not linking a name)"),
    ("the process of computing the value of an expression",
     "evaluation", "action / event", code("5 + y   →   8"),
     "Working out the answer.", "process of computing",
     "expression = the formula itself, not the computing"),
    ("introduces an identifier and specifies its meaning and properties in a program",
     "declaration", "action / event", code("int x;"),
     "Announce: \"there is a box called x, type int\".", "introduces",
     "initialization = declaration <i>plus</i> a first value"),
    ("characters that separate tokens but are otherwise meaningless, including spaces, tabs, and newlines",
     "whitespace", "thing", code("int␣x␣=␣5;"),
     "The gaps between words.", "spaces, tabs, newlines",
     "token = the pieces <i>between</i> the gaps"),
    ("an operator that explicitly converts a value to a specified type",
     "cast", "action / event", code("double d = (double)x;", "(double)"),
     "<b>You</b> convert it, on purpose.", "explicitly",
     "coercion = the language does it automatically"),
    ("automatic conversion of a value to match the type required by an operator; also called implicit conversion",
     "coercion", "action / event", code("5 + 2.0   →   5.0 + 2.0"),
     "The <b>language</b> converts it for you.", "automatic · implicit",
     "cast = you write the conversion yourself"),
    ("name assigned to a variable, function, or type",
     "identifier", "thing", code(LINE, "x"),
     "Just the name tag.", "name assigned",
     "variable = the box the name points to · keyword = reserved name"),
    ("sequence of operands and operators that describes a computation resulting in a value",
     "expression", "thing", code(LINE, "5 + y"),
     "A formula that produces a value.", "resulting in a value",
     "statement = a complete instruction (ends in ;)"),
    ("token or expression representing a value that is acted on by an operator",
     "operand", "thing", code(LINE, "y"),
     "The things the + works on.", "acted on",
     "operator = the + itself"),
    ("symbol that represents a basic computation and can be used to form expressions",
     "operator", "thing", code(LINE, "+"),
     "+  -  *  /  =", "basic computation",
     "operand = what it acts on"),
    ("sequence of tokens that describes a complete executable instruction in a program",
     "statement", "thing", code(LINE, "int x = 5 + y;"),
     "One full instruction: a whole line.", "complete instruction",
     "expression = just the part that makes a value"),
    ("smallest well-defined term or symbol in a programming language",
     "token", "thing", code(LINE, "="),
     "One piece of code: int · x · = · 5 · ;", "programming language",
     "symbol = smallest unit of a <i>written</i> language (the definition itself uses the word symbol)"),
    ("smallest unit of a written language",
     "symbol", "thing", code("a  b  c  7  #"),
     "One letter or sign.", "written language",
     "token = smallest unit of a <i>programming</i> language"),
    ("a group of statements treated as a single unit, usually wrapped in { }",
     "block", "thing", code(LINE, "{"),
     "The { } box around statements.", "group of statements",
     "statement = one instruction inside the block"),
    ("a value written directly in the source code, such as 5 or \"hi\"",
     "literal", "thing", code(LINE, "5"),
     "The value typed straight into the code.", "written directly",
     "value = any data, typed in or computed · token = any piece"),
]

# Contrast cards: (question, answer html, code html)
CONTRASTS = [
    ("function <span class='vs'>vs</span> procedure",
     "<b>function</b> returns a value<br><b>procedure</b> just does a task",
     code("y = sqrt(9);   printReport();")),
    ("declaration <span class='vs'>vs</span> initialization <span class='vs'>vs</span> assignment",
     "<b>declaration</b> announce · <b>initialization</b> announce + first value · <b>assignment</b> change later",
     code("int x;   int x = 5;   x = 7;")),
    ("cast <span class='vs'>vs</span> coercion",
     "<b>cast</b> explicit, you write it<br><b>coercion</b> implicit, automatic",
     code("(double)x      5 + 2.0")),
    ("variable <span class='vs'>vs</span> value",
     "<b>variable</b> the box<br><b>value</b> what's inside",
     code("x  ←  5")),
    ("identifier <span class='vs'>vs</span> variable",
     "<b>identifier</b> the name tag<br><b>variable</b> the box it labels",
     code(LINE, "x")),
    ("keyword <span class='vs'>vs</span> identifier",
     "<b>keyword</b> reserved by the language<br><b>identifier</b> a name you choose",
     code("int count;")),
    ("syntax <span class='vs'>vs</span> semantics",
     "<b>syntax</b> how it's written (grammar)<br><b>semantics</b> what it means",
     code("x = x + 1;")),
    ("expression <span class='vs'>vs</span> statement",
     "<b>expression</b> produces a value<br><b>statement</b> a complete instruction",
     code(LINE, "5 + y")),
    ("token <span class='vs'>vs</span> symbol",
     "<b>token</b> smallest unit of a <i>programming</i> language<br><b>symbol</b> smallest unit of a <i>written</i> language",
     code("int x = 5;")),
    ("literal <span class='vs'>vs</span> value",
     "<b>literal</b> a value typed into the code<br><b>value</b> any data, typed or computed",
     code("5  (literal)      5 + y  →  8  (value)")),
    ("operator <span class='vs'>vs</span> operand",
     "<b>operator</b> the action (+)<br><b>operand</b> what it acts on (5, y)",
     code(LINE, "+")),
    ("evaluation <span class='vs'>vs</span> expression",
     "<b>expression</b> the formula<br><b>evaluation</b> the act of computing it",
     code("5 + y   →   8")),
]

# Spot-it cards: (highlight, answer, note)
SPOTS = [
    ("int", "keyword", "It's also the <b>type</b>."),
    ("x", "identifier", "The name. The box it names is the <b>variable</b>."),
    ("5", "literal", "A <b>value</b> typed straight into the code."),
    ("+", "operator", "It acts on the operands 5 and y."),
    ("y", "operand", "It's also a <b>variable</b>."),
    ("5 + y", "expression", "Computing it is <b>evaluation</b>."),
    ("int x = 5 + y;", "statement", "Specifically an <b>initialization</b>."),
    ("{", "block", "The { } group."),
]

# ---------- design ----------
CSS = r"""
.card {
  --bg: #f6f4ef; --panel: #ffffff; --ink: #1d1d22; --muted: #6b6b76;
  --line: #e4e1d8; --accent: #3b5bdb; --hl: #ffe066; --hl-ink: #1d1d22;
  --code-bg: #1e2030; --code-ink: #c8d3f5; --good: #2b8a3e; --warn: #c2410c;
  font-family: "Segoe UI", system-ui, -apple-system, sans-serif;
  background: var(--bg); color: var(--ink);
  font-size: 18px; line-height: 1.5; text-align: left;
  padding: 24px 16px;
}
.card.nightMode, .nightMode .card {
  --bg: #15161c; --panel: #1f2029; --ink: #ececf1; --muted: #9a9aa8;
  --line: #2e2f3a; --accent: #8ea6ff; --hl: #ffd43b; --code-bg: #0d0e14;
  --good: #69db7c; --warn: #ffa94d;
}
.wrap { max-width: 560px; margin: 0 auto; }
.chip {
  display: inline-block; font-size: 12px; font-weight: 700; letter-spacing: .08em;
  text-transform: uppercase; padding: 3px 10px; border-radius: 999px;
  color: #fff; background: var(--accent);
}
.chip.contrast { background: #d6336c; }
.chip.spot { background: #0c8599; }
.prompt {
  background: var(--panel); border: 1px solid var(--line); border-radius: 14px;
  padding: 18px 20px; margin-top: 12px; font-size: 21px; font-weight: 500;
}
.ask { color: var(--muted); font-size: 14px; margin-top: 10px; }
.vs { color: #d6336c; font-weight: 800; font-size: .8em; padding: 0 4px; }
.hint { margin-top: 10px; font-size: 14px; color: var(--muted); }
.hint a { color: var(--accent); }
.code {
  background: var(--code-bg); color: var(--code-ink); border-radius: 10px;
  padding: 12px 16px; margin: 12px 0 0; font-size: 18px; white-space: pre-wrap;
  font-family: "Cascadia Code", Consolas, "SF Mono", monospace;
}
.hl {
  background: var(--hl); color: var(--hl-ink); border-radius: 4px;
  padding: 1px 3px; font-weight: 700; box-shadow: 0 0 0 2px var(--hl);
}
hr#answer { border: none; border-top: 2px dashed var(--line); margin: 22px 0; }
.term { font-size: 34px; font-weight: 800; color: var(--accent); letter-spacing: -.01em; }
.plain { margin-top: 4px; font-size: 18px; }
.row { display: flex; gap: 8px; align-items: baseline; margin-top: 12px; font-size: 15px; }
.tag { flex: none; font-size: 11px; font-weight: 800; letter-spacing: .08em;
  text-transform: uppercase; padding: 2px 8px; border-radius: 6px; }
.tag.key { background: color-mix(in srgb, var(--good) 18%, transparent); color: var(--good); }
.tag.trap { background: color-mix(in srgb, var(--warn) 18%, transparent); color: var(--warn); }
.answer-big { font-size: 20px; }
"""

FRONT = """
<div class="wrap">
  <span class="chip {{Kind}}">{{Label}}</span>
  <div class="prompt">{{Prompt}}</div>
  {{#FrontCode}}{{FrontCode}}{{/FrontCode}}
  <div class="ask">{{Ask}}</div>
  {{#Hint}}<div class="hint">{{hint:Hint}}</div>{{/Hint}}
</div>
"""

BACK = """
{{FrontSide}}
<div class="wrap">
  <hr id="answer">
  <div class="term">{{Answer}}</div>
  {{#Plain}}<div class="plain">{{Plain}}</div>{{/Plain}}
  {{#BackCode}}{{BackCode}}{{/BackCode}}
  {{#Trigger}}<div class="row"><span class="tag key">trigger</span><span>{{Trigger}}</span></div>{{/Trigger}}
  {{#Trap}}<div class="row"><span class="tag trap">don't mix up</span><span>{{Trap}}</span></div>{{/Trap}}
</div>
"""

FIELDS = ["Key", "Kind", "Label", "Prompt", "FrontCode", "Ask", "Hint",
          "Answer", "Plain", "BackCode", "Trigger", "Trap"]

model = genanki.Model(
    MODEL_ID, "PL Terms (styled)",
    fields=[{"name": f} for f in FIELDS],
    templates=[{"name": "Card", "qfmt": FRONT, "afmt": BACK}],
    css=CSS,
)

class Note(genanki.Note):
    @property
    def guid(self):
        return genanki.guid_for(self.fields[0])

deck = genanki.Deck(DECK_ID, "Programming Language Terms")

def add(tags, **kw):
    deck.add_note(Note(model=model, fields=[kw.get(f, "") for f in FIELDS], tags=tags))

for prompt, term, grammar, c, plain, trig, trap in DEFS:
    add(["definition"], Key=f"def:{term}", Kind="", Label="Definition", Prompt=prompt,
        Ask="Which term?", Hint=f"Grammar group: {grammar}", Answer=term, Plain=plain,
        BackCode=c, Trigger=trig, Trap=trap)

for q, a, c in CONTRASTS:
    add(["contrast"], Key=f"vs:{q}", Kind="contrast", Label="Don't mix up", Prompt=q,
        Ask="What's the one-line difference?", Answer="", Plain=f'<div class="answer-big">{a}</div>',
        BackCode=c)

for target, ans, note in SPOTS:
    add(["spot"], Key=f"spot:{target}", Kind="spot", Label="Spot it",
        Prompt="Name the highlighted part.", FrontCode=code(LINE, target),
        Ask="Pick the most specific term.", Answer=ans, Plain=note)

genanki.Package(deck).write_to_file("Programming_Language_Terms.apkg")
print(f"{len(deck.notes)} notes written")
