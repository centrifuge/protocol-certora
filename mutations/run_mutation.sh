#!/usr/bin/env bash
# Reproduce a mutation kill: apply certora/mutations/<Contract>/<N>.sol over its
# @target source, run its @conf on its @rules, then restore the original source.
# Reading the verdict: the line beginning "[run_mutation] done:" says it outright.
# It is the last line on a decided run and, on the two undecided ones, the line the
# explanation follows. It says Killed, Survived, NOT RUN or NOT DECIDED, and the
# last two are real answers rather than failures to produce one: NOT RUN
# means no rule of @rules was reached, so the mutant was never presented to the
# suite, and NOT DECIDED means rules ran and none reported, usually a solver out of
# budget.
# Exit code: 0 Survived, 1 Killed, 2 NOT RUN and NOT DECIDED alike (one code,
# because neither grades the mutant), 3 error, 5 refusal, 130 interrupted. The
# distinction matters: certoraRun exits nonzero both when a rule is VIOLATED and
# when it never got as far as running one (a typecheck error, an @rules name the
# spec does not carry), so "nonzero = Killed" would score a tooling failure as a
# kill, hence every error path here exits 3, never 1. 3 is that non-verdict tooling
# failure: bad arguments, a missing mutant/conf/target/prover, an untracked or
# dirty target, or a target that did not restore cleanly, which voids a verdict the
# prover may already have given. 5 is the @requires-breakdown fuse: a mutant whose
# @rules already fail on clean source cannot be judged from a verdict at all, so
# the run is refused before the source is touched and no verdict is printed. 130 is
# Ctrl-C, SIGTERM or SIGHUP, returned once the source is back, so a caller can tell
# an interrupted run from a finished one. That reading holds for a local run: a
# cloud run returns as soon as the job is submitted, so read its verdict in the
# job's web report.
# Backup: the target is copied to <target>.mutbak and restored from it on exit;
# git is used only to check that the target is pristine before and after the run.
#
#   ./certora/mutations/run_mutation.sh <Contract> <N>
#   e.g. ./certora/mutations/run_mutation.sh Accounting 602
set -u
cd "$(dirname "$0")/../.." || exit 3

CONTRACT="${1:-}"
N="${2:-}"
if [ -z "$CONTRACT" ] || [ -z "$N" ]; then
    echo "usage: $0 <Contract> <N>   (e.g. $0 Accounting 602)"
    exit 3
fi
# Home lookup: mutants live under certora/mutations/<Contract>/<N>.sol; MUT_DIR overrides the base directory.
MUT="${MUT_DIR:-certora/mutations}/$CONTRACT/$N.sol"
if [ ! -f "$MUT" ]; then
    echo "error: mutant not found: $MUT"
    if [ -d "certora/mutations/$CONTRACT" ]; then
        echo "       available in $CONTRACT: $(ls certora/mutations/$CONTRACT/*.sol 2>/dev/null | xargs -n1 basename 2>/dev/null | sed 's/\.sol$//' | tr '\n' ' ')"
    else
        echo "       available contracts: $(ls -d certora/mutations/*/ 2>/dev/null | xargs -n1 basename 2>/dev/null | tr '\n' ' ')"
    fi
    exit 3
fi

hdr() { sed -n "s/^ \* @$1:[[:space:]]*//p" "$MUT" | head -1; }
CONF="$(hdr conf)"
TARGET="$(hdr target)"
RULES="$(hdr rules | tr ',' ' ')"
if [ -z "$CONF" ] || [ -z "$TARGET" ] || [ -z "$RULES" ]; then
    echo "error: incomplete @conf/@target/@rules header in $MUT"
    exit 3
fi
[ -f "$CONF" ] || { echo "error: conf not found: $CONF"; exit 3; }
[ -f "$TARGET" ] || { echo "error: target not found: $TARGET"; exit 3; }
[ -f "$TARGET.mutbak" ] && { echo "error: stale $TARGET.mutbak found; resolve it before running"; exit 3; }

