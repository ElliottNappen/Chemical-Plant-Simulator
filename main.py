
from drafter import *
from dataclasses import dataclass


# -----------------------------------------
# DATACLASSES
# -----------------------------------------

@dataclass
class Reactor:
    temperature: float
    production_rate: float
    is_operating: bool


@dataclass
class PlantState:
    plant_name: str
    money: float
    raw_materials: int
    total_production: int
    safety_score: int
    reactors: list[Reactor]
    selected_product: str
    total_revenue: float
    total_expenses: float
    turn_number: int


# Starting values for a new game
STARTING_STATE = PlantState(
    "",
    1000.0,
    100,
    0,
    100,
    [Reactor(300.0, 50.0, True)],
    "Ammonia",
    0.0,
    0.0,
    0
)


# -----------------------------------------
# HELPER FUNCTIONS
# -----------------------------------------

def game_is_over(state: PlantState) -> bool:
    """Check whether the player has lost the game."""

    if state.safety_score <= 20:
        return True

    if state.money <= 0 and state.raw_materials <= 0:
        return True

    return False


def navigation_buttons() -> list:
    """Create the navigation buttons used throughout the site."""

    return [
        Button("Dashboard", "plant_dashboard"),
        Button("Reactor Management", "reactor_management"),
        Button("Resources", "resource_management"),
        Button("Production Report", "production_report"),
        Button("Safety Report", "safety_report"),
        Button("Financial Report", "financial_report")
    ]


def check_game(state: PlantState):
    """Send the player to the game over page if necessary."""

    if game_is_over(state):
        return game_over(state)

    return plant_dashboard(state)


# -----------------------------------------
# ROUTE 1: HOME PAGE
# -----------------------------------------

@route
def index(state: PlantState) -> Page:
    """Display the introduction to the chemical plant simulator."""

    return Page(state, [
        Header("CHEMICAL PLANT SIMULATOR"),
        "Welcome to your chemical engineering career!",
        " ",
        "Your goal is to operate a chemical plant successfully.",
        "Produce products, manage your money, and keep your",
        "reactors operating safely.",
        " ",
        "WARNING: Operating reactors at unsafe temperatures",
        "can reduce your safety score.",
        " ",
        Button("Start New Game", "new_game")
    ])


# -----------------------------------------
# ROUTE 2: NEW GAME
# -----------------------------------------

@route
def new_game(state: PlantState) -> Page:
    """Ask the player to name their chemical plant."""

    return Page(state, [
        Header("NEW GAME"),
        "Choose a name for your chemical plant.",
        TextBox("plant_name", "My Chemical Plant"),
        " ",
        Button("Start Operating", "start_game")
    ])


# -----------------------------------------
# ROUTE 3: START GAME
# -----------------------------------------

@route
def start_game(state: PlantState, plant_name: str) -> Page:
    """Reset the game and save the player's plant name."""

    state.plant_name = plant_name

    if state.plant_name.strip() == "":
        state.plant_name = "Unnamed Chemical Plant"

    state.money = 1000.0
    state.raw_materials = 100
    state.total_production = 0
    state.safety_score = 100
    state.reactors = [Reactor(300.0, 50.0, True)]
    state.selected_product = "Ammonia"
    state.total_revenue = 0.0
    state.total_expenses = 0.0
    state.turn_number = 0

    return plant_dashboard(state)


# -----------------------------------------
# ROUTE 4: PLANT DASHBOARD
# -----------------------------------------

@route
def plant_dashboard(state: PlantState) -> Page:
    """Display the current condition of the chemical plant."""

    if game_is_over(state):
        return game_over(state)

    return Page(state, [
        Header(state.plant_name),
        Header("PLANT DASHBOARD"),
        "Production Shift: " + str(state.turn_number),
        " ",
        "Available Money: $" + str(round(state.money, 2)),
        "Raw Materials: " + str(state.raw_materials),
        "Total Production: " + str(state.total_production),
        "Safety Score: " + str(state.safety_score) + "/100",
        " ",
        "Current Product: " + state.selected_product,
        "Number of Reactors: " + str(len(state.reactors)),
        " ",
        *navigation_buttons(),
        " ",
        Button("Run Next Production Shift", "run_production")
    ])


# -----------------------------------------
# ROUTE 5: REACTOR MANAGEMENT
# -----------------------------------------

@route
def reactor_management(state: PlantState) -> Page:
    """Allow the player to adjust reactor settings."""

    reactor = state.reactors[0]

    return Page(state, [
        Header("REACTOR MANAGEMENT"),
        "Adjust the operating conditions of your reactor.",
        " ",
        "Current Temperature: " + str(reactor.temperature),
        "Current Production Rate: " + str(reactor.production_rate),
        "Currently Operating: " + str(reactor.is_operating),
        " ",
        "Choose a product:",
        SelectBox(
            "product_type",
            ["Ammonia", "Fertilizer", "Polymer"],
            state.selected_product
        ),
        " ",
        "Set Reactor Temperature (100-700 Celsius):",
        TextBox("temperature", reactor.temperature),
        " ",
        "Set Production Rate (1-100):",
        TextBox("production_rate", reactor.production_rate),
        " ",
        Button("Save Reactor Settings", "update_reactor"),
        Button("Start / Stop Reactor", "toggle_reactor"),
        " ",
        *navigation_buttons()
    ])


