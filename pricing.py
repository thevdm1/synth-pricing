#PRICING FUNCTIONS
#xsushi apy doesn't need pricing as the pricing is done at the price ID level, not FPL level

def price_leveraged_IL(initial_price, expiry_price, leverage_factor):
    """
    Using the IL approximation formula of IL = ((2 x (sqrt(p)))/(p+1)) -1
    and then taking the abs(IL) x 20 + 1 to make it volatile + tradable
    """
    p = initial_price/expiry_price
    il = ((2*(p**0.5))/(p+1))-1 #power of 0.5 gives same result as sqrt
    leveraged_il_synth_price = (abs(il)*leverage_factor) + 1
    return leveraged_il_synth_price

def price_2xdpi(initial_price, expiry_price, upper_bound, leverage_factor = 2):
    return_factor = expiry_price/initial_price
    return_ = return_factor - 1
    price_2xdpi_synth = (upper_bound/2)*(1+(return_*leverage_factor))
    return price_2xdpi_synth

#PCT LONG FUNCTIONS FOR FPLS
def get_long_pct_leveraged_IL(initial_price, expiry_price, upper_bound, pct_long_cap, leverage_factor):
    leveraged_il_price = price_leveraged_IL(initial_price, expiry_price, leverage_factor)
    print(f'Leveraged IL synth price: {leveraged_il_price}')
    assert pct_long_cap < 1, 'pct_long_cap must be < 1!'
    effective_upper_cap = upper_bound*pct_long_cap
    effective_lower_cap = upper_bound*(1 - pct_long_cap)
    if leveraged_il_price > effective_upper_cap:
        transformed_expiry_price = effective_upper_cap
    elif leveraged_il_price < effective_lower_cap:
        transformed_expiry_price = effective_lower_cap
    else:
        transformed_expiry_price = leveraged_il_price
    pct_long = transformed_expiry_price/upper_bound
    
    return pct_long


def get_long_pct_2xdpi(initial_price, expiry_price, upper_bound, pct_long_cap):
    _2xdpi_price = price_2xdpi(initial_price, expiry_price, upper_bound, leverage_factor = 2)
    print(f'2XDPI synth price: {_2xdpi_price}')
    assert pct_long_cap < 1, 'pct_long_cap must be < 1!'
    effective_upper_cap = upper_bound*pct_long_cap
    effective_lower_cap = upper_bound*(1 - pct_long_cap)

    if _2xdpi_price > effective_upper_cap:
        transformed_expiry_price = effective_upper_cap
    elif _2xdpi_price < effective_lower_cap:
        transformed_expiry_price = effective_lower_cap
    else:
        transformed_expiry_price = _2xdpi_price
    pct_long = transformed_expiry_price/upper_bound
    
    return pct_long

def get_long_pct_linear_FPL_mod(expiry_price, upper_bound, pct_long_cap):
    """This will use the linearLSP thats been modified for easier pooling of two tokens in v2 AMMs"""
    assert pct_long_cap < 1, 'pct_long_cap must be < 1!'
    effective_upper_cap = upper_bound*pct_long_cap
    effective_lower_cap = upper_bound*(1 - pct_long_cap)
    print(f'xsushi-apy synth price: {expiry_price}')

    if expiry_price > effective_upper_cap:
        transformed_expiry_price = effective_upper_cap
    elif expiry_price < effective_lower_cap:
        transformed_expiry_price = effective_lower_cap
    else:
        transformed_expiry_price = expiry_price
    pct_long = transformed_expiry_price/upper_bound
    
    return pct_long

#RUN

def main():
    #default pct_long for now is at 90% -> 0.9

    #IL SYNTH
    #leverage level likely to be 10 to 30 -> will run first iterations of the synth at 20x, start and end prices are in eth/usd
    #starting price will be upper cap / 2 so using 2 as upper cap starting price is 1 which is a good rebasing point
    pct_long_lev_il = get_long_pct_leveraged_IL(4000, 3000, 2, 0.9, 20)
    print(f'Percentage Long Leveraged IL Synth: {pct_long_lev_il}\n')

    #2XDPI SYNTH
    #starting price will be upper cap / 2 so using 2 as upper cap starting price is 1 which is a good rebasing point
    #start and end prices are in terms of DPI/ETH
    pct_long_2xdpi = get_long_pct_2xdpi(0.1, 0.12, 2, 0.9)
    print(f'Percentage Long 2XDPI Synth: {pct_long_2xdpi}\n')

    #XSUSHI-APY SYNTH
    #XSUSHI-APY price likely to range between 2 to 40 in terms of extremes but likely to range <10% most the time
    # again upper bound/2 will be starting price in AMM
    # This time we don't target 1 as a starting point for the synth, xsushi-apy of 6 references 6% so trading this is nice and intuitive
    pct_long_xsushi_apy = get_long_pct_linear_FPL_mod(8, 14, 0.9)
    print(f'Percentage Long XSUSHI-APY Synth: {pct_long_xsushi_apy}\n')

if __name__ == '__main__':
    main()