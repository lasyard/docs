# HuggingFace

<https://huggingface.co/>

## Install

```console
$ pip install -U huggingface_hub
```

## Usage

```console
$ hf download hf://TheDrummer/Cydonia-24B-v4.3-GGUF/Cydonia-24B-v4zg-Q4_K_M.gguf
...
✓ Downloaded
  path: /Users/jyg/.cache/huggingface/hub/models--TheDrummer--Cydonia-24B-v4.3-GGUF/snapshots/5f34e78ac0b8b61671a683b2e094e6f3fe6ae037/Cydonia-24B-v4zg-Q4_K_M.gguf
```

You can download a model to a specified dir by `--local-dir /path/to/dir`. Note there will be a `.cache` dir generated in it.

List models in cache:

```console
$ hf cache ls                                                   
ID                                      SIZE LAST_ACCESSED  LAST_MODIFIED REFS
-------------------------------------- ----- -------------- ------------- ----
model/TheDrummer/Cydonia-24B-v4.3-GGUF 14.3G 52 minutes ago 7 hours ago   main

Found 1 repo(s) for a total of 1 revision(s) and 14.3G on disk.
```

Delete a unwanted model:

```console
$ hf cache rm model/Doctor-Shotgun/MS3.2-24B-Magnum-Diamond-GGUF
About to delete 1 repo(s) totalling 14.3G.
  - model/Doctor-Shotgun/MS3.2-24B-Magnum-Diamond-GGUF (entire repo)
Proceed with deletion? [y/N]: y
✓ Deleted 1 repo(s) and 1 revision(s); freed 14.3G.
  repos_deleted: 1
  revisions_deleted: 1
  freed: 14.3G
```
