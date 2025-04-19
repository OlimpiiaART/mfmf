import os
import requests
import zipfile

# === НАСТРОЙКИ ===
token = "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"
repo = "OlimpiiaART/rmfmf"
tag = "repomodslatest"
zip_path = "BepInEx.zip"
base_folder = "/home/olimpiia/.config/r2modmanPlus-local/REPO/profiles/Default/BepInEx/"
folders_to_zip = ["plugins", "config"]
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github+json"
}

def zip_subfolders(base_path, folders, zip_file_path):
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for folder in folders:
            full_folder_path = os.path.join(base_path, folder)
            for root, dirs, files in os.walk(full_folder_path):
                for file in files:
                    abs_path = os.path.join(root, file)

                    # Относительный путь от папки folder
                    rel_path = os.path.relpath(abs_path, base_path)

                    # Префиксируем явно BepInEx
                    archive_path = os.path.join("BepInEx", rel_path)

                    zipf.write(abs_path, archive_path)

zip_subfolders(base_folder, folders_to_zip, zip_path)
print(f"📦 Архив создан: {zip_path}")

# === Получаем релиз по тегу ===
release_url = f"https://api.github.com/repos/{repo}/releases/tags/{tag}"
release = requests.get(release_url, headers=headers).json()
if "upload_url" not in release:
    print("🛠 Релиз не найден, создаю новый...")

    create_release_payload = {
        "tag_name": tag,
        "name": "Auto Release",
        "body": "Auto-generated release for latest mod build",
        "draft": False,
        "prerelease": False
    }

    create_url = f"https://api.github.com/repos/{repo}/releases"
    create_resp = requests.post(create_url, headers=headers, json=create_release_payload)

    if create_resp.status_code != 201:
        print("❌ Не удалось создать релиз:", create_resp.status_code, create_resp.text)
        exit(1)

    release = create_resp.json()


print("✅ Upload result:", r.status_code, r.json().get("browser_download_url"))
