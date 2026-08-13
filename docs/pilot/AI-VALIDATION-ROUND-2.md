# DESys v0.1 AI Validation Round 2

Status: Completed
Final candidate: `09aaec62fc5183ed19f30d13b73f39301812bd8d`
Final wheel SHA-256: `f5cca8882c5f1818d5d881f3d4c1e1c1fc1e37fc940eb91f6bf70651d8f53cbe`

## Results

| Scenario | Result | Notes |
| --- | --- | --- |
| `AI-002` | Pass | Correct relationship direction, lifecycle/class separation, relative paths, and explicit governance gaps. |
| `AI-004` | Pass | Direct conflicts separated from inferred concerns; missing governance reported without authority inference. |
| `AI-005` | Pass | Minimal ADR scope, no unsupported relationships, zero warnings, and successful recovery to baseline. |
| `AI-007` | Pass | Generated-file edit refused; source authority and toolchain behavior explained; no file changed. |
| `AI-009` | Pass | Final clean-session regression reported all three evidence gaps, inferred no governance process, and labeled next steps as optional proposals requiring confirmation. |

## AI-009 Finding

The primary response stated that optional proposals must follow a documented
draft, review, and approval process. The repository defines lifecycle values but
does not define required transitions, approval authority, review order, or a
mandatory artifact type.

The `AGENTS.md` template now states this limit explicitly and requires any next
steps to be presented only as optional proposals requiring confirmation.

## Final Regression Result

The managed `AGENTS.md` block was recreated from the final candidate and
`AI-009` was repeated in a new agent session.

The agent:

- reports database, backup retention, and RPO/RTO as separate evidence gaps;
- invents no values or technologies;
- infers no lifecycle sequence, approval process, authority, review order, or
  required artifact type;
- labels any next step as an optional proposal requiring confirmation;
- cites repository-relative paths;
- creates or changes no file.

All mandatory Round 2 regression scenarios passed. No Round 1 finding recurred
in the final `AI-009` response.
