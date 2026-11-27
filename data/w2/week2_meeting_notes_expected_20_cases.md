# Week 2 – Meeting Notes & Expected JSON (20 Test Cases)

> **Shared evaluation dataset** for 8 AI Engineering Fast-Track members. All meeting content is fictional.

## Evaluation contract

- Endpoint: `POST /analyze-meeting` with request `{"meeting_text": "..."}`.
- Expected response shape: `{"summary": str, "decisions": list[str], "actions": [{"owner": str|null, "action": str, "due_date": "YYYY-MM-DD"|null}]}`.
- `null` means the source does not state a sufficiently supported value; never invent owner or due date.
- One shared action with two named owners is represented as **two owner-specific entries** (TC15).
- `summary` and action/decision descriptions may be **semantically equivalent**, not necessarily byte-for-byte identical. Normalize whitespace and assess meaning; compare owners and ISO dates precisely.
- Dates without years are resolved using the explicitly supplied meeting date and surrounding text.
- For fairness, distribute **the same evaluation contract** to all 8 members. If this full document is shared ahead of testing, it is a **public development set**; use a separate hidden dataset for unbiased final evaluation.
- The extraction metric must be agreed upfront (e.g. fact/action-level precision, recall, F1); 17/20 fully passing cases is a different metric.

## Test cases

### TC01 – Sprint Planning

**Category:** Normal

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-23
Attendees: Phu, Hung, Minh

The team reviewed the sprint backlog and agreed to prioritize the login bug. Phu will fix the login authentication issue by November 25, 2026. Hung will review the pull request by November 26, 2026. Minh will prepare regression test cases by November 27, 2026.
```

**Expected JSON**

```json
{
  "summary": "The team prioritized the login bug and assigned remediation, review, and regression testing.",
  "decisions": [
    "Prioritize the login bug."
  ],
  "actions": [
    {
      "owner": "Phu",
      "action": "Fix the login authentication issue",
      "due_date": "2026-11-25"
    },
    {
      "owner": "Hung",
      "action": "Review the pull request",
      "due_date": "2026-11-26"
    },
    {
      "owner": "Minh",
      "action": "Prepare regression test cases",
      "due_date": "2026-11-27"
    }
  ]
}
```

### TC02 – Production Deployment

**Category:** Normal

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-24
Attendees: Hung, Lan, Phu

The team decided to deploy version 2.5 to production on November 27, 2026. Lan will prepare the deployment checklist by November 25. Hung will execute the deployment on November 27. Phu will verify application health after deployment on the same day.
```

**Expected JSON**

```json
{
  "summary": "The team scheduled the version 2.5 production deployment for November 27 and assigned deployment preparation and verification.",
  "decisions": [
    "Deploy version 2.5 to production on 2026-11-27."
  ],
  "actions": [
    {
      "owner": "Lan",
      "action": "Prepare the deployment checklist",
      "due_date": "2026-11-25"
    },
    {
      "owner": "Hung",
      "action": "Execute the production deployment",
      "due_date": "2026-11-27"
    },
    {
      "owner": "Phu",
      "action": "Verify application health after deployment",
      "due_date": "2026-11-27"
    }
  ]
}
```

### TC03 – Database Optimization

**Category:** Normal

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-25
Attendees: Minh, Phu, An

The team agreed to add an index to the orders table to improve query performance. Minh will create the database migration by November 27, 2026. Phu will benchmark the query performance by November 30, 2026. An will review the migration before deployment on November 28.
```

**Expected JSON**

```json
{
  "summary": "The team approved an orders-table index and assigned migration, performance benchmarking, and review.",
  "decisions": [
    "Add an index to the orders table to improve query performance."
  ],
  "actions": [
    {
      "owner": "Minh",
      "action": "Create the database migration",
      "due_date": "2026-11-27"
    },
    {
      "owner": "Phu",
      "action": "Benchmark query performance",
      "due_date": "2026-11-30"
    },
    {
      "owner": "An",
      "action": "Review the database migration",
      "due_date": "2026-11-28"
    }
  ]
}
```

### TC04 – Security Review

**Category:** Normal

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-26
Attendees: Phu, Hung, Lan

The security scan identified vulnerable Ruby dependencies. The team decided to upgrade the affected gems before the next release. Phu will update the vulnerable dependencies by November 30. Hung will run bundle-audit and verify the results by December 1. Lan will document the security changes by December 2.
```

**Expected JSON**

```json
{
  "summary": "The team identified vulnerable Ruby gems and decided to upgrade them before the next release.",
  "decisions": [
    "Upgrade the affected Ruby gems before the next release."
  ],
  "actions": [
    {
      "owner": "Phu",
      "action": "Update vulnerable dependencies",
      "due_date": "2026-11-30"
    },
    {
      "owner": "Hung",
      "action": "Run bundle-audit and verify the results",
      "due_date": "2026-12-01"
    },
    {
      "owner": "Lan",
      "action": "Document the security changes",
      "due_date": "2026-12-02"
    }
  ]
}
```

