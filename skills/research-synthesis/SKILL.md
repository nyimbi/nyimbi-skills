---
name: research-synthesis
description: Synthesize user research into themes, insights, and recommendations. Use when you have interview transcripts, survey results, usability test notes, support tickets, NPS responses, or app store reviews to distill into patterns, user segments, and personas; when you need to extract themes and rank findings by frequency and impact; or when turning raw feedback into prioritized, roadmap-ready recommendations.
argument-hint: "<research data, transcripts, or survey results>"
---

# Research Synthesis

> **Routing:** For planning and conducting research (interview guides, survey design, usability tests), use **user-research**; for non-user-research questions (lead qualification, meeting mining, skill gaps, domain names), use **research-and-insight-analysis**.

> If you see `~~connector` placeholders, that source is optional — skip the step when it is not available.

Synthesize user research data into actionable insights. See the **user-research** skill for research methods, interview guides, and analysis frameworks.

## Inputs

Accept research from any combination of:
- Interview transcripts or notes
- Survey results (CSV, pasted data)
- Usability test recordings or notes
- Support tickets or feedback
- NPS/CSAT responses
- App store reviews
- Uploaded files: research documents, spreadsheets, recording summaries
- ~~knowledge base (if connected): search for research documents, interview notes, survey results
- ~~user feedback (if connected): pull support tickets, feature requests, bug reports
- ~~product analytics (if connected): pull usage data, funnel metrics, behavioral data
- ~~meeting transcription (if connected): pull interview recordings and meeting summaries

Ask the user:
- What type of research? (interviews, surveys, usability tests, analytics, support tickets, sales call notes)
- How many sources / participants?
- Is there a specific question or hypothesis being investigated?
- What decisions will this research inform?

If **~~user feedback** is connected: pull support tickets, feature requests, and NPS responses to supplement research data and cross-reference themes with real complaints and requests. If **~~product analytics** is connected: validate qualitative findings with usage data and behavioral metrics, and quantify the impact of identified pain points. If **~~knowledge base** is connected: search for prior research studies to compare against and publish the synthesis to the research repository.

## Workflow

### 1. Process the Research

For each source, extract:
- **Key observations**: what did users say, do, or experience?
- **Quotes**: verbatim quotes that illustrate important points
- **Behaviors**: what users actually did (vs what they said they do)
- **Pain points**: frustrations, workarounds, and unmet needs
- **Positive signals**: what works well, moments of delight
- **Context**: user segment, use case, experience level

### 2. Identify Themes and Patterns

Apply thematic analysis — see **Research Synthesis Methodology** below. Group observations into themes, count frequency across participants, and assess impact severity. Note contradictions and surprises.

Create a priority matrix:
- **High frequency + High impact**: top priority findings
- **Low frequency + High impact**: important for specific segments
- **High frequency + Low impact**: quality-of-life improvements
- **Low frequency + Low impact**: note but deprioritize

### 3. Generate the Synthesis

Produce the structured synthesis in the **Output** format below. Aim for 5-8 key findings, each with:
- **Finding statement**: one clear sentence describing the insight
- **Evidence**: supporting quotes, data points, or observations (with source attribution)
- **Frequency**: how many participants/sources support this finding
- **Impact**: how significantly it affects the user experience or business
- **Confidence level**: High (strong evidence), Medium (suggestive), Low (early signal)

Order findings by priority (frequency x impact).

### 4. Review and Extend

After generating the synthesis:
- Ask if any findings need more detail or different framing
- Offer to generate specific artifacts: persona documents, opportunity maps, research presentations
- Offer to create follow-up research plans for open questions
- Offer to draft product implications (how findings should influence the roadmap)

## Output

