from .database import get_redis
from api.events import state_change_event  # Import the state change event


def get_microwave_state():
    """
    Function to retrieve the current state of the microwave from Redis.

    Returns:
        dict: A dictionary containing the power and counter values of the microwave.
    """
    r = get_redis()
    power = r.get("microwave_power") or 0
    counter = r.get("microwave_counter") or 0
    return {"power": int(power), "counter": int(counter)}

def set_microwave_state(power=None, counter=None):
    """
    Function to set the state of the microwave in Redis and notify listeners of the change.

    Parameters:
        power (int, optional): The new power value to set.
        counter (int, optional): The new counter value to set.
    """
    r = get_redis()
    if power is not None:
        r.set("microwave_power", power)
    if counter is not None:
        r.set("microwave_counter", counter)

    # Set the event to notify listeners of the state change
    state_change_event.set()

