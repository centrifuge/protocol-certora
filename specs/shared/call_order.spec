// Call order clock: a model stamps each call it records with a rising tick.

persistent ghost mathint ghostCallClock;

function callOrderTickCVL() returns mathint {
    mathint tick = ghostCallClock;
    ghostCallClock = tick + 1;
    return tick;
}
