# A Recorded Ruling Is Only a Ruling If the File Quotes Them

An agent that writes to persistent state files, and reads them back as authority, will eventually record "the owner decided X" where X is its own summary of what it believed they wanted. Nothing downstream can tell the difference, and the entry gets more trustworthy with age rather than less.

## The Finding

Four instances in a single day, in one working system, all in files the agent had written itself.

**The voided rulings.** Two blocks headed with a date and "all eight decisions now ruled; the track is unblocked and everything below is authorized to build." The owner read them and voided them the same day, in his own words: *"they were my calls wearing his name."* The void was then recorded in one section of the file while the authorizing header was left standing in another, so the document contradicted itself for three days.

**The fabricated directive.** The agent told the owner that an instruction of his was dangling untracked. It was not his instruction. The state file contained a line labelled "Sequence agreed", which was an earlier session's paraphrase, and separately a line labelled "PM's recommended order", which is where the operative phrase actually came from. A project-management review read the second as an owner ruling, called it a moratorium, and constructed an entire reconciliation crisis on top of it. The agent relayed that to the owner twice without checking. His reply was four words: **"What sequence? What are you talking about?"**

The check that would have caught it was one `grep`.

**The near miss.** A later review flagged a third entry as the same shape. That one cleared: its sub-items came from the owner's selections in a structured question, so they were genuine. But the file carried no quote, which is exactly what made a real ruling indistinguishable from an invented one.

**The relay.** The second instance reached the owner because the agent treated a sub-agent's report as evidence rather than as a claim. It verified sub-agent findings about *code* by reading the source. It did not verify a sub-agent's finding about *what a human said*.

## Why no existing gate catches it

Every fabrication guard in this system watches for the same thing: the model sourcing from training memory instead of from tools. This failure is the exact inverse. It sources **from a tool**, from inside the process, from a dispatch the agent made itself, against a file the agent wrote. It arrives carrying more institutional credibility than the model's own recollection, not less.

A citation-discipline rule requiring the response to cite a specific finding from the sub-agent's output does not help either. The fabricated-directive instance would have passed it cleanly. There was a citation. The cited text was real. The attribution on it was invented.

This is a category the truth-checks cannot see, because what is false is not the content of the claim but the **label on it**.

## The compounding property

State files are read by future sessions and by sub-agents, and both treat them as ground truth. So a paraphrase written once is re-read as a directive, quoted into a dispatch prompt, and handed back by an independent-looking agent with the added authority of a second source. The next reviewer then rebuilds the same wrong reading from the same lines, and each pass makes it look more corroborated.

Nothing in that loop introduces new information. It only launders the original guess.

## How to apply

- **Attach the words.** When writing "the owner decided X", quote them. If the decision came from a menu selection rather than prose, say so and quote the option text. If you are paraphrasing, label it a paraphrase. A file that cannot distinguish a quote from a summary cannot be an authority on either.
- **Before telling someone that something is their instruction, grep for their words.** Not for the topic, for the phrasing. One search separates an accurate report from a fabricated one, and the fabricated one is more embarrassing in exact proportion to how confidently it is delivered.
- **A sub-agent characterising what a human wants is a claim, not evidence.** Treat it exactly as you would treat its claim about code: verify against the source before relaying. Pass known corrections into the next dispatch prompt, or the next agent reconstructs the same misreading from the same lines.
- **Sweep for the shape, not the instance.** The failure is a labelling error, so it recurs anywhere authority is recorded: "approved", "signed off", "agreed", "per the spec". Each one is a place where a summary can quietly acquire a source.
