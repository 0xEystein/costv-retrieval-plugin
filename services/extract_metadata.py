from models.models import Source
from services.openai import get_chat_completion
import json
from typing import Dict


def extract_metadata_from_document(text: str) -> Dict[str, str]:
    sources = Source.__members__.keys()
    sources_string = ", ".join(sources)
    # This prompt is just an example, change it to fit your use case
    uid: Optional[str] = None
    title: Optional[str] = None
    introduction: Optional[str] = None
    duration: Optional[float] = None
    video_url: Optional[str] = None
    cover: Optional[str] = None
    author: Optional[str] = None
    avatar: Optional[str] = None
    like: Optional[int] = None
    view: Optional[int] = None
    gift: Optional[int] = None
    created_at: Optional[str] = None
    messages = [
        {
            "role": "system",
            "content": f"""
            Given a document from a user, try to extract the following metadata:
            - uid: string, id of author
            - title: string, title of video
            - introduction: string, introduction of video
            - duration: float, duration of video
            - video_url: string or don't specify
            - cover: string or don't specify
            - author: string or don't specify
            - avatar: string or don't specify
            - like: integer, number of video like
            - view: integer, number of video view
            - gift: integer, number of video gift
            - created_at: string or don't specify

            Respond with a JSON containing the extracted metadata in key value pairs. If you don't find a metadata field, don't specify it.
            """,
        },
        {"role": "user", "content": text},
    ]

    completion = get_chat_completion(
        messages, "gpt-4"
    )  # TODO: change to your preferred model name

    print(f"completion: {completion}")

    try:
        metadata = json.loads(completion)
    except:
        metadata = {}

    return metadata
