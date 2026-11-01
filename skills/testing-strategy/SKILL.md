---
name: testing-strategy
description: Design test strategies and test plans. Trigger with "how should we test", "test strategy for", "write tests for", "test plan", "what tests do we need", or when the user needs help with testing approaches, coverage, or test architecture. For actually driving a browser to verify or debug a local web app with Playwright, see webapp-testing.
---

# Testing Strategy

Design effective testing strategies balancing coverage, speed, and maintenance.

## Testing Pyramid

```
        /  E2E  \         Few, slow, high confidence
       / Integration \     Some, medium speed
      /    Unit Tests  \   Many, fast, focused
```

## Strategy by Component Type

- **API endpoints**: Unit tests for business logic, integration tests for HTTP layer, contract tests for consumers
- **Data pipelines**: Input validation, transformation correctness, idempotency tests
- **Frontend**: Component tests, interaction tests, visual regression, accessibility
- **Infrastructure**: Smoke tests, chaos engineering, load tests

## What to Cover

Focus on: business-critical paths, error handling, edge cases, security boundaries, data integrity.

Skip: trivial getters/setters, framework code, one-off scripts.

## Output

Produce a test plan with: what to test, test type for each area, coverage targets, and example test cases. Identify gaps in existing coverage.


## TDD red-green-refactor (adopted from obra/superpowers, MIT)

When the strategy is TDD, the execution discipline is in
`references/tdd.md`: write a failing test, watch it fail, write the minimal
code, watch it pass, commit — and delete any production code written before
its test. `references/writing-good-tests.md` defines what makes a test
good vs. an anti-pattern (the strategy doc decides *whether* TDD fits a
given project; these references govern *how* it runs).