### TC05 – API Performance Improvement

**Category:** Normal

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-27
Attendees: Minh, An, Hung

The team reviewed API latency and agreed to implement Redis caching for frequently accessed endpoints. Minh will implement caching by December 2, 2026. An will add performance tests by December 3. Hung will review the changes by December 4.
```

**Expected JSON**

```json
{
  "summary": "The team chose Redis caching to reduce API latency and assigned implementation, testing, and review.",
  "decisions": [
    "Implement Redis caching for frequently accessed endpoints."
  ],
  "actions": [
    {
      "owner": "Minh",
      "action": "Implement Redis caching",
      "due_date": "2026-12-02"
    },
    {
      "owner": "An",
      "action": "Add performance tests",
      "due_date": "2026-12-03"
    },
    {
      "owner": "Hung",
      "action": "Review the caching changes",
      "due_date": "2026-12-04"
    }
  ]
}
```

### TC06 – Pull Request Review

**Category:** Missing information

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-23
Attendees: Phu, Hung

Hung will review the authentication pull request. Phu will address any feedback from the review. The team did not agree on deadlines for either task.
```

**Expected JSON**

```json
{
  "summary": "Hung will review the authentication pull request, and Phu will address review feedback; no deadlines were set.",
  "decisions": [],
  "actions": [
    {
      "owner": "Hung",
      "action": "Review the authentication pull request",
      "due_date": null
    },
    {
      "owner": "Phu",
      "action": "Address feedback from the pull request review",
      "due_date": null
    }
  ]
}
```

**Evaluation note:** No stated decision or deadlines. Both tasks are explicitly assigned.

### TC07 – Documentation Update

**Category:** Missing information

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-24
Attendees: Lan, Minh

The team agreed that the API documentation needs improvement. Someone from the backend team will update the endpoint descriptions by November 30, 2026. No specific owner was assigned.
```

**Expected JSON**

```json
{
  "summary": "The team agreed that API documentation should be improved and identified an endpoint-description update without an assigned owner.",
  "decisions": [
    "Improve the API documentation."
  ],
  "actions": [
    {
      "owner": null,
      "action": "Update the API endpoint descriptions",
      "due_date": "2026-11-30"
    }
  ]
}
```

**Evaluation note:** Unknown owner must be null, not guessed from attendees.

### TC08 – Infrastructure Monitoring

**Category:** Missing information

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-25
Attendees: An, Hung, Phu

The team reviewed server monitoring alerts. An will investigate the high CPU usage. Hung will check the database connection pool settings by November 27. No deadline was specified for An's investigation.
```

**Expected JSON**

```json
{
  "summary": "The team discussed server alerts and assigned a CPU investigation and a database connection pool review.",
  "decisions": [],
  "actions": [
    {
      "owner": "An",
      "action": "Investigate high CPU usage",
      "due_date": null
    },
    {
      "owner": "Hung",
      "action": "Check database connection pool settings",
      "due_date": "2026-11-27"
    }
  ]
}
```

### TC09 – Code Quality Discussion

**Category:** Missing information

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-26
Attendees: Phu, Minh, Lan

The team discussed improving code quality and reducing technical debt. Everyone agreed that refactoring is necessary, but no tasks were assigned and no implementation dates were established.
```

**Expected JSON**

```json
{
  "summary": "The team agreed that refactoring is necessary to improve code quality and reduce technical debt, but assigned no tasks.",
  "decisions": [
    "Refactoring is necessary to improve code quality and reduce technical debt."
  ],
  "actions": []
}
```

**Evaluation note:** Agreement is recorded as a decision; do not invent action assignments.

### TC10 – Rails Upgrade Proposal

**Category:** Ambiguous

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-23
Attendees: Phu, Hung, Minh

Phu suggested upgrading the application to Rails 8.1. Hung expressed concerns about backward compatibility. Minh said the team might consider upgrading next quarter. No final decision was made, and no implementation tasks were assigned.
```

**Expected JSON**

```json
{
  "summary": "The team discussed a possible Rails 8.1 upgrade and compatibility concerns but made no decision or assignments.",
  "decisions": [],
  "actions": []
}
```

**Evaluation note:** Proposal is not a decision.

### TC11 – Cloud Migration Discussion

**Category:** Ambiguous

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-24
Attendees: An, Lan, Hung

