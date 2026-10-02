// Share class domain: two pinned class ids, sized by the single or multi mode.

// SCOPE: pinned classes stand for any, their key is never computed.
persistent ghost bytes16 ghostShareClassA;

persistent ghost bytes16 ghostShareClassB;

definition VALID_SC(bytes16 sc) returns bool =
    sc == ghostShareClassA || sc == ghostShareClassB;