```markdown
## Research Synthesis: [Study Name]
**Method:** [Interviews / Survey / Usability Test] | **Participants:** [X]
**Date:** [Date range] | **Researcher:** [Name]

### Executive Summary
[3-4 sentence overview of key findings]

### Key Themes

#### Theme 1: [Name]
**Prevalence:** [X of Y participants]
**Summary:** [What this theme is about]
**Supporting Evidence:**
- "[Quote]" — P[X]
- "[Quote]" — P[X]
**Implication:** [What this means for the product]

#### Theme 2: [Name]
[Same format]

### Insights → Opportunities

| Insight | Opportunity | Impact | Effort |
|---------|-------------|--------|--------|
| [What we learned] | [What we could do] | High/Med/Low | High/Med/Low |

### User Segments Identified
| Segment | Characteristics | Needs | Size |
|---------|----------------|-------|------|
| [Name] | [Description] | [Key needs] | [Rough %] |

### Recommendations
1. **[High priority]** — [Why, based on which findings]
2. **[Medium priority]** — [Why]
3. **[Lower priority]** — [Why]

### Questions for Further Research
- [What we still don't know]

### Methodology Notes
[How the research was conducted, any limitations or biases to note]
```

## Research Synthesis Methodology

### Thematic Analysis
The core method for synthesizing qualitative research:

1. **Familiarization**: read through all the data before coding anything.
2. **Initial coding**: tag each observation, quote, or data point with descriptive codes. Be generous — it is easier to merge than to split later.
3. **Theme development**: group related codes into candidate themes. A theme captures something important about the data in relation to the research question.
4. **Theme review**: check themes against the data. Does each theme have sufficient evidence? Are themes distinct? Do they tell a coherent story?
5. **Theme refinement**: define and name each theme clearly. Write a 1-2 sentence description of what each theme captures.
6. **Report**: write up the themes as findings with supporting evidence.

### Affinity Mapping
A collaborative method for grouping observations:

1. **Capture observations**: write each distinct observation, quote, or data point as a separate note
2. **Cluster**: group related notes by similarity. Do not pre-define categories — let them emerge from the data.
3. **Label clusters**: give each cluster a descriptive name that captures the common thread
4. **Organize clusters**: arrange clusters into higher-level groups if patterns emerge
5. **Identify themes**: the clusters and their relationships reveal the key themes

Tips: one observation per note; move notes between clusters freely (the first grouping is rarely the best); split clusters that get too large; outliers are interesting — do not force every observation into a cluster; the grouping process builds shared understanding.

### Triangulation
Strengthen findings by combining multiple data sources:
- **Methodological**: same question, different methods (interviews + survey + analytics)
- **Source**: same method, different participants or segments
- **Temporal**: same observation at different points in time

A finding supported by multiple sources and methods is much stronger than one supported by a single source. When sources disagree, that is interesting — it may reveal different user segments or contexts.

## Interview Note Analysis

For each interview, identify:

**Observations**: what did the participant describe doing, experiencing, or feeling?
- Distinguish behaviors (what they do) from attitudes (what they think/feel)
- Note context: when, where, with whom, how often
- Flag workarounds — unmet needs in disguise

**Direct quotes**: verbatim statements that powerfully illustrate a point.
- Good quotes are specific and vivid, not generic
- Attribute to participant type, not name: "Enterprise admin, 200-person team" not "Sarah"
- A quote is evidence, not a finding. The finding is your interpretation of what the quote means.

**Behaviors vs stated preferences**: what people DO often differs from what they SAY they want.
- Behavioral observations are stronger evidence than stated preferences
- If a participant says "I want feature X" but their workflow shows they never use similar features, note the contradiction
- Look for revealed preferences through actual behavior

**Signals of intensity**: how much does this matter to the participant?
- Emotional language: frustration, excitement, resignation
- Frequency: how often they encounter the issue
- Workarounds: how much effort they expend working around the problem
- Impact: the consequence when things go wrong

**Cross-interview analysis** — after processing individual interviews:
- Look for patterns across participants; note frequency per theme
- Identify segments: do different types of users have different patterns?
- Surface contradictions — they often reveal meaningful segments
- Find surprises: what challenged your prior assumptions?

## Survey Data Interpretation

**Quantitative survey analysis:**
- **Response rate**: how representative is the sample? Low rates may introduce bias.
- **Distribution**: look at the shape of responses, not just averages. A bimodal distribution tells a different story than a normal one.
- **Segmentation**: break down responses by segment. Aggregates can mask important differences.
- **Statistical significance**: for small samples, be cautious about small differences.
- **Benchmarks**: compare to industry benchmarks or previous surveys.

**Open-ended response analysis:**
- Treat responses like mini interview notes; code each with themes
- Count frequency of themes; pull representative quotes per theme
- Look for themes in open-ended responses that structured questions missed — things you did not think to ask about

