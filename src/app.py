from shiny import App, render, ui, reactive
import shinyswatch
import matplotlib.pyplot as plt

currency = ""
tax_rate = 0
tax_rates = [
    ["PL", 0.19, "zł"],
    ["USA", 0.24, "USD"],
    ["FR", 0.30, "EUR"],
    ["GER", 0.26, "EUR"],
]
app_ui = ui.page_fluid(
    ui.include_css("styles.css"),
    ui.page_navbar(
        ui.nav_panel(
            shinyswatch.theme_picker_ui(),
        ),
        title="DepositPol",
        id="page",
    ),
    ui.div(
        ui.input_select(
            "country",
            "Choose currency:",
            {
                "dolar": {"USA": "United States"},
                "euro": {"GER": "Germany", "FR": "France"},
                "złoty": {"PL": "Poland"},
            },
        ),
        ui.output_text("set_country"),
        ui.panel_well(
            ui.h2(
                "Interest Calculation Dashboard",
                style="text-align: center; margin-bottom: 30px;",
            ),
        ),
        ui.panel_well(
            ui.layout_columns(
                ui.card(
                    ui.h3(f"Deposit"),
                    ui.input_numeric("deposit", "Deposit:", 0, width="100%"),
                ),
                ui.card(
                    ui.h3("Interest(%)"),
                    ui.input_numeric("interest", "Interest Rate (%):", 0, width="100%"),
                ),
                ui.card(
                    ui.h3("Period(months)"),
                    ui.input_numeric("period", "Period (Months):", 0, width="100%"),
                ),
            ),
            ui.input_action_button(
                "calc_button", "Calculate", style="margin-top: 20px; width: 30%;"
            ),
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
        style="text-align: center;width:80%;margin-left:10%;",
    ),
    theme=shinyswatch.theme.flatly(),
)


def server(input, output, session):
    shinyswatch.theme_picker_server()

    @render.text
    @reactive.event(input.country)
    def set_country():
        global tax_rate, currency
        country = str(input.country())
        for i in tax_rates:
            if i[0] == country:
                tax_rate = i[1]
                currency = i[2]

        return "You choose: " + country

    @output
    @render.text
    @reactive.event(input.calc_button)
    def sum_after_tax():
        profit = calc_profit(input.deposit(), (input.interest() / 100), input.period())
        tax = calc_tax(profit, input.deposit())
        return f"{(profit - tax):.2f} {currency}"

    @output
    @render.text
    @reactive.event(input.calc_button)
    def tax():
        profit = calc_profit(input.deposit(), (input.interest() / 100), input.period())
        return f"{calc_tax(profit, input.deposit()):.2f} {currency}"

    @output
    @render.text
    @reactive.event(input.calc_button)
    def profit():
        return f"{calc_profit(input.deposit(), (input.interest() / 100), input.period()):.2f} {currency}"

    @render.plot(alt="A histogram")
    @reactive.event(input.calc_button)
    def plot():
        deposit = input.deposit()
        interest_rate = input.interest() / 100
        period = input.period()

        profit = calc_profit(deposit, interest_rate, period)
        tax = calc_tax(profit, deposit)
        after_tax = profit - tax

        categories = ["Deposit", "Profit", "Tax", "After Tax"]
        values = [deposit, profit, tax, after_tax]

        fig, ax = plt.subplots()

        bars = ax.bar(categories, values, color=["blue", "green", "red", "orange"])

        for b in bars:
            height = b.get_height()
            ax.text(
                b.get_x() + b.get_width() / 2,
                height,
                f"{height:.2f} {currency}",
                ha="center",
                va="bottom",
            )

        ax.set_xlabel("Category")
        ax.set_ylabel(f"Value ({currency})")
        ax.set_title("Value Distribution")
        return fig

    @render.image
    def icon():
        img = {"src": "calculator.png", "width": "10%"}
        return img


def calc_profit(deposit, interest_rate, period_months):
    capitalization = 12
    period_years = period_months / 12
    profit = deposit * (1 + (interest_rate / capitalization)) ** (
        capitalization * period_years
    )
    return profit


def calc_tax(profit, deposit):
    tax = (profit - deposit) * tax_rate
    return tax


def change_currency(new_currency, new_tax_rate):
    global tax_rate, currency
    tax_rate = new_tax_rate
    currency = new_currency


app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
