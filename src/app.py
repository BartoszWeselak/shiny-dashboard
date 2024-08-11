from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.head_content(
        ui.tags.link(
            rel="stylesheet", href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
        )
    ),
    ui.tags.div(
        ui.h2("Hello, Shiny for Python!", class_="text-xl bg-gray-200 text-center my-4")
    ),
    ui.tags.div(
        ui.input_slider("n", "Number of bins", 10, 100, 20)
    ),
    ui.tags.div(
        ui.p("text")
    )
)

def server(input, output, session):
    @output
    @render.text
    def text():
        return f"Number of bins selected: {input.n()}"

app = App(app_ui, server)

if __name__ == "__main__":
    app.run()

