// Pool domain: two pinned pool ids, sized by the single or multi-pool mode.

// SCOPE: pinned pools stand for any, as pools never share rows.
persistent ghost uint64 ghostPoolA64;

persistent ghost uint64 ghostPoolB64;

definition VALID_POOL(mathint p) returns bool =
    p == ghostPoolA64 || p == ghostPoolB64;
