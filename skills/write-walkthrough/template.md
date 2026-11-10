# Walkthrough: <ticket or feature>

Branch `<branch>` · commit `<short sha>`. I ran <n> of <m> steps on this commit from a fresh shell, and each showed what its **Expect:** line says; steps marked **Not run by me** need you. About <minutes> minutes.

## 0. Setup

```sh
cd <folder the work is checked out in>
git log -1 --oneline                                          # expect: <short sha> <subject>
set -a; . <main checkout>/.env; set +a                        # the env file, from the main checkout
export <APP>__OUTPUT_PATH="$PWD/.sandbox/walkthrough/output"  # writes land here, not in the real location
mkdir -p .sandbox/walkthrough/input
<install command>
```

### Sample data

| Input | What it holds | Used in | Source |
|---|---|---|---|
| `<file or record>` | <what matters in it: "4 valid rows; row 5 has no date"> | steps 1, 3 | generated |
| `<file>` | <what it is> | step 2 | your `<path>`, copied |
| `<file>` | <what it is> | step 1 | reused from `<repo path or demo.sh>` |

```sh
cat > .sandbox/walkthrough/input/<file> <<'EOF'
<contents>
EOF
cp <path you gave me> .sandbox/walkthrough/input/
<app command that creates the walkthrough- records>
```

## 1. <criterion, as the ticket words it>

```sh
<command on .sandbox/walkthrough/input/<file>>
```

**Expect:** `<exact output line>`, from <the sample record behind it>.
Before this change: <what the same command showed>.

## 2. <criterion with a UI>

```sh
<start command> > .sandbox/walkthrough/server.log 2>&1 &
echo $! > .sandbox/walkthrough/server.pid
```

Wait until `.sandbox/walkthrough/server.log` shows `<ready line>`, then:

1. Open <URL>.
2. Click **<label>**.
3. Type `<text>` in **<field label>** and press Enter.

**Expect:** <what the screen shows>, as in `<Demo screenshot path>`.

## 3. Edge case: <what goes wrong>

```sh
<command on the edge-case record>
```

**Expect:** <the message or output>. A crash here is a bug.

## 4. Cleanup

```sh
kill "$(cat .sandbox/walkthrough/server.pid)"
<app command that deletes the walkthrough- records>
rm -rf .sandbox/walkthrough
```

## Your check

| Step | Expected | OK? |
|---|---|---|
| 1 | <short expected> | ☐ |
| 2 | <short expected> | ☐ |
| 3 | <short expected> | ☐ |

If a step shows something else, paste its output back to me: that's a bug report.
