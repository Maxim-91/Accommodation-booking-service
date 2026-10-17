# Contributing and Git Workflow

## 1. Main branch

The `main` branch contains the integrated and reviewed project state. Direct commits to `main` should be avoided. Changes are integrated through pull requests.

## 2. Branch naming

Create a separate branch for each GitHub Issue.

Use the naming convention:

`<type>/<issue-number>-<short-description>`

Examples:

- `docs/1-project-architecture`
- `feature/8-accommodation-api`
- `test/18-backend-tests`
- `ci/29-frontend-workflow`

Common branch types:

- `feature/` — new functionality
- `docs/` — documentation
- `test/` — tests and test infrastructure
- `ci/` — continuous integration configuration

## 3. Development workflow

1. Start from the latest `main` branch.
2. Create or switch to the branch associated with the Issue.
3. Implement only the changes relevant to that Issue.
4. Run the relevant checks and tests.
5. Commit the changes with a descriptive message.
6. Push the branch to GitHub.
7. Open a pull request targeting `main`.
8. Review the diff and verify the checks.
9. Merge the pull request when it is ready.
10. Confirm that the associated Issue is closed.
11. Delete the merged branch if it is no longer needed.

## 4. Commit messages

Use descriptive commit messages. Prefer the following format:

`<type>: <short description>`

Examples:

- `docs: define project requirements`
- `feat: add accommodation endpoints`
- `test: add booking service tests`
- `ci: configure backend test workflow`

## 5. Pull request requirements

Each pull request should:

- Explain what changed and why.
- Reference the related GitHub Issue.
- Include the relevant tests or verification steps.
- Avoid unrelated changes.
- Have no unresolved merge conflicts.
- Pass applicable automated checks, when configured.

Use a closing keyword such as `Closes #8` when the pull request completes the corresponding Issue.

## 6. Security and repository hygiene

- Never commit passwords, API tokens, private keys, or real personal data.
- Keep local environment files and secrets out of version control.
- Use synthetic data for development and testing.
- Keep changes focused and the repository documentation up to date.
