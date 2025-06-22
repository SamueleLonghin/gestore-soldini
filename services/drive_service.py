from services.google_service_account import get_drive_service_service_account


def get_shared_files_with_user(user_email):
    service = get_drive_service_service_account()

    files = (
        service.files()
        .list(
            fields="files(id, name)",
            q="mimeType='application/vnd.google-apps.spreadsheet' and name contains 'Gestione Spese - '",
        )
        .execute()
        .get("files", [])
    )
    print(f"Trovati {len(files)} file condivisi.")
    print(f"Utente: {user_email}")
    print("Elenco dei file trovati:")
    for file in files:
        print(f" - {file['name']} (ID: {file['id']})")
    condivisi = []

    for file in files:
        try:
            permissions = (
                service.permissions()
                .list(fileId=file["id"], fields="permissions(emailAddress)")
                .execute()
            )
            for p in permissions.get("permissions", []):
                if p.get("emailAddress") == user_email:
                    condivisi.append(file)
                    break
        except Exception as e:
            print(f"Errore nel leggere i permessi per il file {file['id']}: {e}")

    return condivisi
