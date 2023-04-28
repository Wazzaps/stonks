import base64
import json
import requests
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.modify"]
CREDS_DIR = Path("/mnt/hdd/stonks/creds")
UNPROCESSED_DIR = Path("/mnt/hdd/stonks/unprocessed")
PROCESSED_DIR = Path("/mnt/hdd/stonks/processed")


def main():
    try:
        fetch_new_zips()
    except Exception as e:
        print(f"An unknown error occurred while fetching zips: {e}")

    try:
        stonks_api_creds = json.load((CREDS_DIR / "stonks_creds.json").open("r"))
        PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        for f in UNPROCESSED_DIR.iterdir():
            print(f"Processing {f.name}")
            if f.is_file() and f.suffix == ".zip":
                res = requests.put(
                    f"http://localhost:8000/api/v1/parse_swiftness_zip?zip_pass={stonks_api_creds['zip_pass']}",
                    data=f.open("rb"),
                    auth=(stonks_api_creds["username"], stonks_api_creds["password"]),
                )
                if res.status_code in (200, 201):
                    f.rename(PROCESSED_DIR / f.name)
                else:
                    print(f"Failed to process {f.name}: {res.status_code}")
                    print(res.content.decode("utf-8", errors="ignore"))
    except Exception as e:
        print(f"An unknown error occurred while posting zips for processing: {e}")


def get_the_label_id(service):
    labels = service.users().labels().list(userId="me").execute()
    for label in labels["labels"]:
        if label["name"] == "swiftness-processed":
            return label["id"]


def fetch_new_zips():
    creds = get_google_creds()

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        label_id = get_the_label_id(service)
        if not label_id:
            # Create the label if it doesn't exist
            label_id = (
                service.users()
                .labels()
                .create(
                    userId="me",
                    body={
                        "name": "swiftness-processed",
                        "labelListVisibility": "labelShow",
                        "messageListVisibility": "show",
                    },
                )
                .execute()["id"]
            )

        messages = (
            service.users()
            .messages()
            .list(userId="me", q="from:doNotReply@swiftness.co.il has:attachment -label:swiftness-processed")
            .execute()
        ).get("messages", [])

        processed_messages = []
        try:
            for message in messages:
                fetch_message_attachment(service, message)
                processed_messages.append(message["id"])
        finally:
            if processed_messages:
                service.users().messages().batchModify(
                    userId="me", body={"ids": processed_messages, "addLabelIds": [label_id]}
                ).execute()

    except HttpError as e:
        # TODO(developer) - Handle errors from gmail API.
        print(f"A Gmail error occurred: {e}")


def fetch_message_attachment(service, message):
    message_id = message["id"]
    message = service.users().messages().get(userId="me", id=message_id).execute()
    headers = {header["name"]: header["value"] for header in message["payload"]["headers"]}
    print(f'Processing ID={message_id}, Subject="{headers["Subject"]}", Date="{headers["Date"]}"')

    if "parts" not in message["payload"]:
        return

    for part in message["payload"]["parts"]:
        if part.get("mimeType", "") != "application/octet-stream":
            continue
        if not part.get("filename", "").endswith(".zip"):
            continue
        attachment_id = part["body"]["attachmentId"]
        attachment_size = part["body"]["size"]
        attachment_filename = part["filename"]
        assert "/" not in attachment_filename, "Invalid attachment filename"
        assert attachment_size < 10 * 1024 * 1024, "Attachment too large"

        print(f"Downloading {attachment_filename}")
        attachment = (
            service.users().messages().attachments().get(userId="me", messageId=message_id, id=attachment_id).execute()
        )

        UNPROCESSED_DIR.mkdir(parents=True, exist_ok=True)
        path = UNPROCESSED_DIR / attachment_filename
        with path.open("wb") as f:
            f.write(base64.urlsafe_b64decode(attachment["data"]))

        break  # Only one attachment per message


def get_google_creds():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if (CREDS_DIR / "token.json").exists():
        creds = Credentials.from_authorized_user_file(str(CREDS_DIR / "token.json"), SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(str(CREDS_DIR / "credentials.json"), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with (CREDS_DIR / "token.json").open("w") as token:
            token.write(creds.to_json())
    return creds


if __name__ == "__main__":
    main()
