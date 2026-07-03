## Description: <br>
Query workout data from Hevy including workouts, routines, exercises, and history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect Hevy workout history, routines, exercise templates, exercise progress, and related account data. It can also help prepare or run supported routine and exercise creation commands when the user explicitly requests account changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires HEVY_API_KEY and can access private Hevy workout and routine data. <br>
Mitigation: Install only when the agent should access the user's Hevy account, keep the API key scoped to that purpose, and remove or rotate the key when access is no longer needed. <br>
Risk: The skill includes account-changing commands for creating or updating routines, folders, workouts, and custom exercises. <br>
Mitigation: Review any create or update command and its JSON payload before execution, and treat the hevy binary as a read/write account tool rather than only a lookup helper. <br>
Risk: Using an unexpected hevy binary could send API credentials or workout data to an unintended implementation. <br>
Mitigation: Verify that the hevy binary on PATH comes from the expected package or source before use. <br>


## Reference(s): <br>
- [ClawHub Hevy Skill](https://clawhub.ai/mjrussell/hevy) <br>
- [Hevy](https://hevy.com) <br>
- [Hevy API Documentation](https://api.hevyapp.com/docs/) <br>
- [Hevy Developer Settings](https://hevy.com/settings?developer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text, JSON] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the hevy binary and HEVY_API_KEY for authenticated Hevy API access.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
