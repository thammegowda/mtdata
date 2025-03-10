import argparse
import json
from pathlib import Path
import time
from collections import defaultdict
from typing import List, Dict, Any

import requests

from mtdata import resource_dir, log, yaml
from mtdata.index import Index, DatasetId, Entry

QUERY_URL = "https://huggingface.co/datasets-json"
README_URL = "https://huggingface.co/datasets/{repo_id}/raw/main/README.md"
RESOURCE_FILE = resource_dir / 'huggingface-datasets.jsonl'
QPARAMS = {
    "task_categories": "task_categories:translation",
    "sort": "created",
    "withCount": "true",
    "p": 0,
}
HF_EXT = "hfds"  # huggingface dataset

# To refresh the data_file from huggingface:
#    python -m mtdata.index.huggingface --refresh

def load_all(index: Index):
    meta_file = RESOURCE_FILE
    assert meta_file.exists(), f"{meta_file} does not exist"
    assert meta_file.stat().st_size > 0, f"{meta_file} is empty"
    with meta_file.open() as lines:
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("//"):
                continue
            data = json.loads(line)
            if data['id'] != "google/wmt24pp":
                continue  # TODO: support other datasets

            id_parts = data['id'].split('/')
            assert len(id_parts) == 2, f"Invalid dataset id: {data['id']}"
            group, name = id_parts
            group = group.title()
            for config in data['configs']:
                split_name = name
                if config["split"] != "train":
                    # assume train is the default
                    split_name += f"_{config['split']}"
                orig_langs = config["name"]
                langs = tuple(orig_langs.split("-"))
                assert len(langs) in (1, 2), f"Invalid langs: {langs}"
                data_id = DatasetId(group=group, name=split_name, version="1", langs=langs)
                if data_id in index:
                    log.warning(f"Duplicate dataset id: {data_id}")
                    continue
                params = dict(langs=orig_langs, split=config["split"])
                url = "https://huggingface.co/datasets/" + data['id']
                meta = dict(config=config['name'], orig_id=data['id'], split=config["split"])
                in_paths = config["paths"]
                cite = None
                entry = Entry(did=data_id, url=url, in_paths=in_paths, cite=cite, ext=HF_EXT, in_ext=HF_EXT, meta=meta)
                index.add_entry(entry)


def query_datasets(page_num=0):
    params = QPARAMS.copy()
    last_request_time = 0
    request_interval = 1  # seconds
    while True:
        ### Fair crawling: dont overwhelm the server
        now = time.time()
        assert now >= last_request_time
        interval = now - last_request_time
        if interval < request_interval:
            time.sleep(request_interval - interval)
        last_request_time = time.time()
        ###
        params["p"] = page_num
        url_with_parms = f"{QUERY_URL}?{requests.compat.urlencode(params)}"
        log.info(f"GET {url_with_parms}")
        response = requests.get(url_with_parms)
        if response.status_code != 200:
            log.warning(f"Failed to fetch data: {response.status_code}; text:\n{response.text}")
            raise Exception(f"Failed to fetch data: {response.status_code}")
        data = response.json()
        if "datasets" not in data or not data["datasets"]:
            log.info("No more datasets found.")
            break
        for d in data["datasets"]:
            yield d
        page_num += 1
        # uncomment for testing on a subset of results
        #if page_num >= 10: break

def enrich_metadata(meta):
    """
    Enrich the dataset's metadata by parsing YAML config from README the repository.
    """
    # use API https://huggingface.co/docs/datasets/load_hub#configurations
    configs = meta.get("config", [])
    readme_url = README_URL.format(repo_id=meta["id"])
    log.info(f"GET {readme_url}")
    readme_text = requests.get(readme_url).text
    yaml_config_text = ""
    parts = readme_text.split("---")
    if len(parts) < 3:
        log.warning(f"Failed to find YAML config in {readme_url}")
        return False
    try:
        # find the text between the first and second "---"
        yaml_config_text = readme_text.split("---", 2)[1]
        readme_config = yaml.load(yaml_config_text)
        my_config = []
        for config in readme_config.get("configs", []):
            splits = defaultdict(list)
            for split in config.get("data_files", []):
                splits[split["split"]].append(split["path"])
            for name, paths in splits.items():
                my_config.append(dict(
                    name= config.get("config_name"),
                    split=name,
                    paths=paths,
                    #langs=None   #FIXME:  need to infer langs. often in config name but not consistent
                ))
        if my_config:
            meta["configs"] = my_config
            return True
    except Exception as e:
        log.warning(f"Failed to parse YAML config in {readme_url}: {e}")
    return False


def enrich_metadata_lite(meta):
    """
    Enrich the dataset's metadata by parsing YAML config from README the repository.
    """
    # NOTE: this didnt work. code froze
    import datasets as hfds
    configs = hfds.get_dataset_config_names(meta["id"])
    my_config = []
    for config_name in configs:
        splits = hfds.get_dataset_split_names(meta["id"], config_name)
        for split_name in splits:
            my_config.append(dict(
                    name=config_name,
                    split=split_name
                    #langs=None   #FIXME:  need to infer langs. often in config name but not consistent
                ))
    if my_config:
        meta["configs"] = my_config
        return True
    return False


def update_resource_file(out_file, refresh=False):
    all_out_file = out_file.with_name(out_file.name.replace(".jsonl", "") + ".all.jsonl")
    if refresh or not out_file.exists():
        log.info(f"Fetching datasets from {QUERY_URL}. This might take a while")
        datasets = query_datasets()
        datasets = list(sorted(datasets, key=lambda x: x["id"].lower()))
        with all_out_file.open("w", encoding="utf-8") as all_f:
            for d in datasets:
                line = json.dumps(d, ensure_ascii=False, indent=None)
                all_f.write(line + "\n")
    else:
        log.info(f"Loading datasets from {all_out_file}")
        # load existing datasets from the resource file
        datasets = []
        with all_out_file.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("//"):
                    continue
                data = json.loads(line)
                datasets.append(data)
    if not datasets:
        log.warning("No datasets found.")
        return

    # focus on a selected few datasets for now before expanding to others
    # enrich_metadata is slow and we need to be careful about the number of requests
    select_datasets = {"google/wmt24pp", "ai4bharat/samanantar"}
    log.info(f"Writing selected datasets to {out_file} and all datasets to {all_out_file}")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        for d in datasets:
            if select_datasets and d["id"] not in select_datasets:
                continue
            # enrich metadata for a selected few datasets
            enrich_metadata(d)
            line = json.dumps(d, ensure_ascii=False, indent=None)
            f.write(line + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Download datasets from Hugging Face")
    parser.add_argument("-o", "--out", dest='out_file', type=str, default=RESOURCE_FILE,
        help="Output file to save the downloaded datasets",)
    parser.add_argument("-r", "--refresh", dest='refresh', action='store_true',
        help="Refresh the datasets from Hugging Face")

    args = parser.parse_args()
    out_file = Path(args.out_file).expanduser()
    update_resource_file(out_file, refresh=args.refresh)
