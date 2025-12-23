import os
import requests
from pathlib import Path
from urllib.parse import quote

SERVERS_URL = "https://cdn-us-1.comaps.app/servers"

def get_latest_map_version():
    response = requests.get(f"{SERVERS_URL}?allversions", timeout=30)
    response.raise_for_status()
    return response.json()[-1]

def get_best_cdn_host(map_version):
    response = requests.get(f"{SERVERS_URL}?version={map_version}", timeout=30)
    response.raise_for_status()
    return response.json()[0]

def fetch_country_json(cdn_host, version):
    """Fetch countries.txt (JSON content) from CDN and return parsed JSON"""
    url = f"{cdn_host}/maps/{version}/countries.txt"
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.json()

def expand_maps(user_maps, cdn_host, version):
    """Expand countries/groups into all sub-maps"""
    data = fetch_country_json(cdn_host, version)

    all_maps = {}
    for entry in data.get("g", []):
        if "g" in entry:
            all_maps[entry["id"]] = [sub["id"] for sub in entry["g"]]
        else:
            all_maps[entry["id"]] = []

    expanded = []
    for m in user_maps:
        m_clean = m.replace(".mwm", "")
        if m_clean in all_maps and all_maps[m_clean]:
            for sub_map in all_maps[m_clean]:
                expanded.append(f"{sub_map}.mwm")
        else:
            expanded.append(f"{m_clean}.mwm")

    return list(dict.fromkeys(expanded))

def download_file(url, output_path):
    """
    Downloads a file from `url` to `output_path`.
    Skips download if the file already exists.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.exists():
        print(f"Skipping {output_path.name}, already exists", flush=True)
        return

    print(f"Downloading {output_path.name}...", flush=True)
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
    print(f"Downloaded {output_path.name}", flush=True)

def main():
    maps_env = os.getenv("MAPS")
    output_dir = Path(os.getenv("OUTPUT_DIR", "/maps"))

    if not maps_env:
        raise RuntimeError("MAPS env variable is required")

    user_maps = [m.strip() for m in maps_env.split(",") if m.strip()]

    print("Resolving latest map version…")
    map_version = get_latest_map_version()
    print(f"Using map version: {map_version}")

    print("Resolving best CDN host…")
    cdn = get_best_cdn_host(map_version)
    print(f"Using CDN: {cdn}")

    maps_to_download = expand_maps(user_maps, cdn, map_version)

    for map_file in maps_to_download:
        encoded = quote(map_file)
        url = f"{cdn}/maps/{map_version}/{encoded}"
        output_path = output_dir / map_version / map_file
        print(f"Downloading {map_file} -> {output_path}", flush=True)
        download_file(url, output_path)

    print("All downloads complete")

if __name__ == "__main__":
    main()

