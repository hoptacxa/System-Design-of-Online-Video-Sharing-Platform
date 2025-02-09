from fastapi.responses import StreamingResponse
from io import BytesIO
from fastapi import APIRouter, HTTPException, Depends
from Application.Commands.download_command import DownloadCommand
from Application.CommandHandlers.download_command_handler import DownloadCommandHandler
from Application.CommandHandlers.download_by_name_command_handler import DownloadByNameCommandHandler
from Application.CommandHandlers.pull_command_handler import PullCommandHandler
from Presentation.Requests.get_request import GetRequest
from Presentation.Requests.get_by_name_request import GetByNameRequest
import os
from Application.Commands.download_by_name_command import DownloadByNameCommand
# Initialize the router
router = APIRouter()

@router.get("/command/get_by_name/{name}/{filename}")
async def command(
    request: GetByNameRequest = Depends(),
    command_handler: DownloadByNameCommandHandler = Depends()
):
    try:
        command = DownloadByNameCommand(
            name=request.name,
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

@router.get("/command/pull/{cid}/{filename:path}")
async def command_pull(
    request: GetRequest = Depends(),
    command_handler: PullCommandHandler = Depends()
):
    try:
        command = DownloadCommand(
            cid=request.cid,
            filename=request.filename
        )
        
        download_bytes = command_handler.handle(command)
        
        if download_bytes:
            file_stream = BytesIO(download_bytes)
            
            filename = os.path.basename(request.filename)
            return StreamingResponse(
                file_stream,
                media_type="application/octet-stream",
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
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

@router.get("/command/get/{cid}/{filename}")
async def command(
    request: GetRequest = Depends(),
    command_handler: DownloadCommandHandler = Depends()
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
