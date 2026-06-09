# 04 — Stash side-quest

**Scenario:** Your PR is open. You decided to tweak the bomb's color, so you've
got uncommitted changes in your working directory. *Right then*, your
instructor announces a small fix has landed on upstream `main` —
**press R to restart after game over**. Everyone wants it. But your changes
aren't ready to commit.

You can't pull on top of dirty working tree changes — Git will refuse. You
have three options:
1. Commit your half-done work (creates a junk commit you'll have to clean up)
2. Throw your changes away (no!)
3. **Stash them, pull, then re-apply them.** ← this lesson

---

## 1. See your dirty state

```bash
git status
# On branch feature/bomb-item
# Changes not staged for commit:
#   modified:   items/bomb.py
```

## 2. Stash

```bash
git stash push -m "wip: tweaking bomb color"
```

`git stash` is like a clipboard for your uncommitted work. It saves your
changes and resets your working tree to a clean state.

```bash
git status
# nothing to commit, working tree clean
```

Your changes are still safe — they're in the stash:

```bash
git stash list
# stash@{0}: On feature/bomb-item: wip: tweaking bomb color
```

## 3. Pull the upstream fix

Same routine as [Bonus 1 — sync your fork](bonus-1-reflog-and-sync-fork.md): update
local main from upstream, push it to your fork to keep them in sync, then
merge main into your feature branch.

```bash
git checkout main
git pull upstream main            # download + apply upstream's new commits
git push origin main              # keep your fork's main in sync with upstream
git checkout feature/bomb-item
git merge main                    # bring the fix into your feature branch
```

> **Why merge main into the feature branch?** So your branch is up-to-date
> with the fix before you keep working. Otherwise you'd be building on top
> of stale main, and you'd hit the conflict later when you try to merge.
>
> **Why also push origin/main?** Without it, your fork's `main` drifts behind
> upstream's. Anyone cloning your fork would get old code, and your next
> feature branch would start from the wrong place. Cheap habit, big payoff.

Run the game once after the merge — you should now be able to press **R**
to restart after game over.

## 4. Pop your stash back

```bash
git stash pop
# On branch feature/bomb-item
# Changes not staged for commit:
#   modified:   items/bomb.py
# Dropped refs/stash@{0} (...)
```

Your tweaks are back. Carry on.

> **`pop` vs `apply`:** `git stash pop` applies the stash *and removes it
> from the stash list*. `git stash apply` applies it but keeps it. Use
> `apply` when you want to apply the same stash to multiple branches.

## 5. If popping causes a conflict

If `main` happened to touch the same lines you'd been editing, `git stash pop`
can produce a conflict — same conflict markers, same resolution process you'll
see in the next lesson. The stash stays in the list until you resolve it,
then `git stash drop stash@{0}` removes it.

---

## Cheat sheet

| Command | Does |
|---|---|
| `git stash` (or `git stash push`) | Save dirty changes, clean working tree |
| `git stash push -m "msg"` | Stash with a label |
| `git stash list` | Show all stashes |
| `git stash pop` | Re-apply the most recent stash and remove it |
| `git stash apply` | Re-apply but keep the stash |
| `git stash drop stash@{0}` | Delete a specific stash without applying |
| `git stash show -p stash@{0}` | View what a stash contains |

---

→ [Next: 05 — The conflict](05-the-conflict.md)
