from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.page_navbar(
        ui.nav_panel("A", "Page A content"),
        ui.nav_panel("B", "Page B content"),
        ui.nav_panel("C", "Page C content"),
        title="App with navbar",
        id="page",
    ),


    ui.h2("Interest Calculation Dashboard", style="text-align: center; margin-bottom: 30px;"),

    ui.panel_well(
        ui.row(
            ui.column(4, ui.input_numeric("num1", "Deposit:", 0, width="100%")),
            ui.column(4, ui.input_numeric("num2", "Interest Rate (%):", 0, width="100%")),
            ui.column(4, ui.input_numeric("num3", "Period (Months):", 0, width="100%")),
        ),
        ui.input_action_button("calc_button", "Calculate", style="margin-top: 20px; width: 100%;"),
        ui.row(
          ui.h3("Calculation Results", style="margin-top: 20px; text-align: center;"),
          ui.output_text_verbatim("result", placeholder=True),
        )
    ),
    ui.panel_well(
       ui.row(
           ui.p("test"),
           ui.p("test"),
           ui.p("test"),

       ),
        ),
    )


def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.calc_button)
    def result():
        deposit = input.num1()
        interest_rate = input.num2() / 100
        period_months = input.num3()
        capitalization = 12
        period_years = period_months / 12
        profit = deposit * (1 + (interest_rate / capitalization)) ** (capitalization * period_years)
        tax = calc_tax(deposit, profit)
        sum_after_tax = profit - tax
        return f"Profit: {profit:.2f}\nTax: {tax:.2f}\nSum After Tax (19%): {sum_after_tax:.2f}"

    def calc_tax(deposit, profit):
        tax = (profit - deposit) * 0.19
        return tax


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
