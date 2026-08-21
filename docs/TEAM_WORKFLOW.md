# TEAM WORKFLOW

## Team model

Four-person team working from one repository.

## Branch policy

- `main` = stable, reviewed project state.
- `develop` = integration branch once implementation begins.
- `feature/<short-description>` = individual task branches.

No direct work should normally be developed on `main`.

## Standard task flow

1. Create or select a GitHub Issue.
2. Assign the task to a team member.
3. Create a feature branch from the appropriate integration branch.
4. Implement and test the change.
5. Commit with a descriptive message.
6. Open a Pull Request.
7. Review the change.
8. Run relevant validation.
9. Merge only when acceptance criteria are satisfied.
10. Update project state/documentation when the task changes project knowledge.

## Research work

Research tasks follow the same traceability rule as software tasks. A dataset decision, experimental protocol, metric change, architecture change or scope change should have an Issue or documented decision record.

## Avoid

- Direct pushes to `main` for normal development.
- Large unreviewed changes mixing unrelated work.
- Committing raw large datasets when external storage is more appropriate.
- Treating a passing unit test as scientific validation.
- Changing a research claim without recording the reason.
