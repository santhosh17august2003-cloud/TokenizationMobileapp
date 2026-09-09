from pathlib import Path
import os
import shutil
import tarfile
import zipfile


ORIGINAL_USERPROFILE = os.environ.get("USERPROFILE")
PROJECT_DIR = Path(__file__).resolve().parent
LOCAL_RUNTIME_HOME = PROJECT_DIR / ".runtime-home"

LOCAL_RUNTIME_HOME.mkdir(exist_ok=True)

if ORIGINAL_USERPROFILE:
    orig_flet = Path(ORIGINAL_USERPROFILE) / ".flet"
    dest_flet = LOCAL_RUNTIME_HOME / ".flet"
    if orig_flet.exists() and not dest_flet.exists():
        try:
            shutil.copytree(orig_flet, dest_flet)
        except Exception:
            pass

os.environ["USERPROFILE"] = str(LOCAL_RUNTIME_HOME)
os.environ["HOME"] = str(LOCAL_RUNTIME_HOME)

import flet as ft

if not hasattr(ft, "colors") and hasattr(ft, "Colors"):
    ft.colors = ft.Colors
if not hasattr(ft, "icons") and hasattr(ft, "Icons"):
    ft.icons = ft.Icons
if hasattr(ft, "border") and not hasattr(ft.border, "all") and hasattr(ft, "Border"):
    ft.border.all = ft.Border.all

from ui.main_page import build_main_page


def patch_flet_desktop_cache() -> None:
    import flet_desktop
    from flet.utils import safe_tar_extractall, safe_zip_extractall

    def ensure_client_cached_without_rename() -> Path:
        cache_dir = flet_desktop.__get_client_storage_dir()
        executable = cache_dir / "flet" / "flet.exe"
        if executable.exists():
            return cache_dir

        resolved_cache_dir = cache_dir.resolve()
        resolved_runtime_home = LOCAL_RUNTIME_HOME.resolve()
        if resolved_runtime_home not in resolved_cache_dir.parents:
            raise RuntimeError(f"Unexpected Flet cache location: {cache_dir}")

        if cache_dir.exists():
            shutil.rmtree(cache_dir, ignore_errors=True)
        cache_dir.mkdir(parents=True, exist_ok=True)

        artifact = flet_desktop.get_artifact_filename()
        bundled = Path(flet_desktop.get_package_bin_dir()) / artifact
        archive_path = bundled if bundled.exists() else Path(flet_desktop.__download_flet_client(artifact))

        if artifact.endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as archive:
                safe_zip_extractall(archive, str(cache_dir))
        else:
            with tarfile.open(archive_path, "r:gz") as archive:
                safe_tar_extractall(archive, str(cache_dir))

        return cache_dir

    flet_desktop.ensure_client_cached = ensure_client_cached_without_rename


def main(page: ft.Page) -> None:
    build_main_page(page)


if __name__ == "__main__":
    if os.name == "nt":
        patch_flet_desktop_cache()
    ft.run(main)