# -----------------------------------------
# ROUTE 6: UPDATE REACTOR
# -----------------------------------------

@route
def update_reactor(
    state: PlantState,
    product_type: str,
    temperature: float,
    production_rate: float
) -> Page:
    """Save the new reactor settings after checking the inputs."""

    if temperature < 100 or temperature > 700:
        return Page(state, [
            Header("INVALID TEMPERATURE"),
            "Temperature must be between 100 and 700 Celsius.",
            Button("Try Again", "reactor_management")
        ])

    if production_rate < 1 or production_rate > 100:
        return Page(state, [
            Header("INVALID PRODUCTION RATE"),
            "Production rate must be between 1 and 100.",
            Button("Try Again", "reactor_management")
        ])

    if product_type not in ["Ammonia", "Fertilizer", "Polymer"]:
        return reactor_management(state)

    state.selected_product = product_type

    for reactor in state.reactors:
        reactor.temperature = temperature
        reactor.production_rate = production_rate

    return reactor_management(state)


# -----------------------------------------
# ROUTE 7: TOGGLE REACTOR
# -----------------------------------------

@route
def toggle_reactor(state: PlantState) -> Page:
    """Turn the reactors on or off."""

    for reactor in state.reactors:
        reactor.is_operating = not reactor.is_operating

    return reactor_management(state)


# -----------------------------------------
# ROUTE 8: RESOURCE MANAGEMENT
# -----------------------------------------

@route
def resource_management(state: PlantState) -> Page:
    """Display available materials and allow purchases."""

    return Page(state, [
        Header("RESOURCE MANAGEMENT"),
        "Available Raw Materials: " + str(state.raw_materials),
        " ",
        "Purchase additional raw materials.",
        "Each unit costs $100.",
        " ",
        "Enter the amount you wish to purchase:",
        TextBox("quantity", 25),
        " ",
        Button("Purchase Materials", "buy_materials"),
        " ",
        *navigation_buttons()
    ])


# -----------------------------------------
# ROUTE 9: BUY MATERIALS
# -----------------------------------------

@route
def buy_materials(state: PlantState, quantity: int) -> Page:
    """Purchase raw materials using the plant's available money."""

    if quantity <= 0:
        return Page(state, [
            Header("INVALID PURCHASE"),
            "Enter a quantity greater than zero.",
            Button("Return to Resources", "resource_management")
        ])

    cost = quantity * 100

    if cost > state.money:
        return Page(state, [
            Header("INSUFFICIENT FUNDS"),
            "You do not have enough money for this purchase.",
            "Available Money: $" + str(round(state.money, 2)),
            "Purchase Cost: $" + str(cost),
            Button("Try Again", "resource_management")
        ])

    state.money = state.money - cost
    state.raw_materials = state.raw_materials + quantity
    state.total_expenses = state.total_expenses + cost

    return Page(state, [
        Header("PURCHASE SUCCESSFUL"),
        "You purchased " + str(quantity) + " units of raw materials.",
        "Remaining Money: $" + str(round(state.money, 2)),
        "Available Materials: " + str(state.raw_materials),
        Button("Return to Resources", "resource_management"),
        Button("Dashboard", "plant_dashboard")
    ])


# -----------------------------------------
# ROUTE 10: RUN PRODUCTION
# -----------------------------------------

