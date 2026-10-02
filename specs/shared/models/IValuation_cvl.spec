// Valuation model: a free per asset price and quote for the holdings scenes.

methods {
    // SCOPE: the summaries ignore their pool, class and asset keys.

    // UNSAFE: drops the unset-price refusal, a quote always comes back.
    function _.getQuote(uint64 poolId, bytes16 scId, uint128 assetId, uint128 baseAmount) external
        => valuationGetQuoteCVL(calledContract, assetId, baseAmount) expect uint128;

    // UNSAFE: drops the unset-price refusal, a price always comes back.
    function _.getPrice(uint64 poolId, bytes16 scId, uint128 assetId) external
        => valuationGetPriceCVL() expect uint128;
}

function valuationGetPriceCVL() returns uint128 {
    uint128 price;
    return price;
}

persistent ghost mathint ghostValQuoteCount {
    init_state axiom ghostValQuoteCount == 0;
    axiom ghostValQuoteCount >= 0;
}
persistent ghost address ghostValLastCallee;
persistent ghost uint128 ghostValLastAsset128;
persistent ghost uint128 ghostValLastBase128;
persistent ghost uint128 ghostValLastQuote128;

function valuationGetQuoteCVL(address valuation, uint128 assetId, uint128 baseAmount) returns uint128 {
    uint128 quote;
    require(baseAmount != 0 || quote == 0, "TRUSTED: managers pick valuations that price zero at zero");
    ghostValQuoteCount = ghostValQuoteCount + 1;
    ghostValLastCallee = valuation;
    ghostValLastAsset128 = assetId;
    ghostValLastBase128 = baseAmount;
    ghostValLastQuote128 = quote;
    return quote;
}
