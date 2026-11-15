# Module 1 glossary — master key

Built from the HW1.3 matching variants (2026-09-16). The pool repeats heavily:
find the trigger phrase, read off the term. Expect 2–4 unused decoys per variant.

| Trigger phrase in the definition | Term |
|---|---|
| initial value | initialization |
| storing or **updating** a value / side effect | assignment |
| introduces an identifier / specifies meaning and properties | declaration |
| allocates storage / supplies the body | definition |
| smallest well-defined term or symbol | token |
| pre-defined meaning, cannot be used as identifiers | keyword |
| a **name** you choose | identifier |
| enclosed in **braces** / compound statement | block |
| **explicitly** converts a value to a type | cast |
| **automatic** conversion / implicit conversion | coercion |
| declared in a function **definition**, receives input | parameter |
| value supplied as input **to a call** | argument |
| **meaning** of words and statements | semantics |
| **rules for arranging** words into statements | syntax |
| complete executable **instruction** | statement |
| operands and operators producing a **value** | expression |
| **symbol** representing a basic **computation** | operator |
| value **acted on by** an operator | operand |
| **named** data object / storage location | variable |
| size, structure, **interpretation** of a value | type |
| **the process of** computing a value | evaluation |
| single data element; the **result of** evaluating | value |
| the value as **written in the source** | literal |
| named reusable block of code, performs a task | procedure |
| procedure that **also** produces an output value | function |
| **association between** a name and the thing it refers to | binding |
| separates tokens but otherwise meaningless; spaces, tabs | whitespace |
| descriptive text **ignored by the compiler** | comment |
| which operator goes **first** | precedence |
| **same** precedence — which **direction** | associativity |

## Discriminators for the confusable pairs

| Confusion | One question that settles it |
|---|---|
| cast vs coercion | You typed it → cast. Compiler did it silently → coercion |
| parameter vs argument | **P**arameter is in the **P**rototype/definition. **A**rgument is **A**t the call |
| declaration vs definition | Announces the name → declaration. Creates it → definition |
| declaration vs initialization | Mentions an *initial value* → initialization |
| assignment vs initialization | At declaration → initialization. Later, at run time → assignment |
| expression vs statement | Produces a value → expression. Does something, ends in `;` → statement |
| syntax vs semantics | Form → syntax. Meaning → semantics |
| value vs evaluation | "the process of" → evaluation. "a single data element" → value |
| value vs literal | Written in source → literal. Result of evaluating → value |
| operator vs operand | The d**oer** → operat**or**. The **done-to** → operan**d** |
| variable vs type | The named box → variable. Rules about what fits → type |
| procedure vs function | Returns a value, callable inside an expression → function |
| precedence vs associativity | Different operators → precedence. Same precedence → associativity |

## The "X which also Y" pattern

When a definition names another term from the list and adds "which also", the answer is the
narrower term, and the base noun in the sentence still needs its own row. Two slots from one read.

- "**declaration** which **also** provides an initial value" -> initialization (and declaration is elsewhere)
- "**procedure** which **also** produces an output value" -> function (and procedure is elsewhere)
