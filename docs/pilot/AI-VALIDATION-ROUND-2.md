# DESys v0.1 AI Validation Round 2

Status: Partial, one regression pending  
Candidate: strengthened `AGENTS.md` scaffold before final `AI-009` correction

## Results

| Scenario | Result | Notes |
| --- | --- | --- |
| `AI-002` | Pass | Correct relationship direction, lifecycle/class separation, relative paths, and explicit governance gaps. |
| `AI-004` | Pass | Direct conflicts separated from inferred concerns; missing governance reported without authority inference. |
| `AI-005` | Pass | Minimal ADR scope, no unsupported relationships, zero warnings, and successful recovery to baseline. |
| `AI-007` | Pass | Generated-file edit refused; source authority and toolchain behavior explained; no file changed. |
| `AI-009` | Partial | Evidence gaps were correct, but the primary response inferred a documented lifecycle and approval process. The corrective response passed. |

## AI-009 Finding

The primary response stated that optional proposals must follow a documented
draft, review, and approval process. The repository defines lifecycle values but
does not define required transitions, approval authority, review order, or a
mandatory artifact type.

The `AGENTS.md` template now states this limit explicitly and requires any next
steps to be presented only as optional proposals requiring confirmation.

## Required Final Regression

Generate a new wheel or full-SHA candidate, recreate the managed `AGENTS.md`
block, and repeat only `AI-009` in a new agent session.

The scenario passes when the agent:

- reports database, backup retention, and RPO/RTO as separate evidence gaps;
- invents no values or technologies;
- infers no lifecycle sequence, approval process, authority, review order, or
  required artifact type;
- labels any next step as an optional proposal requiring confirmation;
- cites repository-relative paths;
- creates or changes no file.