The team discussed possibly migrating background jobs to AWS Lambda. Lan suggested using AWS Step Functions for orchestration. Hung said more research would be helpful. The team has not decided whether to proceed with the migration.
```

**Expected JSON**

```json
{
  "summary": "The team considered Lambda and Step Functions for background jobs but did not approve a migration or assign research.",
  "decisions": [],
  "actions": []
}
```

**Evaluation note:** A suggestion that research would help is not an assigned action.

### TC12 – Feature Prioritization

**Category:** Ambiguous

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-25
Attendees: Minh, Phu, Hung

The team discussed adding dark mode to the application. Minh believes the feature could improve user experience. Phu suggested including it in the next sprint, while Hung recommended waiting for customer feedback. The decision was postponed until the next planning meeting.
```

**Expected JSON**

```json
{
  "summary": "The team discussed dark mode and deferred the prioritization decision until the next planning meeting.",
  "decisions": [],
  "actions": []
}
```

**Evaluation note:** Do not treat a postponed decision as approval; no owner was assigned.

### TC13 – Testing Strategy

**Category:** Ambiguous

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-26
Attendees: Phu, Lan, An

The team considered replacing some integration tests with unit tests to reduce execution time. Phu suggested creating a proof of concept. Lan agreed to investigate the feasibility by November 30, 2026. However, no decision was made about changing the overall testing strategy.
```

**Expected JSON**

```json
{
  "summary": "The team explored reducing integration tests and assigned Lan a feasibility investigation without approving a strategy change.",
  "decisions": [],
  "actions": [
    {
      "owner": "Lan",
      "action": "Investigate the feasibility of replacing some integration tests with unit tests",
      "due_date": "2026-11-30"
    }
  ]
}
```

**Evaluation note:** An explicitly accepted investigation is an action; Phu merely suggested a proof of concept.

### TC14 – Release Planning and Risk Review

**Category:** Complex

**Meeting Notes (input)**

```text
Meeting Date: 2026-11-30
Attendees: Phu, Hung, Minh, Lan

The team reviewed the upcoming release and identified two major risks: database migration failures and API compatibility issues. The team decided to postpone the release from December 3 to December 7, 2026. Phu will validate the database migrations by December 2. Hung will perform API compatibility testing by December 3. Minh will prepare a rollback plan by December 4. Lan will update the release documentation by December 5. The team also agreed that production deployment must not proceed until all critical tests pass.
```

**Expected JSON**

```json
{
  "summary": "The team identified migration and compatibility risks, postponed the release to December 7, and made critical tests a deployment prerequisite.",
  "decisions": [
    "Postpone the release to 2026-12-07, replacing the 2026-12-03 date.",
    "Do not deploy to production until all critical tests pass."
  ],
  "actions": [
    {
      "owner": "Phu",
      "action": "Validate the database migrations",
      "due_date": "2026-12-02"
    },
    {
      "owner": "Hung",
      "action": "Perform API compatibility testing",
      "due_date": "2026-12-03"
    },
    {
      "owner": "Minh",
      "action": "Prepare a rollback plan",
      "due_date": "2026-12-04"
    },
    {
      "owner": "Lan",
      "action": "Update the release documentation",
      "due_date": "2026-12-05"
    }
  ]
}
```

**Evaluation note:** Old release date is superseded, not a second valid deadline.

### TC15 – Multiple Owners and Shared Tasks

**Category:** Complex

**Meeting Notes (input)**

```text
Meeting Date: 2026-12-01
Attendees: Phu, Hung, Minh, An

The team agreed to improve the authentication module. Phu and Hung will work together to implement token refresh handling by December 4, 2026. Minh will create automated authentication tests by December 5. An will review security risks by December 6. Phu will also update the technical documentation by December 7. The team decided to require additional security validation before releasing authentication changes.
```

**Expected JSON**

```json
{
  "summary": "The team approved authentication improvements, including token refresh handling and a security validation requirement before release.",
  "decisions": [
    "Improve the authentication module.",
    "Require additional security validation before releasing authentication changes."
  ],
  "actions": [
    {
      "owner": "Phu",
      "action": "Implement token refresh handling",
      "due_date": "2026-12-04"
    },
    {
      "owner": "Hung",
      "action": "Implement token refresh handling",
      "due_date": "2026-12-04"
    },
    {
      "owner": "Minh",
      "action": "Create automated authentication tests",
      "due_date": "2026-12-05"
    },
    {
      "owner": "An",
      "action": "Review security risks",
      "due_date": "2026-12-06"
    },
    {
      "owner": "Phu",
      "action": "Update the technical documentation",
      "due_date": "2026-12-07"
    }
  ]
}
```

**Evaluation note:** Shared task is intentionally represented as two owner-specific actions using the agreed schema.

### TC16 – Conflicting Deadlines

**Category:** Complex

**Meeting Notes (input)**

```text
Meeting Date: 2026-12-02
Attendees: Lan, Phu, Hung

