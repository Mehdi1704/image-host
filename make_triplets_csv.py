#!/usr/bin/env python3
import os, csv, sys, subprocess
from pathlib import Path
from urllib.parse import quote

# ---- EDIT THESE TO MATCH YOUR PUBLIC REPO ----
USER        = "Mehdi1704"
REPO        = "image-host"
REPO_SUBDIR = "output_images"         # "" if folders are at repo root

IMAGES_DIR  = f"{REPO_SUBDIR}/images"
DEPTH_DIR   = f"{REPO_SUBDIR}/depth"
NORMALS_DIR = f"{REPO_SUBDIR}/normals"

OUT_CSV     = "triplets_by_basename.csv"
# ----------------------------------------------

IMG_EXTS    = {".jpg", ".jpeg", ".jpe"}
DEPTH_EXTS  = {".png"}
NORMAL_EXTS = {".png"}

def detect_branch():
    try:
        b = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True
        ).strip()
        # Accept either "master" or "main" etc.
        return b if b else "master"
    except Exception:
        return "master"

def raw_base(user, repo, branch):
    # you can also return f".../{user}/{repo}/refs/heads/{branch}/" if you prefer that style
    return f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/"

def index_by_stem(folder: Path, allowed_exts):
    mapping = {}
    for name in os.listdir(folder):
        p = folder / name
        if not p.is_file():
            continue
        ext = p.suffix.lower()
        if allowed_exts and ext not in allowed_exts:
            continue
        mapping[p.stem] = name
    return mapping

def main():
    branch = detect_branch()  # e.g., "master"
    RAW_BASE = raw_base(USER, REPO, branch)
    root = Path(".").resolve()

    images_p  = root / IMAGES_DIR
    depth_p   = root / DEPTH_DIR
    normals_p = root / NORMALS_DIR
    for p in (images_p, depth_p, normals_p):
        if not p.is_dir():
            sys.exit(f"[error] folder not found: {p}")

    imgs  = index_by_stem(images_p,  IMG_EXTS)
    deps  = index_by_stem(depth_p,   DEPTH_EXTS)
    norms = index_by_stem(normals_p, NORMAL_EXTS)

    common = sorted(set(imgs) & set(deps) & set(norms))
    if not common:
        sys.exit("[error] found no complete triplets (basename present in all three folders).")

    out_path = root / OUT_CSV
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["basename","image_url","depth_url","normal_url"])
        for stem in common:
            image_url  = f"{RAW_BASE}{IMAGES_DIR}/{quote(imgs[stem])}"
            depth_url  = f"{RAW_BASE}{DEPTH_DIR}/{quote(deps[stem])}"
            normal_url = f"{RAW_BASE}{NORMALS_DIR}/{quote(norms[stem])}"
            w.writerow([stem, image_url, depth_url, normal_url])

    print(f"[ok] wrote {out_path} with {len(common)} rows (branch: {branch})")

if __name__ == "__main__":
    main()