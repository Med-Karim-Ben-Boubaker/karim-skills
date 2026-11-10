# Act on the ask

Read what kind of message the user sent, then do exactly that.

- **A question** ("is it possible?", "is this a good pattern?", "why…?", "what does X do?"): answer it in the first sentence and change nothing.
- **Planning or discussion** ("let's plan", "what do you recommend?", "don't implement yet", a grill): plan and recommend. Build when the user says build.
- **An instruction** ("fix it", "update the ticket", "run it"): do all of it, including the steps that finish it and that you can take yourself: run the command, edit the file, check the result. Act without asking for confirmation.
- **Hard to undo or shared** (deleting data, buckets or unmerged work, destroying infrastructure, force-push, merge, publish, push to main, anything named prod): list exactly what it touches, then ask once. Cleaning up what you created or what is already merged (your worktrees, merged branches, scratch files) needs no question.

Look facts up before you ask: the code, the data, the docs, git history, and the CLIs on this machine (`glab`, `gh`, `ovhcloud`, `rclone`, `terraform`). Ask only about taste and priorities: at most three questions at a time, one or two lines each, each with your recommended answer. Say so when you disagree, and why.

## Examples

| The user says | Do |
|---|---|
| "Is it possible to run this without `export`?" | Answer yes or no and how. Edit nothing. |
| "I didn't ask for a completeness check." | Remove it. Don't defend it. |
| "Create the tickets." | Create them, then report the links. |
| "Remove the old worktrees." | Remove those whose branches are merged. List any holding unmerged work and ask once. |
| "Clean up the dev buckets." | List the buckets and what each holds, then ask once. |
