from fastapi import APIRouter, HTTPException, Depends
from Presentation.Requests.get_request import GetRequest

# Initialize the router
router = APIRouter()

@router.get("/command/get", response_model=dict)
async def command(request: GetRequest = Depends()):
    try:
        return {}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))  # Handle invalid input
    except Exception as e:
        print(e)
        trace = e.__traceback__
        while trace.tb_next:
            trace = trace.tb_next
            print(f"Caused by: {trace.tb_frame.f_code.co_name} in {trace.tb_frame.f_code.co_filename}:{trace.tb_lineno}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
