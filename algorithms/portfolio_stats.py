"""
This module has been copied from a previous repository.

"""


def calculate_portfolio_equity(assets):
    # Calculate Portfolio Equity
    portfolio_equity = sum(asset.get("equity", 0) for asset in assets)

    # Round the Portfolio Equity to the nearest dollar
    portfolio_equity_rounded = round(portfolio_equity)

    # Return the calculated Portfolio Equity directly
    return portfolio_equity_rounded


def calculate_group_equity(assets):
    # Initialize a dictionary to store group equity
    group_equity = {}

    # Iterate through the list of assets
    for asset in assets:
        # Get the group assignment of the current asset
        group_assignment = asset.get("group_assignment")

        # Get the equity of the current asset
        equity = asset.get("equity")

        # Check if the group assignment already exists in the group_equity dictionary
        if group_assignment in group_equity:
            # If the group assignment exists, add the equity of the current asset to the existing sum
            group_equity[group_assignment] += equity
        else:
            # If the group assignment doesn't exist, initialize it with the equity of the current asset
            group_equity[group_assignment] = equity

    return group_equity


def calculate_portfolio_weighting(assets, portfolio_equity_rounded):
    # Initialize list to store asset weightings as tuples
    asset_weightings = []

    # Calculate Portfolio Weighting for each asset
    for asset in assets:
        equity = asset.get("equity", 0)
        symbol = asset.get("symbol")

        if portfolio_equity_rounded != 0:  # Avoid division by zero
            asset_weighting = round((equity / portfolio_equity_rounded) * 100, 2)
        else:
            asset_weighting = 0  # Set weighting to 0 if portfolio equity is 0

        # Store asset weighting as a tuple (symbol, weighting)
        asset_weightings.append((symbol, asset_weighting))

    return asset_weightings


def calculate_group_weighting(assets, group_equity):
    group_weighting = {}

    for asset in assets:
        group_assignment = asset.get("group_assignment")
        equity = asset.get("equity", 0)
        symbol = asset.get("symbol")

        if group_assignment not in group_weighting:
            group_weighting[group_assignment] = {}

        group_equity_for_group = group_equity.get(group_assignment, 0)
        asset_weighting = (
            0
            if group_equity_for_group == 0
            else round((equity / group_equity_for_group) * 100, 2)
        )

        group_weighting[group_assignment][symbol] = asset_weighting

    return group_weighting


def calculate_group_portfolio_weighting(portfolio_equity, group_equity):
    # Initialize a dictionary to store group portfolio weightings
    group_portfolio_weighting = {}

    # Iterate through each group and calculate its portfolio weighting
    for group_assignment, equity in group_equity.items():
        if portfolio_equity != 0:
            group_portfolio_weighting[group_assignment] = round(
                (equity / portfolio_equity) * 100, 2
            )
        else:
            group_portfolio_weighting[group_assignment] = (
                0  # Set to 0 if portfolio equity is 0
            )

    return group_portfolio_weighting