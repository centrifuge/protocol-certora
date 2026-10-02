// Math model: the pricing mulDiv helpers, summarized as exact mathint division.

methods {
    // SAFE: exact mathint division, rounding as the 512 bit path does.

    // No live caller: the D18 constructions in scope fold at compile time.
    function MathLib.mulDiv(uint256 x, uint256 y, uint256 denominator) internal returns (uint256)
        => mulDivCVL(x, y, denominator);

    // Rounding: Down = 0, Up = 1, Zero = 2, and only Up rounds up here.
    function MathLib.mulDiv(uint256 x, uint256 y, uint256 denominator, MathLib.Rounding rounding) internal returns (uint256)
        => mulDivRoundingCVL(x, y, denominator, to_mathint(rounding) == 1);
}

function mulDivCVL(uint256 x, uint256 y, uint256 denominator) returns uint256 {
    require(denominator != 0, "ASSERT: the divisor must be nonzero");
    mathint product = x * y;
    return require_uint256(product / denominator);
}

function mulDivRoundingCVL(uint256 x, uint256 y, uint256 denominator, bool roundUp) returns uint256 {
    require(denominator != 0, "ASSERT: the divisor must be nonzero");
    mathint product = x * y;
    mathint floorResult = product / denominator;
    if (roundUp && product % denominator != 0) {
        return require_uint256(floorResult + 1);
    } else {
        return require_uint256(floorResult);
    }
}
