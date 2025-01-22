from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi import APIRouter, HTTPException, Depends
from Application.Commands.download_command import DownloadCommand
from Application.CommandHandlers.download_command_handler import DownloadCommandHandler as CommandHandler
from Presentation.Requests.get_request import GetRequest

# Initialize the router
router = APIRouter()

@router.get("/command/get/{cid}/{filename}")
async def command(
    request: GetRequest = Depends(),
    command_handler: CommandHandler = Depends()
):
    try:
        command = DownloadCommand(
            cid=request.cid,
            filename=request.filename
        )
        
        download_bytes = command_handler.handle(command)
        
        if download_bytes:
            file_stream = BytesIO(download_bytes)
            
            return StreamingResponse(
                file_stream,
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f"attachment; filename={request.filename}"
                }
            )

        else:
            raise HTTPException(status_code=400, detail="Download failed")
    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))  # Handle invalid input
    except Exception as e:
        print(f"An error occurred: {e}")
        print(e)
        trace = e.__traceback__
        while trace.tb_next:
            trace = trace.tb_next
            print(f"Caused by: {trace.tb_frame.f_code.co_name} in {trace.tb_frame.f_code.co_filename}:{trace.tb_lineno}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
