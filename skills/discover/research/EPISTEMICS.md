# Epistemics

Every claim in a research file sits in exactly one tier. The tier sets its phrasing.

## Tiers

- **Verified.** A primary source states it explicitly: the regulation's text, the library's docs or source, the client's written answer. Phrase it plainly and cite the source next to it: "Invoices must carry a sequential number ([Directive 2006/112/EC, Art. 226](...))."
- **Inferred.** Several sources converge on it, or it follows from verified facts, but nothing states it outright. Make the chain explicit: "Given A and B, C seems likely." Cite A and B.
- **Guess.** A plausible hypothesis on thin evidence, where other explanations fit equally well. Say so: "One possibility is X, but we found no direct evidence." List competing guesses side by side.
- **Unknown.** You looked and could not find out. Name what you searched and with which terms. This is a valid, valuable outcome.

## Rules

- Confidence words ("is", "requires", "because", "the client decided") need a citation right next to them. Use hedges ("appears to", "likely", "suggests") for anything below Verified.
- A secondary source (blog, tutorial, Stack Overflow, an LLM's memory) never makes a claim Verified. Use it to find the primary source, then cite that.
- If the user's question embeds a hypothesis ("I assume FHIR covers this?"), treat it as one candidate, not the answer. Check it independently.
- When sources contradict, show both with citations. Don't pick the tidier story.
- A file with no **What we don't know** section is suspicious. Either the evidence was unusually complete or gaps are being hidden.