**Common mistakes:**
- Reporting averages without distributions (a 3.5 average could mean everyone lukewarm, or half love it and half hate it)
- Ignoring non-response bias
- Over-interpreting small differences (a 0.1 point NPS change is noise)
- Treating Likert scales as interval data
- Confusing correlation with causation in cross-tabulations

## Combining Qualitative and Quantitative Insights

- **Qualitative first**: interviews and observation reveal WHAT is happening and WHY; they generate hypotheses.
- **Quantitative validation**: surveys and analytics reveal HOW MUCH and HOW MANY; they test hypotheses at scale.
- **Qualitative deep-dive**: return to qualitative methods to understand unexpected quantitative findings.

Integration strategies:
- Use quantitative data to prioritize qualitative findings (a theme is more important if usage data shows it affects many users)
- Use qualitative data to explain quantitative anomalies (a retention drop is a number; interviews reveal the confusing onboarding change behind it)
- Present combined evidence: "47% of surveyed users report difficulty with X (survey), and interviews reveal this is because Y (qualitative finding)."

When sources disagree: this is signal, not error. Check for different populations, stated-vs-actual behavior gaps, and whether the question captured the intended construct. Report the disagreement honestly and investigate rather than choosing one source.

## Persona Development from Research

Personas should emerge from research data, not imagination:

1. **Identify behavioral patterns**: clusters of similar behaviors, goals, and contexts
2. **Define distinguishing variables**: what differentiates clusters (company size, technical skill, usage frequency, primary use case)
3. **Create persona profiles**: for each cluster — name and description; key behaviors and goals; pain points and needs; context (role, company, tools); representative quotes
4. **Validate with data**: can you size each segment using quantitative data?

Persona template:
```
[Persona Name] — [One-line description]

Who they are:
- Role, company type/size, experience level
- How they found/started using the product

What they are trying to accomplish:
- Primary goals and jobs to be done
- How they measure success

How they use the product:
- Frequency and depth of usage
- Key workflows and features used
- Tools they use alongside this product

Key pain points:
- Top 3 frustrations or unmet needs
- Workarounds they have developed

What they value:
- What matters most in a solution
- What would make them switch or churn

Representative quotes:
- 2-3 verbatim quotes that capture this persona's perspective
```

Common persona mistakes: demographic personas (behavior predicts product needs better than age/gender/location); too many (3-5 is the sweet spot); fictional (assumptions, not data); static (never updated); personas without implications (if it changes no decision, it is not useful).

## Opportunity Sizing

For each finding or opportunity area, estimate:
- **Addressable users**: how many users could benefit? (analytics, survey, or market data)
- **Frequency**: how often do affected users encounter it? (daily, weekly, monthly, one-time)
- **Severity**: blocker, significant friction, or minor annoyance?
- **Willingness to pay**: would fixing this drive upgrades, retention, or acquisition?

Opportunity scoring:
- **Impact**: (users affected) x (frequency) x (severity)
- **Evidence strength**: multiple sources > single source; behavioral data > stated preferences
- **Strategic alignment**: does it fit company strategy and product vision?
- **Feasibility**: technical feasibility, resources, time to impact

Presenting sizing: be transparent about assumptions and confidence; show the math ("Based on support ticket volume, ~2,000 users/month encounter this; interviews suggest 60% call it a significant blocker"); use ranges, not false precision; rank opportunities against each other.

## Tips

- Let the data speak. Do not force findings into a predetermined narrative.
- Include raw quotes — direct participant quotes make insights credible and memorable.
- Separate observations from interpretations: "5 of 8 users clicked the wrong button" is an observation; "the button placement is confusing" is an interpretation.
- Quantify where possible: "most users" is vague; "7 of 10 users" is specific.
- Be explicit about confidence levels. A finding from 2 interviews is a hypothesis, not a conclusion.
- Contradictions in the data are interesting, not inconvenient — they often reveal distinct user segments.
- Recommendations should be specific enough to act on. "Improve onboarding" is not actionable; "add a progress indicator to the setup flow" is.
- Resist synthesizing too many themes. 5-8 strong findings beat 20 weak ones.
