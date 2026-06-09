from fastapi import APIRouter,Depends, File, HTTPException, UploadFile, status

from app.services.document_upload_service import DocumentUploadService

from ..dependencies import get_upload_service
from ..schemas import DocumentUploadedResponse

router = APIRouter(prefix  ="/documents",tags=['documents'])

@router.post(
    "/upload",
    response_model=DocumentUploadedResponse,
    status_code = status.HTTP_201_CREATED,
)
async def upload_document(
    file: UploadFile = File(...),
    upload_service: DocumentUploadService = Depends(get_upload_service)
) -> DocumentUploadedResponse:
    try:
        return await upload_service.upload_document(
            upload_file = file
        )
    except ValueError as error:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = str(error),
        ) from error