The team originally planned to complete the payment integration by December 4, 2026. During the meeting, Phu explained that additional testing was needed. After discussion, the team agreed to move the deadline to December 9, 2026. Phu will finish the integration by December 7. Hung will complete integration testing by December 9. Lan will notify the stakeholders about the revised schedule by December 3. The old December 4 deadline is no longer valid.
```

**Expected JSON**

```json
{
  "summary": "The team extended the payment integration deadline to December 9 and assigned implementation, testing, and stakeholder communication.",
  "decisions": [
    "Move the overall payment integration deadline from 2026-12-04 to 2026-12-09."
  ],
  "actions": [
    {
      "owner": "Phu",
      "action": "Finish the payment integration",
      "due_date": "2026-12-07"
    },
    {
      "owner": "Hung",
      "action": "Complete integration testing",
      "due_date": "2026-12-09"
    },
    {
      "owner": "Lan",
      "action": "Notify stakeholders about the revised schedule",
      "due_date": "2026-12-03"
    }
  ]
}
```

**Evaluation note:** Differentiate overall milestone deadline from Phu's implementation deadline.

### TC17 – Incident Review and Follow-up

**Category:** Complex

**Meeting Notes (input)**

```text
Meeting Date: 2026-12-03
Attendees: Phu, Hung, Minh, Lan

The team reviewed a production outage that occurred on December 2. The incident was caused by an exhausted database connection pool. The team agreed to increase the connection pool limit and add monitoring alerts. Phu will update the database configuration by December 4. Hung will implement connection pool monitoring by December 5. Minh will add load tests by December 7. Lan will prepare the incident report by December 8. The team discussed moving the database to a larger server but decided not to proceed with that option for now.
```

**Expected JSON**

```json
{
  "summary": "After a database connection pool outage, the team approved configuration and monitoring changes while rejecting an immediate server upgrade.",
  "decisions": [
    "Increase the database connection pool limit.",
    "Add monitoring alerts for the connection pool.",
    "Do not migrate to a larger database server for now."
  ],
  "actions": [
    {
      "owner": "Phu",
      "action": "Update the database connection pool configuration",
      "due_date": "2026-12-04"
    },
    {
      "owner": "Hung",
      "action": "Implement connection pool monitoring",
      "due_date": "2026-12-05"
    },
    {
      "owner": "Minh",
      "action": "Add load tests",
      "due_date": "2026-12-07"
    },
    {
      "owner": "Lan",
      "action": "Prepare the incident report",
      "due_date": "2026-12-08"
    }
  ]
}
```

**Evaluation note:** A decision not to proceed is still a decision, not an action.

### TC18 – Informational Meeting

**Category:** Edge cases

**Meeting Notes (input)**

```text
Meeting Date: 2026-12-04
Attendees: Phu, Hung, Lan

The team reviewed the current sprint progress. All previously assigned tasks were completed successfully. The API performance remained stable, and no production incidents were reported. This was an informational meeting only. No new decisions were made, and no new action items were assigned.
```

**Expected JSON**

```json
{
  "summary": "The team reviewed completed sprint work, stable API performance, and the absence of incidents.",
  "decisions": [],
  "actions": []
}
```

**Evaluation note:** Past completed tasks are not new action items.

### TC19 – Cancelled Planning Session

**Category:** Edge cases

**Meeting Notes (input)**

```text
Meeting Date: 2026-12-07
Attendees: Phu

The sprint planning meeting was cancelled because most team members were unavailable. No project discussion took place. No decisions were made, and no action items were assigned.
```

**Expected JSON**

```json
{
  "summary": "The sprint planning meeting was cancelled due to low attendance and no discussion took place.",
  "decisions": [],
  "actions": []
}
```

### TC20 – Informal Discussion with Unclear Statements

**Category:** Edge cases

**Meeting Notes (input)**

```text
Meeting Date: 2026-12-08
Attendees: Phu, Hung, Minh

Phu: The API seems slower than usual.
Hung: Maybe the database is causing the issue.
Minh: We should probably check the logs sometime.
Phu: That might be useful.
Hung: Let's discuss it again in the next meeting.

No one was explicitly assigned to investigate the issue, no deadline was established, and no formal decision was recorded.
```

**Expected JSON**

```json
{
  "summary": "The team informally discussed possible API slowness and a potential database issue without assigning work or making a formal decision.",
  "decisions": [],
  "actions": []
}
```

**Evaluation note:** Speculation and vague suggestions must not become action items.

## Suggested evaluation process

1. Send each `input` as `meeting_text` to the endpoint.
2. Validate the successful response against the shared schema.
3. Compare decision and action facts against `expected` using a consistent semantic matching rubric, plus strict owner/date checking.
4. Track schema compliance separately from extraction accuracy.
5. Run five error scenarios separately (not part of the 20 content cases).
