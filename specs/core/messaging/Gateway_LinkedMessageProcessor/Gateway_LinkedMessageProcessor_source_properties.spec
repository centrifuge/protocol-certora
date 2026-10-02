import "setup/Gateway_LinkedMessageProcessor_base.spec";
import "setup/Gateway_LinkedMessageProcessor_source.spec";

// --- reverts ---

// GW-RV-24: an upgrade message opening a batch fails unless sent from mainnet.
rule rvGwHandleRefusesAnUpgradeFromANetworkOtherThanMainnet(env e, uint16 c, bytes batch) {

    setupEnv(e);
    uint8 kind = _BytesSlice.toUint8Pure(batch, 0);
    require(kind == 1 || kind == 2, "SCOPE: an upgrade message opens the batch");
    require(c != MAINNET_CENTRIFUGE_ID_GW(), "SCOPE: sent from a network other than mainnet");
    mathint forwardedBefore = ghostGwForwardCount;

    _Gateway.handle@withrevert(e, c, batch);

    assert(lastReverted && ghostGwForwardCount == forwardedBefore,
        "an upgrade from off mainnet reverts with nothing forwarded");
}

// GW-RV-25: a hub-to-spoke message opening a batch fails unless sent from its pool's hub.
rule rvGwHandleRefusesAHubMessageOffItsPoolHome(env e, uint16 c, bytes batch) {

    setupEnv(e);
    require(POOL_HOMED_TYPE_GW(_BytesSlice.toUint8Pure(batch, 0)), "SCOPE: a hub-to-spoke message opens the batch");
    mathint home = _BytesSlice.toUint64Pure(batch, 1) / 2^48;
    require(home == 0 || to_mathint(c) != home, "SCOPE: sent from off the pool's home, or a pool with no home");
    mathint forwardedBefore = ghostGwForwardCount;

    _Gateway.handle@withrevert(e, c, batch);

    assert(lastReverted && ghostGwForwardCount == forwardedBefore,
        "a hub message from off its pool's home reverts with nothing forwarded");
}

// GW-RV-26: an asset message opening a batch fails for an ISO-4217 asset or if sent off its home network.
rule rvGwHandleRefusesAnAssetMessageOffItsHomeOrForAnIsoAsset(env e, uint16 c, bytes batch) {

    setupEnv(e);
    uint8 kind = _BytesSlice.toUint8Pure(batch, 0);
    require(kind == 3 || kind == 14 || kind == 16, "SCOPE: an asset registration, holding report or request opens the batch");
    mathint home = _BytesSlice.toUint128Pure(batch, kind == 3 ? 1 : 25) / 2^112;
    require(home == 0 || to_mathint(c) != home, "SCOPE: an ISO-4217 asset, or sent from off the asset's home");
    mathint forwardedBefore = ghostGwForwardCount;

    _Gateway.handle@withrevert(e, c, batch);

    assert(lastReverted && ghostGwForwardCount == forwardedBefore,
        "an ISO-4217 or off-home asset message reverts with nothing forwarded");
}
