# Canonical Branch Synchronization Rule

When a substantial project change is completed and agreed upon by the end of a project chat, `main` and `develop` must be brought to exactly the same canonical commit/state before the chat is considered complete, unless an explicitly documented review or integration task is intentionally left pending.

During active work, changes may live on task/research branches or `develop`. Once accepted, promote them so:

`main == develop`

Branch synchronization does not imply scientific validation or stage completion.