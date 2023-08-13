from fastapi import APIRouter, Depends, HTTPException
from api.dependencies.microwave_helpers import set_microwave_state, get_microwave_state
from api.dependencies.jwt import verify_token
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/state")
def microwave_state():
    """Endpoint to fetch the current microwave state."""
    try:
        return get_microwave_state()
    except Exception as e:
        logger.error(f"Error in fetching the state: {e}")
        raise HTTPException(status_code=500, detail="Error in fetching the state.")

@router.post("/power/increase")
def increase_power():
    """Endpoint to increase the microwave's power."""
    try:
        state = get_microwave_state()
        new_power = min(100, state["power"] + 10)
        set_microwave_state(power=new_power)
        return {"power": new_power, "counter": state["counter"]}
    except Exception as e:
        logger.error(f"Error increasing power: {e}")
        raise HTTPException(status_code=500, detail="Error increasing power.")
    

@router.post("/power/decrease")
def decrease_power():
    """Endpoint to decrease the microwave's power."""
    try:
        state = get_microwave_state()
        new_power = max(0, state["power"] - 10)
        set_microwave_state(power=new_power)
        return {"power": new_power, "counter": state["counter"]}
    except Exception as e:
        logger.error(f"Error descresing power: {e}")
        raise HTTPException(status_code=500, detail="Error descresing power.")

@router.post("/counter/increase")
def increase_counter():
    """Endpoint to increase the microwave's counter."""
    try:
        state = get_microwave_state()
        new_counter = state["counter"] + 10
        set_microwave_state(counter=new_counter)
        return {"power": state["power"], "counter": new_counter}
    except Exception as e:
        logger.error(f"Error increasing counter: {e}")
        raise HTTPException(status_code=500, detail="Error increasing counter.")

@router.post("/counter/decrease")
def decrease_counter():
    """Endpoint to decrease the microwave's counter."""
    try:
        state = get_microwave_state()
        new_counter = max(0, state["counter"] - 10)
        set_microwave_state(counter=new_counter)
        return {"power": state["power"], "counter": new_counter}
    except Exception as e:
        logger.error(f"Error descresing counter: {e}")
        raise HTTPException(status_code=500, detail="Error descresing counter.")

@router.post("/cancel")
def cancel_operation(payload: dict = Depends(verify_token)):
    """Endpoint to cancel the microwave operation and reset its state."""
    try:
        print("Entered cancel")
        set_microwave_state(power=0, counter=0)
        return {"power": 0, "counter": 0}
    except Exception as e:
        logger.error(f"Error in cancelling microwave state: {e}")
        raise HTTPException(status_code=500, detail="Error in cancelling microwave state.")
