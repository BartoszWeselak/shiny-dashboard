from shiny import App, render, ui, reactive
import shinyswatch



app_ui = ui.page_fluid(

    ui.page_navbar(
        ui.nav_panel(ui.div( shinyswatch.theme_picker_ui(), style="text-align: center;")),
        title="DepositPol",
        id="page",
    ),

    ui.div(
    ui.h2("Interest Calculation Dashboard", style="text-align: center; margin-bottom: 30px;"),
    ui.panel_well(
        ui.row(
            ui.column(4, ui.input_numeric("deposit", "Deposit:", 0, width="100%")),
            ui.column(4, ui.input_numeric("intrest", "Interest Rate (%):", 0, width="100%")),
            ui.column(4, ui.input_numeric("period", "Period (Months):", 0, width="100%")),
        ),
        ui.input_action_button("calc_button", "Calculate", style="margin-top: 20px; width: 100%;"),
        ui.row(
          ui.h3("Calculation Results", style="margin-top: 20px; text-align: center;"),
          ui.output_text_verbatim("profit", placeholder=True),
          ui.output_text_verbatim("tax", placeholder=True),
          ui.output_text_verbatim("sum_after_tax", placeholder=True),
        )
    ),
    ),
    theme=shinyswatch.theme.cosmo()
    )


def server(input, output, session):
    shinyswatch.theme_picker_server()

    @output
    @render.text
    @reactive.event(input.calc_button)
    def sum_after_tax():
        profit=calc_profit( input.deposit(),(input.intrest() / 100),input.period())
        tax=calc_tax(profit, input.deposit())
        return profit-tax

    @output
    @render.text
    @reactive.event(input.calc_button)
    def tax():
        profit=calc_profit(input.deposit(), (input.intrest() / 100), input.period())
        return calc_tax(profit, input.deposit())

    @output
    @render.text
    @reactive.event(input.calc_button)
    def profit():
        return calc_profit( input.deposit(),(input.intrest() / 100),input.period())

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
