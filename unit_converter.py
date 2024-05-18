import zmq

si_units = {
    'G': 10 ** 9,
    'M': 10 ** 6,
    'k': 10 ** 3,
    'h': 10 ** 2,
    'da': 10 ** 1,
    'g': 10 ** 0,
    'd': 10 ** -1,
    'c': 10 ** -2,
    'm': 10 ** -3,
    'micro': 10 ** -6,
    'n': 10 ** -9,
    'moles': 1
}


def obtain_grams(number, unit):  # Converts unit to grams (or returns the number if grams was provided)
    """Converts a measurement to grams."""
    if unit in si_units.keys():
        return number * si_units[unit]
    else:
        raise KeyError(
            'The unit you provided is not supported. The following units are supported: "G" (giga) | "M" (mega)'
            ' | "k" (kilo) | "h" (hecto) | "da" (deka) | "d" (deci) | "c" (centi) | "m" (milli) | '
            '"micro" (micro) | "n" (nano)')


def unit_converter():
    """Stoichiometry converter that converts from grams to moles or converts from moles to grams depending on user
        request."""

    context = zmq.Context()
    socket = context.socket(zmq.REP)  # Socket for sending responses
    socket.bind("tcp://*:5555")  # Bind to port 5555

    while True:
        # Wait for next request from client
        request = socket.recv_json()

        # client sends conversion, mass, unit, molar_mass in json
        conversion = request["conversion"]
        mass_value = request["mass"]
        unit = request["unit"]
        molar_mass = request["molar_mass"]

        try:
            molar_mass = float(molar_mass)
            mass_in_grams = obtain_grams(mass_value, unit)  # convert the mass to grams if necessary
            if conversion == "grams_to_moles":  # Calculation for converting grams to moles
                amount = mass_in_grams / molar_mass
                unit = "moles"

            elif conversion == "moles_to_grams":  # Calculation for converting moles to grams
                amount = mass_value * molar_mass
                unit = "grams"
            else:
                raise ValueError("The conversion type you provided is not supported.")
            response = f'The converted amount is {amount} {unit}.'  # Compile response to be sent
        except Exception as exception:
            response = str(exception)

        # Send response to main program
        socket.send_json(response)


if __name__ == "__main__":
    unit_converter()
