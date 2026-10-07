# Bullet Point Engineering Formulas

A recruiter skims bullet points in 2 to 3 seconds each. Every bullet must communicate tangible technical impact, quantifiable outcome, and engineering judgment.

______________________________________________________________________

## The Three Core Frameworks

### 1. Google XYZ Formula (Recommended)

> **"Accomplished [X] as measured by [Y] by doing [Z]"**

Move the metric ([Y]) as close to the beginning of the bullet as possible so skimming eyes catch it immediately.

- **Formula**: `[Verb + Outcome (X)] by [Metric (Y)] through [Technical Implementation (Z)]`
- **Example**: "Reduced API p99 latency from 450ms to 85ms by refactoring search queries to use asynchronous PostgreSQL read replicas"
- **Example**: "Cut CI build times by 42% by containerizing test suites and implementing Docker layer caching"

### 2. CAR Formula (Challenge, Action, Result)

Best for technical troubleshooting or refactoring legacy systems:

- **Challenge**: The technical bottleneck or bug.
- **Action**: The architecture or algorithm you chose.
- **Result**: The measured impact.
- **Example**: "Resolved memory leak causing production server crashes under 10k RPS load by profiling heap dumps and rewriting WebSocket connection pooling in Go"

### 3. STAR Formula (Situation, Task, Action, Result)

Best for multi-team initiatives or zero-to-one product features:

- **Situation/Task**: The operational necessity.
- **Action**: What *you* engineered.
- **Result**: What happened after shipping.
- **Example**: "Architected multi-tenant telemetry pipeline ingesting 12M events daily, reducing data ingestion delays from 2 hours to sub-second streaming using Kafka and ClickHouse"

______________________________________________________________________

## Integration Over Parts List

**Rule**: It matters less what specific components you used and more how you integrated them to accomplish the goal.

### Anti-Pattern (Parts List):

> - Weak: *"Used a Raspberry Pi, C++, and stepper motor to complete task X"*
> - Weak: *"Used React, Redux, Node.js, and MongoDB to build a dashboard"*

### Pro-Pattern (Integration & Impact):

> - Strong: *"Developed Python control software interfacing with stepper motors via GPIO to achieve ±0.5° positioning accuracy for task X"*
> - Strong: *"Built real-time telemetry dashboard in React and Node.js serving 4k concurrent operators with sub-100ms WebSocket updates"*

______________________________________________________________________

## Line Length & Spillover Prevention

Recruiters subconsciously register white space and visual rhythm:

- **Optimal length**: 1 full line, or 2 nearly full lines.
- **Spillover anti-pattern**: A bullet that wraps onto line 2 with only 1 to 4 words.
  - *Bad*:
    ```
    - Refactored legacy monolithic backend to microservices using FastAPI and Docker, improving overall
      maintainability.
    ```
  - *Fix*: Either trim filler words so it fits strictly on 1 line:
    ```
    - Refactored monolithic backend to FastAPI microservices, reducing deployment cycle times by 35%
    ```
    Or expand with technical specificity to fill the second line cleanly.

______________________________________________________________________

## Handling Sensitive or Classified Content

When working on proprietary, confidential, or defense-related systems, you cannot name specific military platforms, internal codenames, or NDA-protected architectures.

**Technique**: Describe the *category*, *standard*, and *technical challenge* without revealing forbidden specifics:

- Violating: "Wrote missile guidance telemetry software for the Tomahawk Block IV using proprietary Raytheon protocol."
- Too generic: "Wrote C++ code for defense customer."
- Compliant & Strong: "Developed hard real-time C++ telemetry software on MIL-STD-1553 avionics bus, guaranteeing sub-5ms deterministic response under high EMI conditions"

______________________________________________________________________

## Software Engineering Bullet Patterns

1. **Latency & Performance**:

   - `Reduced [metric] from [A] to [B] by implementing [solution] in [language/framework]`
   - *Example*: "Reduced cold-start latency from 2.4s to 320ms by migrating serverless endpoints to Rust on AWS Lambda"

1. **Cost & Resource Optimization**:

   - `Decreased [cloud spend/resource] by [X%] by rearchitecting [component] to [approach]`
   - *Example*: "Decreased AWS infrastructure costs by 28% ($4,500/month) by migrating database instances to ARM-based Graviton3 instances"

1. **Scale & Throughput**:

   - `Architected [system/pipeline] handling [throughput/load] with [uptime/reliability metric]`
   - *Example*: "Architected distributed message queue handling 85k requests/sec across 14 nodes with 99.99% uptime using Apache Pulsar"

1. **Automation & CI/CD**:

   - `Automated [manual process] using [tool/script], saving [X] hours/week for [N] engineers`
   - *Example*: "Automated database schema migrations using Python and Liquibase, eliminating 6 hours of weekly manual deployment downtime"

1. **Root-Cause Analysis & Reliability**:

   - `Identified and resolved root cause of [system failure], reducing [error rate/crash rate] by [X%]`
   - *Example*: "Diagnosed deadlocks in distributed transactions, eliminating race conditions and cutting database connection timeouts by 94%"

______________________________________________________________________

## Hardware & Systems Bullet Patterns

1. **Design & Constraint Optimization**:

   - `Designed [component] using [software/analysis], achieving [performance metric] within [constraint]`
   - *Example*: "Designed multi-layer PCB for high-speed sensor interface using Altium Designer, achieving 1.2 Gbps data transfer within a 45x30mm form factor"

1. **Physical / Mechanical Efficiency**:

   - `Reduced [weight/cost/lead time] by [X%] through [design change or process improvement]`
   - *Example*: "Reduced chassis assembly weight by 18% through topology optimization in SolidWorks while preserving 1500N structural load tolerance"

1. **Validation & Compliance**:

   - `Validated [system/design] via [testing method], confirming compliance with [standard/spec]`
   - *Example*: "Validated high-voltage battery enclosures via thermal cycling (-40°C to 85°C), certifying compliance with ISO 26262 safety standards"
