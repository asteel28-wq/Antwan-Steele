New Kickoff Rule and Injury Rates

September 2026

The Impact of the NFL's Dynamic Kickoff Rule on High-Velocity Collision and Injury Rates

Working independently

Introduction

Player safety is one of the issues in football that is talked about a lot, and the kickoffs have always stood out as one of the most dangerous plays in the sport on all levels. Players sprint 40+ yards downfield before making contact, and for decades that produced some of the highest closing speeds and most violent collisions in the game. When I started looking into it for this project, I found that injury data consistently ranks kickoffs among the most dangerous plays per snap in the NFL, which is part of why the league has spent years tweaking the rules instead of getting rid of the play entirely.

In 2024, the NFL rolled out a dynamic kickoff format that changed where players line up and how much distance they cover before contact, specifically to try to cut down on high-speed, full-field collisions while still keeping the kickoff in the game. What I want to find out with this project is whether that change actually shows up in the injury numbers, or if the format shift hasn't really moved the needle the way the league hoped. To me, this connects to a bigger question I care about: how much do sports policy changes actually improve player safety versus just changing what a play looks like on paper.

Dataset and Problem Framing

For this project I'm using data from nflverse, an open-source NFL data project distributed under a CC-BY 4.0 license through the nflreadpy Python package. I landed on three datasets that gives me the information I need:

Play-by-play data (load_pbp()), which goes back to 1999 and lets me isolate kickoff plays specifically and split them into the traditional era versus the dynamic era (2024–present).
Weekly injury reports (load_injuries()), available since 2009, which give me player-level injury designations, practice status, and game status by week.
Participation and snap-count data (load_participation() and load_snap_counts()), which I'm planning to use to help confirm which players were actually on the field for kickoff units in a given week, since injury reports aren't tagged to a specific play.

One thing I ran into while reading through the nflverse documentation is that there's no dataset that directly measures collision force or velocity, not even Next Gen Stats, which only covers passing, receiving, and rushing plays. That was a little frustrating at first, but it made me rethink how I'm defining "high-velocity collision" for this project. Instead of measuring it directly, I'm treating it as a proxy built from return yardage, play type (full return vs. touchback), and injury type — I'm assuming concussions are more likely tied to high-speed contact than lower-body injuries, though I know that's an assumption and not something the data confirms outright.

Methodology and Planned Analysis

Here's how I'm planning to approach the analysis:

Isolate kickoff plays in the play-by-play data and tag each one with an era flag — traditional (before 2024) or dynamic (2024 onward).
Join injury and participation data to the kickoff data by season, team, and week, so I can build a season-level summary of kickoff-related injury counts and types across both eras.
Compare the two eras with two visualizations: a season-by-season trend in kickoff injury counts with the 2024 rule change marked, and a breakdown of injury type (concussion vs. other) before and after the change.

I haven't run the actual analysis yet, so I'm leaving this section as my plan for now. Once I pull the data and build the charts, I'll come back and replace this with what I actually found.

Limitations, Ethics, and Reflection

Since I'm looking for a relationship, and possibly something causal, between a rule change and injury outcomes, there are a few limitations I think are important to be upfront about.

Injury reports are recorded weekly, not by individual play, so my analysis can really only show that a player who took kickoff snaps in a given week was also listed with an injury that week — it can't confirm the injury happened on that specific kickoff. I believe the participation and snap-count data will narrow that gap, but I don't think it closes it completely.

I also want to be honest that because no nflverse dataset measures collision velocity directly, I'm operationalizing "high-velocity collision" through indirect proxies rather than a real physical measurement. So any conclusions I draw about collision severity should be read as suggestive, not as something I directly measured.

Another thing I kept coming back to while working on this is that the dynamic kickoff format has only been around for about one full season so far. That's a small sample to draw strong conclusions from, so I'm treating this more as an early look than a final verdict on whether the rule change worked.

Last thing — I don't think this project creates any real risk for anyone. If I find little to no change in injury rates, that doesn't mean player safety isn't worth pursuing, it just might mean this particular rule change didn't go far enough. And if I do find a meaningful drop, I think that's a useful data point showing a non-destructive rule change can still meaningfully improve safety, which matters beyond just kickoffs.

References

nflverse. (2026). nflreadpy: Python interface to nflverse data [Software]. https://nflreadpy.nflverse.com/

NFL Football Operations. (2024). 2024 kickoff rule changes. https://operations.nfl.com/

Code Repo and Technical Report

https://github.com/asteel28-wq/twanolito

AI Transparency

I used Claude to help me think through my research design, figure out which nflverse datasets actually fit what I was trying to measure, and organize this project page. I believe it was a helpful tool for planning, especially since I was still learning what data was even available when I started this. But all the analysis, interpretation, and conclusions here are going to be mine once I actually get into the data.
