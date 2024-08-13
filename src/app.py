from shiny import App, render, ui, reactive
import shinyswatch
import matplotlib.pyplot as plt



app_ui = ui.page_fluid(
    ui.include_css("styles.css"),
    ui.page_navbar(
        ui.nav_panel(ui.div( shinyswatch.theme_picker_ui(), style="text-align: center;text-decoration:none")),
        title="DepositPol",
        id="page",

    ),

    ui.div(
    ui.h2("Interest Calculation Dashboard", style="text-align: center; margin-bottom: 30px;"),
    ui.panel_well(
        ui.row(
            ui.column(4, ui.input_numeric("deposit", "Deposit:", 0, width="100%")),
            ui.column(4, ui.input_numeric("interest", "Interest Rate (%):", 0, width="100%")),
            ui.column(4, ui.input_numeric("period", "Period (Months):", 0, width="100%")),
        ),
        ui.input_action_button("calc_button", "Calculate", style="margin-top: 20px; width: 100%;"),

          ui.h3("Calculation Results", style="margin-top: 20px; text-align: center;"),
    ui.layout_columns(
        ui.card(
            ui.h3("Profit"),
            ui.output_text_verbatim("profit", placeholder=True),
        ),
        ui.card(
            ui.h3("Tax"),
            ui.output_text_verbatim("tax", placeholder=True),
        ),
        ui.card(
            ui.h3("After Tax"),
            ui.output_text_verbatim("sum_after_tax", placeholder=True),
        ),
        ),

        ui.output_plot("plot"),
    ),
    style="text-align: center;width:80%;margin-left:10%;"
    ),
    theme=shinyswatch.theme.cosmo(),

    )


def server(input, output, session):
    shinyswatch.theme_picker_server()

    @output
    @render.text
    @reactive.event(input.calc_button)
    def sum_after_tax():
        profit=calc_profit( input.deposit(),(input.interest() / 100),input.period())
        tax=calc_tax(profit, input.deposit())
        return profit-tax

    @output
    @render.text
    @reactive.event(input.calc_button)
    def tax():
        profit=calc_profit(input.deposit(), (input.interest() / 100), input.period())
        return calc_tax(profit, input.deposit())

    @output
    @render.text
    @reactive.event(input.calc_button)
    def profit():
        return calc_profit( input.deposit(),(input.interest() / 100),input.period())

    @render.plot(alt="A histogram")
    @reactive.event(input.calc_button)
    def plot():
        deposit = input.deposit()
        interest_rate = input.interest() / 100
        period = input.period()

        # profit = calc_profit(deposit, interest_rate, period)
        # tax = calc_tax(profit, deposit)
        # after_tax = profit - tax
        print(deposit)
        categories = ['Deposit', 'Profit', 'Tax', 'After Tax']
        values = [0, 0, 0, 0]

        fig, ax = plt.subplots()
        ax.bar(categories, values)

        ax.set_xlabel('Category')
        ax.set_ylabel('Value($)')
        ax.set_title('Value distribution')


        return fig
def create_plot():
    x = ['A', 'B', 'C']
    y = [10, 20, 15]

    fig, ax = plt.subplots()
    ax.bar(x, y)

    ax.set_xlabel('Category')
    ax.set_ylabel('Value($)')
    ax.set_title('Value distribution')
    return fig

def calc_profit(deposit, interest_rate,period_months):
    capitalization = 12
    period_years = period_months / 12
    profit = deposit * (1 + (interest_rate / capitalization)) ** (capitalization * period_years)
    return profit
def calc_tax(profit,deposit):
    tax = (profit - deposit) * 0.19
    return tax

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
