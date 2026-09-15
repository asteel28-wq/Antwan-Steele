---
title: Dynamic Kickoff Rule and Injury Rates
---

[Antwan's Portfolio](../../)

## Dynamic Kickoff Rule and Injury Rates

### Problem Introduction and Importance

Player safety has always stood out to me as one of the biggest issues in football, and the kickoff is probably the play I think about most when it comes to injury risk — the closing speeds and full-field collisions are just different from anything else in the game. In 2024, the NFL rolled out a new "dynamic kickoff" format meant to cut down on those high-speed collisions without getting rid of kickoffs entirely. I wanted to actually dig into whether that change did what it was supposed to do, instead of just taking the league's word for it.

### Research Questions

1. Has the rate of concussions and other high-velocity-collision injuries on kickoffs dropped since the NFL introduced the dynamic kickoff format (2024 rule change), compared to the prior three seasons of traditional kickoffs?
2. Among kickoff-return injuries, has the severity (games missed) changed since the rule switch, even if the total number of injuries hasn't moved much?

### Key Variables

- Whether an injury happened on a kickoff play
- Injury type/body part (concussion vs. lower-body, etc.)
- Injury severity (games missed)
- Kickoff format era (traditional vs. dynamic)
- Play type (return vs. touchback)

### How I'm Defining Each Variable

Honestly, this part took me longer to think through than I expected. Injury occurrence, to me, means a player got hurt on a kickoff play and it actually showed up on a weekly injury report. Kickoff format era is just which rule was in effect that season — I'm splitting it as pre-2024 (traditional) vs. 2024 onward (dynamic). Injury severity I'm defining as how much game time an injury actually cost someone, based on their official injury report status.

### How I'm Measuring Each Variable

I'm planning to pull injury type, designation, and weekly status from `load_injuries()` in the nflreadpy package. For the era split, I'll just build that column myself based on season year. The trickier part is play-level detail — injury reports don't say "this happened on a kickoff," so I'll need to separately pull kickoff plays from `load_pbp()` and connect the two by team and week. I'm also planning to check `load_participation()` and `load_snap_counts()` to help confirm someone was actually on the field for special teams that week.

### The Data I Ideally Need

When I was reading through what's actually available, I realized weekly injury reports (2021–2026, so I get both formats) joined with kickoff plays from play-by-play data is really the core of what I need. The part I'm still working through is that nflverse doesn't have anything that measures collision speed directly — there's no "velocity" stat sitting in these tables. So I think I'm going to have to use a proxy, like return yardage or whether a play was a full return vs. a touchback, as a stand-in for high-speed open-field contact.

### Where I'm Looking to Access This Data

I believe everything I need is available through the `nflreadpy` Python package, which pulls from the nflverse-data GitHub repo (it's CC-BY 4.0 licensed, so I'm fine to use it for a school project). Specifically I'll be using `load_pbp()`, `load_injuries()`, `load_participation()`, and `load_snap_counts()`.

### Two Visualizations I Might Make

1. A bar chart showing kickoff-related injuries by season, with a line marking where the 2024 rule change happened, so it's easy to see before vs. after.
2. A stacked bar chart comparing injury types (concussion vs. everything else) before and after the rule change.

### Questions I Still Have

- I'm not totally sure yet whether `load_injuries` gives any indication of what play caused an injury, or if it's purely a weekly status report. If it's the latter, I'll have to lean more on timing and participation data to make the connection, which feels a little shaky.
- The dynamic kickoff has only been around for about a season and a half so far — I keep going back and forth on whether that's really enough data to draw a solid conclusion from, or if I should frame this more as an early look rather than a final answer.
- I'm still not 100% sure a yardage/play-type proxy is a fair way to represent "high-velocity collision." It might make more sense to just reframe the question around something more directly measurable, like open-field kickoff-return injuries specifically.

### A Note on AI Use

I used Claude to help me think through my research design, figure out which nflverse datasets actually fit what I'm trying to measure, and organize this page.