@route
def run_production(state: PlantState) -> Page:
    """Run one production shift and calculate its results."""

    if game_is_over(state):
        return game_over(state)

    product_prices = {
        "Ammonia": 40,
        "Fertilizer": 50,
        "Polymer": 60
    }

    shift_production = 0
    shift_revenue = 0.0
    shift_expenses = 0.0

    # Process every reactor in the plant.
    for reactor in state.reactors:

        if reactor.is_operating:

            # Check if enough materials are available.
            possible_production = int(reactor.production_rate / 5)

            if state.raw_materials < possible_production * 2:
                possible_production = state.raw_materials // 2

            if possible_production <= 0:
                reactor.is_operating = False

            else:
                materials_used = possible_production * 2

                state.raw_materials = (
                    state.raw_materials - materials_used
                )

                shift_production = (
                    shift_production + possible_production
                )

                # Calculate revenue and operating costs.
                revenue = (
                    possible_production *
                    product_prices[state.selected_product]
                )

                expenses = 100 + possible_production * 5

                shift_revenue = shift_revenue + revenue
                shift_expenses = shift_expenses + expenses

            # Check the safety of the reactor.
            if reactor.temperature > 450 or reactor.temperature < 150:
                state.safety_score = state.safety_score - 15

            elif reactor.temperature > 400 or reactor.temperature < 200:
                state.safety_score = state.safety_score - 5

            else:
                if state.safety_score < 100:
                    state.safety_score = state.safety_score + 1

    # Update the plant's financial and production records.
    state.total_production = (
        state.total_production + shift_production
    )

    state.total_revenue = state.total_revenue + shift_revenue
    state.total_expenses = state.total_expenses + shift_expenses

    state.money = (
        state.money + shift_revenue - shift_expenses
    )

    state.turn_number = state.turn_number + 1

    if state.safety_score < 20:
        state.safety_score = 20

    if game_is_over(state):
        return game_over(state)

    return Page(state, [
        Header("PRODUCTION SHIFT COMPLETE"),
        "Shift Number: " + str(state.turn_number),
        " ",
        "Product Manufactured: " + state.selected_product,
        "Units Produced: " + str(shift_production),
        "Revenue Earned: $" + str(round(shift_revenue, 2)),
        "Operating Expenses: $" + str(round(shift_expenses, 2)),
        " ",
        "Remaining Materials: " + str(state.raw_materials),
        "Current Money: $" + str(round(state.money, 2)),
        "Safety Score: " + str(state.safety_score),
        " ",
        Button("Continue", "plant_dashboard"),
        Button("View Production Report", "production_report")
    ])


# -----------------------------------------
# ROUTE 11: PRODUCTION REPORT
# -----------------------------------------

@route
def production_report(state: PlantState) -> Page:
    """Display the plant's production statistics."""

    return Page(state, [
        Header("PRODUCTION REPORT"),
        "Production Shift: " + str(state.turn_number),
        "Selected Product: " + state.selected_product,
        "Total Units Manufactured: " + str(state.total_production),
        "Remaining Raw Materials: " + str(state.raw_materials),
        " ",
        "Total Revenue: $" + str(round(state.total_revenue, 2)),
        "Total Expenses: $" + str(round(state.total_expenses, 2)),
        " ",
        *navigation_buttons(),
        Button("Run Next Production Shift", "run_production")
    ])


# -----------------------------------------
# ROUTE 12: SAFETY REPORT
# -----------------------------------------

@route
def safety_report(state: PlantState) -> Page:
    """Display the plant's current safety condition."""

    safety_message = "Plant operating within safe limits."

    if state.safety_score < 75:
        safety_message = "WARNING: Plant safety is declining!"

    if state.safety_score < 40:
        safety_message = "DANGER: Critical safety conditions!"

    if state.safety_score <= 20:
        safety_message = "CRITICAL FAILURE: Plant has shut down."

    return Page(state, [
        Header("SAFETY REPORT"),
        "Current Safety Score: " + str(state.safety_score) + "/100",
        " ",
        safety_message,
        " ",
        "Recommended Reactor Temperature: 200-400 Celsius.",
        "Avoid extreme temperatures to protect the plant.",
        " ",
        *navigation_buttons()
    ])


# -----------------------------------------
# ROUTE 13: FINANCIAL REPORT
# -----------------------------------------

@route
def financial_report(state: PlantState) -> Page:
    """Display the plant's financial performance."""

    profit = state.total_revenue - state.total_expenses

    return Page(state, [
        Header("FINANCIAL REPORT"),
        "Available Money: $" + str(round(state.money, 2)),
        "Total Revenue: $" + str(round(state.total_revenue, 2)),
        "Total Expenses: $" + str(round(state.total_expenses, 2)),
        " ",
        "Net Profit/Loss: $" + str(round(profit, 2)),
        " ",
        *navigation_buttons()
    ])


# -----------------------------------------
# ROUTE 14: GAME OVER
# -----------------------------------------

@route
def game_over(state: PlantState) -> Page:
    """Display the final results when the player loses."""

    reason = "The plant has run out of money and materials."

    if state.safety_score <= 20:
        reason = "The plant experienced a critical safety failure."

    return Page(state, [
        Header("GAME OVER"),
        "Plant: " + state.plant_name,
        " ",
        reason,
        " ",
        Header("FINAL STATISTICS"),
        "Total Production: " + str(state.total_production),
        "Total Revenue: $" + str(round(state.total_revenue, 2)),
        "Total Expenses: $" + str(round(state.total_expenses, 2)),
        "Final Money: $" + str(round(state.money, 2)),
        "Final Safety Score: " + str(state.safety_score),
        "Production Shifts: " + str(state.turn_number),
        " ",
        Button("Play Again", "new_game"),
        Button("Home", "index")
    ])

set_website_title("Chemical Plant Simulator")

set_site_information(
    "Your Name",
    "A chemical plant management and engineering simulator.",
    "Created using Python and the Drafter library.",
    "See the project planning document in the GitHub repository.",
    []
)
hide_debug_information()
set_website_framed(False)
start_server(STARTING_STATE)