# Warn, before the source is touched, about an @rules name this conf cannot run: the shape that made a
# typecheck failure look like a kill. Only what the ENTRY spec DECLARES or explicitly `use`s counts: a
# plain import does not make an imported rule verifiable, so an @rules mixing a transitions rule with an
# invariant from the imported valid_state spec dies in the typechecker and no rule runs at all.
# A warning and not a refusal: the parse is textual, and the verdict line reports NOT RUN either way.
SPEC="$(sed -n 's/.*"verify"[[:space:]]*:[[:space:]]*"[^:]*:\([^"]*\)".*/\1/p' "$CONF" | head -1)"
if [ -n "$SPEC" ] && [ ! -f "$SPEC" ]; then
    echo "[run_mutation] warning: $CONF verifies $SPEC, which is not in the tree; @rules cannot be checked against it"
elif [ -n "$SPEC" ]; then
    for r in $RULES; do
        grep -qE "^[[:space:]]*(rule|invariant|use[[:space:]]+(rule|invariant))[[:space:]]+$r\b" "$SPEC" \
            || echo "[run_mutation] warning: @rules names '$r', which $SPEC neither declares nor uses"
    done
fi

# Checked before the source is touched: a missing prover would otherwise mutate the
# tree, fail with 127, and leave the reviewer reading a tooling error as a verdict.
command -v certoraRun >/dev/null 2>&1 || { echo "error: certoraRun not on PATH; install the Certora CLI first"; exit 3; }

# The pristine check has to run in the work tree that actually tracks the target.
# Targets under lib/ belong to their own repository (a submodule of this one), so a
# git command issued here would report them clean whatever their contents. Ask git
# from the target's own directory instead, and refuse to run when it does not know
# the file: that means the containing repository is not checked out here, and the
# before/after comparison would be vacuous.
TARGET_DIR="$(dirname "$TARGET")"
TARGET_BASE="$(basename "$TARGET")"
git -C "$TARGET_DIR" ls-files --error-unmatch "$TARGET_BASE" >/dev/null 2>&1 || {
    echo "error: $TARGET is not tracked in a git work tree of its own"
    echo "       (an uninitialized submodule looks like this: check it out first)"
    exit 3
}
# `status --porcelain`, not `diff --quiet`: diff compares against the INDEX, so a
# staged edit of the target reads as pristine and the run would grade modified source.
pristine() { [ -z "$(git -C "$TARGET_DIR" status --porcelain -- "$TARGET_BASE")" ]; }
pristine || { echo "error: $TARGET has local modifications (staged or unstaged); restore it before running"; exit 3; }

restore() {
    if [ -f "$TARGET.mutbak" ]; then
        cp "$TARGET.mutbak" "$TARGET" && rm -f "$TARGET.mutbak"
        echo "[run_mutation] restored $TARGET"
    fi
}
trap restore EXIT
trap 'restore; trap - EXIT; exit 130' INT TERM HUP

# A mutant whose @rules are ALREADY VIOLATED on the clean source cannot be judged by this script, and
# saying so is the whole of the fix. `Violated for:` appears in the log whether or not the mutant did
# anything, because the pre-existing failure is still there, so the verdict test below would answer
# KILLED to any edit at all, including an empty one. The outcome for such a mutant lives in the
# per-method breakdown: the rule holds on most selectors and fails on one, and a kill is a method
# moving from SUCCESS to FAIL, which the verdict column cannot show.
#
# The mutants carry that caveat in their own headers already. It was written for a human and the
# decision is taken by this script, which did not read it: a convention living where nobody enforces
# it. Hence a machine-readable field, and a refusal rather than a guess.
if [ "$(hdr requires-breakdown)" = "true" ]; then
    echo "[run_mutation] this mutant is NOT decidable from a verdict."
    echo "               Its rules already fail on the clean source at one selector, so the log carries"
    echo "               'Violated for:' regardless of what the edit did, and any verdict this script"
    echo "               printed would say KILLED for an empty change."
    echo "               Read the per-method breakdown of the run instead: the kill is a method moving"
    echo "               from SUCCESS to FAIL, and the rule's overall verdict stays Violated either way."
    echo "               Run it yourself with:"
    echo "                 certoraRun $CONF --rule $RULES"
    echo "               and compare the method table against the same run on unmodified source."
    exit 5
fi

# Both copies are guarded: an unchecked backup that failed (read-only tree, full disk)
# would be followed by an apply that overwrites the source with no way back.
cp "$TARGET" "$TARGET.mutbak" || { echo "error: could not back up $TARGET; source untouched"; exit 3; }
cp "$MUT" "$TARGET" || { echo "error: could not apply $MUT"; exit 3; }
echo "[run_mutation] applied $MUT over $TARGET"
echo "[run_mutation] certoraRun $CONF --rule $RULES"
LOG="$(mktemp -t run_mutation.XXXXXX)"
certoraRun "$CONF" --rule $RULES 2>&1 | tee "$LOG"
status="${PIPESTATUS[0]}"

restore
trap - EXIT INT TERM HUP
pristine || { echo "error: $TARGET did not restore cleanly"; rm -f "$LOG"; exit 3; }

# A verdict is read from POSITIVE evidence that rules were checked, never from the exit
# code and never from a list of known error strings. certoraRun answers nonzero both when a
# rule is VIOLATED and when it never got as far as running one, and the set of ways a run can
# fail before that point is open: a solidity compile error, an unresolved import, a missing
# dependency, a prover version skew. A blacklist of failure strings scores every unlisted
# failure as a KILL, which hands the reader a verdict from a run that did not happen.
#
# So the question asked here is the opposite one: is there proof that at least one rule of
# @rules was actually checked. If not, the answer is NOT RUN whatever the process returned.
# This fails SAFE: a future prover that renames its markers yields NOT RUN, never a kill.
#
# Every read of the log uses grep -a. The prover's output carries null bytes, and without it
# grep treats the log as binary and reports NO MATCH on a marker that is present, which would
# deny a real kill. A positive marker is only as good as the ability to read it, and this one
# was measured missing a match on a log with a single null byte in it.
checked=0
for r in $RULES; do
    if grep -aqE "Checking rule ${r}|\"${r}\"[[:space:]]*:" "$LOG"; then checked=1; break; fi
done
if [ "$checked" -eq 0 ] && grep -aq "Checking rule" "$LOG"; then checked=1; fi

if [ "$checked" -eq 0 ]; then
    echo "[run_mutation] done: NOT RUN; no rule of @rules was reached, so this is neither Killed nor Survived"
    echo "               The run ended before rule checking began. Common causes, in order:"
    echo "                 the tree's submodules are missing (git submodule update --init --recursive),"
    echo "                 a name in @rules is not declared by the spec this conf verifies,"
    echo "                 or the prover could not compile the mutated source."
    echo "               The last 20 log lines follow."
    tail -20 "$LOG" | tr -d '\000' 
    rm -f "$LOG"
    exit 2
fi
# The OUTCOME is read the same way the run itself was: from what the prover SAID, never from how the
# process ended. certoraRun exits nonzero when a rule is violated AND when it runs out of budget, so
# scoring a nonzero exit as a kill credits a mutant that was never caught, only outlasted. That matters
# most for a `satisfy`: an assert that exhausts its budget reports Timeout, a state of its own, while a
# witness still searching has simply found no witness, which is also how a real kill reports. So the
# exit code cannot tell them apart and the log can.
#
# TWO markers, and the second is not optional. `Violated for:` prints once per broken rule and is
# absent from a timeout entirely. `SANITY_FAILED` is the other side of the same boundary: a mutant that
# renders a rule VACUOUS has been caught, because mutation testing asks whether the suite REACTED, not
# what it proved, and a rule reporting that it can no longer say anything has reacted. Requiring only
# the first marker would score every vacuity mutant as a survivor.
#
# A timeout on one rule while another rule of the same @rules fires is still a kill, earned by that
# other rule, and it falls out of counting occurrences rather than deciding per rule.
killers=$(grep -ac "Violated for:" "$LOG" 2>/dev/null || true)
vacuous=$(grep -ac "SANITY_FAILED" "$LOG" 2>/dev/null || true)
rm -f "$LOG"
if [ "${killers:-0}" -eq 0 ] && [ "${vacuous:-0}" -eq 0 ]; then
    if [ "$status" -eq 0 ]; then
        echo "[run_mutation] done: mutant SURVIVED; every case of its @rules verified on the mutated source"
        exit 0
    fi
    echo "[run_mutation] done: NOT DECIDED; the run ended nonzero but no rule of @rules reported"
    echo "               VIOLATED or SANITY_FAILED, so nothing was caught. The usual cause is the"
    echo "               solver running out of budget, which is not a kill: raise the conf's own"
    echo "               timeout and run it again. Scoring this as Killed would bank coverage the"
    echo "               suite never earned."
    exit 2
fi
echo "[run_mutation] done: mutant KILLED; a rule of its @rules reported VIOLATED or SANITY_FAILED on the mutated source"
exit 1
