# Watchable commands

When a terminal command is long-running (builds, full test suites, installs, migrations, benchmarks, training, dev servers, anything likely to take more than about 30 seconds) or the user expects to see its output, make its progress watchable by the user instead of running it silently.

1. **Log to a file.** Send the command's full output to a log file, whether it runs in the foreground or the background: `<command> > <log> 2>&1`. Put logs in the session's scratchpad directory if one is listed, otherwise `/tmp/claude-logs/`, named `<what>-<YYYYMMDD-HHMMSS>.log`.
2. **Make it verbose.** When the tool has a verbose or progress flag (`--verbose`, `-v`, `--progress`, `--reporter=verbose`, `--info`), use it, so the log shows progress, not just the final result.
3. **Hand over the tail command before you wait.** Right after starting the command, give the user the exact command to watch it, with the full absolute path, in its own code block:

   ```
   tail -f /absolute/path/to/<what>-<timestamp>.log
   ```

   Do this before waiting on the result, so the user can follow along in another terminal.
4. **Don't flood your own context.** Read the log with `tail -n` or `grep`, not `cat`. Pull only the lines that carry the signal: errors, the summary, the failing test.
5. **Report the outcome** with the exit status, the relevant lines, and the log path again.

Short commands (a `git status`, a single test file, a quick grep) run normally: no log file, no tail command.
