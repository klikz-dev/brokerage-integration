"""
This is the Sector Investor algorithm, it is currently a placeholder.
"""

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    xlk_investment = 0.0
    xlc_investment = 0.0
    xly_investment = 0.0
    xlv_investment = 0.0
    xlp_investment = 0.0
    print(request.form)  # Print all form data
    investment_amount = request.form.get('investmentAmount')
    print(investment_amount)  # Print the specific field

    if request.method == 'POST':
        # This is a POST request, so we have access to the form data.
        # You can access the form data using request.form.
        investment_amount = float(request.form.get('investmentAmount') or '0')
        xlk_current_equity = float(request.form.get('equityXLK') or '0')
        xlc_current_equity = float(request.form.get('equityXLC') or '0')
        xly_current_equity = float(request.form.get('equityXLY') or '0')
        xlv_current_equity = float(request.form.get('equityXLV') or '0')
        xlp_current_equity = float(request.form.get('equityXLP') or '0')

        #initialize Total Portfolio Value Variable
        total_portfolio_value = investment_amount + xlk_current_equity + xlc_current_equity + xly_current_equity + xlv_current_equity + xlp_current_equity
        print("Total Portfolio Value: $", total_portfolio_value)

        #This section is for the portfolio weighting set by the investment advisor. In this version these are fixed.
        xlk_targetweighting=(.23)
        xlc_targetweighting=(.225)
        xly_targetweighting=(.225)
        xlv_targetweighting=(.17)
        xlp_targetweighting=(.15)

        #Step: Calculate current total equity by summing individual equities.
        total_current_equity = xlk_current_equity + xlc_current_equity + xly_current_equity + xlv_current_equity + xlp_current_equity
        print("Total Current Equity: $", total_current_equity)

        #Step: Check to see if this is the users initial investment. 
        #If total current equity =  0, it is the initial investment
        #If total current equity = <1, it is not the initial investment

        # Initialize the is_initial_investment variable with a default value
        is_initial_investment = "No"

        if total_current_equity == 0:
            is_initial_investment = "Yes"
        elif total_current_equity < 0:
            is_initial_investment = "No"

        # Print the value of the initial_investment variable
        print("Initial Investment:", is_initial_investment)

        #Step: Calculate and intialize current weighting, this will be used in segment 5
        # Initialize variable with a value so that current equity divided by current equity is not divide by 0 error if initial investment.
        xlk_current_weighting = 0
        xlc_current_weighting = 0
        xly_current_weighting = 0
        xlv_current_weighting = 0
        xlp_current_weighting = 0

        #Step: Prevent divide by zero error.
        if total_current_equity != 0:
            xlk_current_weighting = xlk_current_equity / total_current_equity
            xlc_current_weighting = xlc_current_equity / total_current_equity
            xly_current_weighting = xly_current_equity / total_current_equity
            xlv_current_weighting = xlv_current_equity / total_current_equity
            xlp_current_weighting = xlp_current_equity / total_current_equity
        
        #Step: Calculate and intialize the weighting difference, this will be used in segment 5
        xlk_weighting_difference = xlk_targetweighting - xlk_current_weighting
        xlc_weighting_difference = xlc_targetweighting - xlc_current_weighting
        xly_weighting_difference = xly_targetweighting - xly_current_weighting
        xlv_weighting_difference = xlv_targetweighting - xlv_current_weighting
        xlp_weighting_difference = xlp_targetweighting - xlp_current_weighting

        #Step: If this is the initial investment, multiply the investment amount by the target weighting per stock.
        if is_initial_investment == "Yes":
            xlk_investment = investment_amount * xlk_targetweighting
            xlc_investment = investment_amount * xlc_targetweighting
            xly_investment = investment_amount * xly_targetweighting
            xlv_investment = investment_amount * xlv_targetweighting
            xlp_investment = investment_amount * xlp_targetweighting
        elif is_initial_investment == "No":
            xlk_investment = "Move to Segment 2"
            xlc_investment = "Move to Segment 2"
            xly_investment = "Move to Segment 2"
            xlv_investment = "Move to Segment 2"
            xlp_investment = "Move to Segment 2"




        #SEGMENT 2
        #The purpose of this segment is to check if the investment is large enough to fully rebalance the portfolio.
        #STEP: Engage Segment 2
        # Initialize the segment2 variable with a default value
        segment2 = "Off"

        if is_initial_investment == "No":
            segment2 = "On"
        elif is_initial_investment == "Yes":
            segment2 = "Off"

        #initialize variables
        investment_can_achieve_target = "No"
        xlk_targetequity_beforeoffset = xlk_targetweighting * total_current_equity
        xlc_targetequity_beforeoffset = xlc_targetweighting * total_current_equity
        xly_targetequity_beforeoffset = xly_targetweighting * total_current_equity
        xlv_targetequity_beforeoffset = xlv_targetweighting * total_current_equity
        xlp_targetequity_beforeoffset = xlp_targetweighting * total_current_equity

        #STEP: Calculate the target equity for each stock by multiplying the target weighting by the total current equity.

        if segment2 == "On":
            xlk_targetequity_beforeoffset = xlk_targetweighting * total_current_equity
            xlc_targetequity_beforeoffset = xlc_targetweighting * total_current_equity
            xly_targetequity_beforeoffset = xly_targetweighting * total_current_equity
            xlv_targetequity_beforeoffset = xlv_targetweighting * total_current_equity
            xlp_targetequity_beforeoffset = xlp_targetweighting * total_current_equity
            print("XLK Target Equity Before Offset: $", xlk_targetequity_beforeoffset)
            print("XLC Target Equity Before Offset: $", xlc_targetequity_beforeoffset)
            print("XLY Target Equity Before Offset: $", xly_targetequity_beforeoffset)
            print("XLV Target Equity Before Offset: $", xlv_targetequity_beforeoffset)
            print("XLP Target Equity Before Offset: $", xlp_targetequity_beforeoffset)

            #STEP: Calculate the investment needed to reach the target weighting before offset 
            #      by subtracting the current equity from the target equity per stock. 

            xlk_investmentneeded_beforeoffset = xlk_targetequity_beforeoffset - xlk_current_equity
            xlc_investmentneeded_beforeoffset = xlc_targetequity_beforeoffset - xlc_current_equity
            xly_investmentneeded_beforeoffset = xly_targetequity_beforeoffset - xly_current_equity
            xlv_investmentneeded_beforeoffset = xlv_targetequity_beforeoffset - xlv_current_equity
            xlp_investmentneeded_beforeoffset = xlp_targetequity_beforeoffset - xlp_current_equity
            print("XLK Investment Needed Before Offset: $", xlk_investmentneeded_beforeoffset)
            print("XLC Investment Needed Before Offset: $", xlc_investmentneeded_beforeoffset)
            print("XLY Investment Needed Before Offset: $", xly_investmentneeded_beforeoffset)
            print("XLV Investment Needed Before Offset: $", xlv_investmentneeded_beforeoffset)
            print("XLP Investment Needed Before Offset: $", xlp_investmentneeded_beforeoffset)

            #STEP: Find the lowest value of all investments needed before offset

            lowest_before_offset = min(xlk_investmentneeded_beforeoffset,xlc_investmentneeded_beforeoffset,xly_investmentneeded_beforeoffset,xlv_investmentneeded_beforeoffset,xlp_investmentneeded_beforeoffset)

            print("Lowest Before Offset: ", lowest_before_offset)

            #STEP: Calculate the offset needed per stock based on the minimum value 
            #      by adding the minimum value to each stock, 
            #      resulting in the most overweighted stock equalling $0.

            xlk_offsetneeded = (lowest_before_offset * -1) + xlk_investmentneeded_beforeoffset
            xlc_offsetneeded = (lowest_before_offset * -1) + xlc_investmentneeded_beforeoffset
            xly_offsetneeded = (lowest_before_offset * -1) + xly_investmentneeded_beforeoffset
            xlv_offsetneeded = (lowest_before_offset * -1) + xlv_investmentneeded_beforeoffset
            xlp_offsetneeded = (lowest_before_offset * -1) + xlp_investmentneeded_beforeoffset
            print("XLK Offset Needed:", xlk_offsetneeded)
            print("XLC Offset Needed:", xlc_offsetneeded)
            print("XLY Offset Needed:", xly_offsetneeded)
            print("XLV Offset Needed:", xlv_offsetneeded)
            print("XLP Offset Needed:", xlp_offsetneeded)

            #STEP: Sum the Offset Needed to determine the
            #      minimum investment requirement to achieve the target portfolio weighting.

            investment_needed_for_target = xlk_offsetneeded + xlc_offsetneeded + xly_offsetneeded + xlv_offsetneeded + xlp_offsetneeded

            print("Investment Needed for Target: $", investment_needed_for_target)

            investment_can_achieve_target = "No"

            if investment_needed_for_target <= investment_amount:
                investment_can_achieve_target = "Yes"
            elif investment_needed_for_target > investment_amount:
                investment_can_achieve_target = "No"

            print("Investment Amount:", investment_amount)
            print("Investment Can Reach Target Weighting:", investment_can_achieve_target)

            #Step: If this investment amount can reach the target: Move to Segment 3
            #      If this investment amount can't reach the target: Move to Segment 4
            if investment_can_achieve_target == "Yes":
                xlk_investment = "Move to Segment 3"
                xlc_investment = "Move to Segment 3"
                xly_investment = "Move to Segment 3"
                xlv_investment = "Move to Segment 3"
                xlp_investment = "Move to Segment 3"
            elif is_initial_investment == "No":
                xlk_investment = "Move to Segment 4"
                xlc_investment = "Move to Segment 4"
                xly_investment = "Move to Segment 4"
                xlv_investment = "Move to Segment 4"
                xlp_investment = "Move to Segment 4"




        #SEGMENT 3
        #If the investment is large enough to fully rebalance the portfolio: 
        #The goal of this segment is to calculate how to rebalance the entire portfolio 
        #to achieve the target weighting based on the current equity and the additional investment.
        #STEP: Engage Segment 3
        # Initialize the segment3 variable with a default value
        segment3 = "Off"

        if investment_can_achieve_target == "Yes" and is_initial_investment == "No":
            segment3 = "On"
            print("Segment 3:", segment3)
        elif investment_can_achieve_target == "No" and is_initial_investment == "Yes":
            segment3 = "Off"
            print("Segment 3:", segment3)


        #STEP if segment 3 is engaged, calculate target portfolio equity
        if segment3 == "On":
            xlk_targetequity_includingtotal = xlk_targetweighting * total_portfolio_value
            xlc_targetequity_includingtotal = xlc_targetweighting * total_portfolio_value
            xly_targetequity_includingtotal = xly_targetweighting * total_portfolio_value
            xlv_targetequity_includingtotal = xlv_targetweighting * total_portfolio_value
            xlp_targetequity_includingtotal = xlp_targetweighting * total_portfolio_value
            print("XLK Target Equity Including Total: $", xlk_targetequity_includingtotal)
            print("XLC Target Equity Including Total: $", xlc_targetequity_includingtotal)
            print("XLY Target Equity Including Total: $", xly_targetequity_includingtotal)
            print("XLV Target Equity Including Total: $", xlv_targetequity_includingtotal)
            print("XLP Target Equity Including Total: $", xlp_targetequity_includingtotal)

            #STEP: Target Equity minus Current Equity. Negative values are overweighted.
            xlk_equitydifference = xlk_targetequity_includingtotal - xlk_current_equity
            xlc_equitydifference = xlc_targetequity_includingtotal - xlc_current_equity
            xly_equitydifference = xly_targetequity_includingtotal - xly_current_equity
            xlv_equitydifference = xlv_targetequity_includingtotal - xlv_current_equity
            xlp_equitydifference = xlp_targetequity_includingtotal - xlp_current_equity

            print("XLK Equity Difference = $", xlk_equitydifference)
            print("XLC Equity Difference = $", xlc_equitydifference)
            print("XLY Equity Difference = $", xly_equitydifference)
            print("XLV Equity Difference = $", xlv_equitydifference)
            print("XLP Equity Difference = $", xlp_equitydifference)

            #IMPORTANT# EQUITY DIFFERENCE IS THE ANSWER FOR THIS SEGMENT FOR BUY/SELL ALGORITHM #IMPORTANT#

            #STEP: Convert any positive values into 0
            # initialize variables
            xlk_equitydifference_negsum = xlk_equitydifference
            xlc_equitydifference_negsum = xlc_equitydifference
            xly_equitydifference_negsum = xly_equitydifference
            xlv_equitydifference_negsum = xlv_equitydifference
            xlp_equitydifference_negsum = xlp_equitydifference

            if xlk_equitydifference_negsum > 0:
                xlk_equitydifference_negsum = 0

            if xlc_equitydifference_negsum > 0:
                xlc_equitydifference_negsum = 0

            if xly_equitydifference_negsum > 0:
                xly_equitydifference_negsum = 0

            if xlv_equitydifference_negsum > 0:
                xlv_equitydifference_negsum = 0

            if xlp_equitydifference_negsum > 0:
                xlp_equitydifference_negsum = 0

            #STEP: Sum negative values
            # Initialize the equity_difference_negativesum variable with 0
            equity_difference_negativesum = 0

            # Create a list of the 5 variables
            equity_differences = [xlk_equitydifference, xlc_equitydifference, xly_equitydifference, xlv_equitydifference, xlp_equitydifference]

            # Iterate through the list and sum the negative values
            for equity_difference in equity_differences:
                if equity_difference < 0:
                    equity_difference_negativesum += equity_difference

            # Print the result
            print("Equity Difference Negative Sum:", equity_difference_negativesum)



            #STEP: Count positive number of stocks:
            # Initialize the underweighted_stocks variable with 0
            underweighted_stocks = 0

            # Iterate through the list and count the number of elements that have values greater than or equal to 0
            for equity_difference in equity_differences:
                if equity_difference >= 0:
                    underweighted_stocks += 1

            # Print the result
            print("Underweighted Stocks:", underweighted_stocks)



            #STEP: Divide the equity difference negative sum by the number of underweighted stocks
            #      This gives a value to subtract from all stocks to equal the Investment amount

            subtract_from_underweighted = equity_difference_negativesum / underweighted_stocks
            #print("Subtract From Underweighted Stocks: $", subtract_from_underweighted)


            #STEP: Subtract the subtract_from_underweighted from each stock target equity difference
            #      IF the negsum = 0. This results in the investment amount offset by the overweighted stocks.
            if xlk_equitydifference_negsum == 0:
                xlk_investment = xlk_equitydifference + subtract_from_underweighted
            elif xlk_equitydifference_negsum <0:
                xlk_investment = 0

            if xlc_equitydifference_negsum == 0:
                xlc_investment = xlc_equitydifference + subtract_from_underweighted
            elif xlc_equitydifference_negsum < 0:
                xlc_investment = 0

            if xly_equitydifference_negsum == 0:
                xly_investment = xly_equitydifference + subtract_from_underweighted
            elif xly_equitydifference_negsum < 0:
                xly_investment = 0

            if xlv_equitydifference_negsum == 0:
                xlv_investment = xlv_equitydifference + subtract_from_underweighted
            elif xlv_equitydifference_negsum < 0:
                xlv_investment = 0

            if xlp_equitydifference_negsum == 0:
                xlp_investment = xlp_equitydifference + subtract_from_underweighted
            elif xlp_equitydifference_negsum < 0:
                xlp_investment = 0



        #SEGMENT 4 - SELL TO ACHIEVE WEIGHTING
        # If the investment is not large enough to fully rebalance the portfolio, and
        # the portfolio is outside of 3% weighting, this segment will sell stocks to achieve target weighting
        # Intitialize segment4 variable with a default value
        segment4 = "Off"

        print("Segment 4:", segment4)
        
        if xlk_weighting_difference >= 0.03 or xlk_weighting_difference <= -0.03:
            segment4 = "On"

        if xlc_weighting_difference >= 0.03 or xlc_weighting_difference <= -0.03:
            segment4 = "On"

        if xly_weighting_difference >= 0.03 or xly_weighting_difference <= -0.03:
            segment4 = "On"

        if xlv_weighting_difference >= 0.03 or xlv_weighting_difference <= -0.03:
            segment4 = "On"

        if xlp_weighting_difference >= 0.03 or xlp_weighting_difference <= -0.03:
            segment4 = "On"

        if investment_can_achieve_target == "Yes" or is_initial_investment == "Yes":
            segment4 = "Off"
        
        if segment4 == "On":
            xlk_targetequity_includingtotal = xlk_targetweighting * total_portfolio_value
            xlc_targetequity_includingtotal = xlc_targetweighting * total_portfolio_value
            xly_targetequity_includingtotal = xly_targetweighting * total_portfolio_value
            xlv_targetequity_includingtotal = xlv_targetweighting * total_portfolio_value
            xlp_targetequity_includingtotal = xlp_targetweighting * total_portfolio_value
            print("XLK Target Equity Including Total: $", xlk_targetequity_includingtotal)
            print("XLC Target Equity Including Total: $", xlc_targetequity_includingtotal)
            print("XLY Target Equity Including Total: $", xly_targetequity_includingtotal)
            print("XLV Target Equity Including Total: $", xlv_targetequity_includingtotal)
            print("XLP Target Equity Including Total: $", xlp_targetequity_includingtotal)

            #STEP: Target Equity minus Current Equity. Negative values are overweighted.
            xlk_equitydifference = xlk_targetequity_includingtotal - xlk_current_equity
            xlc_equitydifference = xlc_targetequity_includingtotal - xlc_current_equity
            xly_equitydifference = xly_targetequity_includingtotal - xly_current_equity
            xlv_equitydifference = xlv_targetequity_includingtotal - xlv_current_equity
            xlp_equitydifference = xlp_targetequity_includingtotal - xlp_current_equity

            print("XLK Equity Difference = $", xlk_equitydifference)
            print("XLC Equity Difference = $", xlc_equitydifference)
            print("XLY Equity Difference = $", xly_equitydifference)
            print("XLV Equity Difference = $", xlv_equitydifference)
            print("XLP Equity Difference = $", xlp_equitydifference)

            #IMPORTANT# EQUITY DIFFERENCE IS THE ANSWER FOR THIS SEGMENT FOR BUY/SELL ALGORITHM #IMPORTANT#

            xlk_investment = xlk_equitydifference
            xlc_investment = xlc_equitydifference
            xly_investment = xly_equitydifference
            xlv_investment = xlv_equitydifference
            xlp_investment = xlp_equitydifference

        #if segment4 == "On":
         #   xlk_investment = xlk_targetequity_includingtotal - xlk_current_equity
          #  xlc_investment = xlc_targetequity_includingtotal - xlc_current_equity
           # xly_investment = xly_targetequity_includingtotal - xly_current_equity
           # xlv_investment = xlv_targetequity_includingtotal - xlv_current_equity
            #xlp_investment = xlp_targetequity_includingtotal - xlp_current_equity





        #Segment 5 - CHAT GPT PROPORTIONAL OFFSET
        #The investment is not large enough to fully rebalance the portfolio. 
        # The goal of this segment is to get the current weighting as close to the 
        # target weighting as possible after the investment using the current investment.
        # Initialize the segment5 variable with a default value
        segment5 = "Off"

        if investment_can_achieve_target == "Yes" and is_initial_investment == "Yes":
            segment5 = "Off"
        elif investment_can_achieve_target == "No" and is_initial_investment == "No":
            segment5 = "On"
        
        if segment4 == "On":
            segment5 = "Off"

        print("Segment 5:", segment5)

        if segment5 == "On":
            # Calculate shortfall for each equity
            xlk_shortfall = max(xlk_targetequity_beforeoffset - xlk_current_equity, 0)
            xlc_shortfall = max(xlc_targetequity_beforeoffset - xlc_current_equity, 0)
            xly_shortfall = max(xly_targetequity_beforeoffset - xly_current_equity, 0)
            xlv_shortfall = max(xlv_targetequity_beforeoffset - xlv_current_equity, 0)
            xlp_shortfall = max(xlp_targetequity_beforeoffset - xlp_current_equity, 0)

            # Calculate total shortfall
            total_shortfall = xlk_shortfall + xlc_shortfall + xly_shortfall + xlv_shortfall + xlp_shortfall

            # Calculate proportional difference for each equity
            xlk_proportional_difference = xlk_shortfall / total_shortfall if total_shortfall > 0 else 0
            xlc_proportional_difference = xlc_shortfall / total_shortfall if total_shortfall > 0 else 0
            xly_proportional_difference = xly_shortfall / total_shortfall if total_shortfall > 0 else 0
            xlv_proportional_difference = xlv_shortfall / total_shortfall if total_shortfall > 0 else 0
            xlp_proportional_difference = xlp_shortfall / total_shortfall if total_shortfall > 0 else 0

            # Allocate the investment
            xlk_investment = xlk_proportional_difference * investment_amount
            xlc_investment = xlc_proportional_difference * investment_amount
            xly_investment = xly_proportional_difference * investment_amount
            xlv_investment = xlv_proportional_difference * investment_amount
            xlp_investment = xlp_proportional_difference * investment_amount

        xlk_action = "Buy" if xlk_investment > 0 else "Sell" if xlk_investment < 0 else ""
        xlc_action = "Buy" if xlc_investment > 0 else "Sell" if xlc_investment < 0 else ""
        xly_action = "Buy" if xly_investment > 0 else "Sell" if xly_investment < 0 else ""
        xlv_action = "Buy" if xlv_investment > 0 else "Sell" if xlv_investment < 0 else ""
        xlp_action = "Buy" if xlp_investment > 0 else "Sell" if xlp_investment < 0 else ""

        # Convert floating-point numbers to integers
        investment_amount = int(investment_amount)
        xlk_current_equity = int(xlk_current_equity)
        xlc_current_equity = int(xlc_current_equity)
        xly_current_equity = int(xly_current_equity)
        xlv_current_equity = int(xlv_current_equity)
        xlp_current_equity = int(xlp_current_equity)

        return render_template('calculator.html', 
                       xlk_investment=xlk_investment, xlk_action=xlk_action,
                       xlc_investment=xlc_investment, xlc_action=xlc_action,
                       xly_investment=xly_investment, xly_action=xly_action,
                       xlv_investment=xlv_investment, xlv_action=xlv_action,
                       xlp_investment=xlp_investment, xlp_action=xlp_action,
                       investmentAmount=investment_amount, 
                       equityXLK=xlk_current_equity,
                       equityXLC=xlc_current_equity,
                       equityXLY=xly_current_equity,
                       equityXLV=xlv_current_equity,
                       equityXLP=xlp_current_equity)


    return render_template('calculator.html', xlk_investment=0, xlc_investment=0, xly_investment=0, xlv_investment=0, xlp_investment=0, xlk_action="", xlc_action="", xly_action="", xlv_action="", xlp_action="")


if __name__ == '__main__':
    app.run(debug=False)