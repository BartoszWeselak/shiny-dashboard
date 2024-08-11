from shiny import App, render, ui, reactive

# Definiujemy interfejs użytkownika
app_ui = ui.page_fluid(

    ui.input_numeric("num1", "Deposit:",0),

    ui.input_numeric("num2", "interest rate(%):",0),

    ui.input_numeric("num3", "period(months:",0),

    ui.input_action_button("calc_button", "Calculate"),
    ui.output_text_verbatim("result"),
    ui.output_text_verbatim("test"),

)

# Definiujemy funkcje serwera
def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.calc_button)  # Zdarzenie aktywujące renderowanie
    def result():
        deposit = input.num1()
        interest_rate = input.num2() / 100
        period_months = input.num3()
        capitalization = 12
        period_years = period_months / 12
        sum_result = deposit * (1 + (interest_rate / capitalization)) ** (capitalization * period_years)

        return f"Result: {sum_result}"

    @output
    @render.text
    def test():
        return "test"
app = App(app_ui, server)
if __name__ == "__main__":
    app.run()
