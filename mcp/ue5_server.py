from mcp.server.fastmcp import FastMCP
from pathlib import Path
import subprocess
import os

mcp = FastMCP("agentos-ue5")

# ==================================================
# CONFIG (override via env vars)
# ==================================================
UE_ENGINE_ROOT = Path(os.environ.get("UE_ENGINE_ROOT", ""))
UE_PROJECT_ROOT = Path(os.environ.get("UE_PROJECT_ROOT", ""))


# ==================================================
# HELPERS
# ==================================================
def find_uproject():
    if UE_PROJECT_ROOT.exists():
        projects = list(UE_PROJECT_ROOT.glob("*.uproject"))
        if projects:
            return projects[0]
    return None


def meta(tool: str):
    return {
        "tool": tool,
        "system": "UE5",
        "engine_root": str(UE_ENGINE_ROOT),
        "project_root": str(UE_PROJECT_ROOT),
    }


# ==================================================
# 1. GENERATE PROJECT FILES
# (calls GenerateProjectFiles.bat)
# ==================================================
@mcp.tool()
def generate_project_files():
    uproject = find_uproject()
    if not uproject:
        return {"error": "No .uproject found"}

    script = UE_ENGINE_ROOT / "Engine/Build/BatchFiles/GenerateProjectFiles.bat"

    cmd = [str(script), f"-project={uproject}"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "meta": meta("generate_project_files"),
    }


# ==================================================
# 2. BUILD PROJECT (UBT via Build.bat)
# ==================================================
@mcp.tool()
def build_project(configuration: str = "Development Editor"):
    uproject = find_uproject()
    if not uproject:
        return {"error": "No .uproject found"}

    build_script = UE_ENGINE_ROOT / "Engine/Build/BatchFiles/Build.bat"

    cmd = [
        str(build_script),
        f"{uproject.stem}Editor",
        "Win64",
        configuration,
        f"-project={uproject}",
        "-WaitMutex",
        "-FromMsBuild",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "meta": meta("build_project"),
    }


# ==================================================
# 3. CLEAN BUILD (Binaries/Intermediate reset)
# ==================================================
@mcp.tool()
def clean_project():
    removed = []

    for folder in ["Binaries", "Intermediate"]:
        path = UE_PROJECT_ROOT / folder
        if path.exists():
            subprocess.run(["rm", "-rf", str(path)], shell=True)
            removed.append(str(path))

    return {"removed": removed, "meta": meta("clean_project")}


# ==================================================
# 4. LAUNCH EDITOR
# ==================================================
@mcp.tool()
def launch_editor():
    uproject = find_uproject()
    if not uproject:
        return {"error": "No .uproject found"}

    editor = UE_ENGINE_ROOT / "Engine/Binaries/Win64/UnrealEditor.exe"

    process = subprocess.Popen([str(editor), str(uproject)])

    return {
        "status": "launched_editor",
        "pid": process.pid,
        "meta": meta("launch_editor"),
    }


# ==================================================
# 5. LAUNCH GAME MODE
# ==================================================
@mcp.tool()
def launch_game():
    uproject = find_uproject()
    if not uproject:
        return {"error": "No .uproject found"}

    editor = UE_ENGINE_ROOT / "Engine/Binaries/Win64/UnrealEditor.exe"

    process = subprocess.Popen([str(editor), str(uproject), "-game"])

    return {"status": "launched_game", "pid": process.pid, "meta": meta("launch_game")}


# ==================================================
# 6. DEBUG LAUNCH (with log window)
# ==================================================
@mcp.tool()
def launch_debug():
    uproject = find_uproject()
    if not uproject:
        return {"error": "No .uproject found"}

    editor = UE_ENGINE_ROOT / "Engine/Binaries/Win64/UnrealEditor.exe"

    process = subprocess.Popen([str(editor), str(uproject), "-log"])

    return {
        "status": "launched_debug",
        "pid": process.pid,
        "meta": meta("launch_debug"),
    }


# ==================================================
# 7. UBA STATUS (placeholder hook)
# ==================================================
@mcp.tool()
def uba_status():
    return {
        "status": "assumed_active",
        "note": "UBA is handled via Horde / Build Accelerator pipeline automatically during builds",
        "meta": meta("uba_status"),
    }
