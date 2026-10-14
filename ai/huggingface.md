# HuggingFace

<https://huggingface.co/>

## Install

```console
$ pip install -U huggingface_hub
```

## Usage

```console
$ hf download bartowski/Rocinante-12B-v1.1-GGUF Rocinante-12B-v1.1-Q8_0.gguf
...
✓ Downloaded
  path: /Users/xxxx/.cache/huggingface/hub/models--bartowski--Rocinante-12B-v1.1-GGUF/snapshots/9d15ca24c675a428fc5821cccc537f2a6f64987d/Rocinante-12B-v1.1-Q8_0.gguf
```

You can download a model to a specified dir by `--local-dir /path/to/dir`. Note there will be a `.cache` dir generated in it.

List models in cache:

```console
$ hf cache ls
ID                                            SIZE LAST_ACCESSED  LAST_MODIFIED REFS
-------------------------------------------- ----- -------------- ------------- ----
model/TheDrummer/Rocinante-X-12B-v1-GGUF     13.0G 51 minutes ago 2 days ago    main
model/bartowski/L3-8B-Stheno-v3.2-GGUF        8.5G 18 hours ago   2 days ago    main
model/bartowski/MN-12B-Mag-Mell-R1-GGUF      13.0G 2 hours ago    4 days ago    main
model/bartowski/Rocinante-12B-v1.1-GGUF      13.0G 26 minutes ago 4 days ago    main
```

Delete a unwanted model:

```console
$ hf cache rm model/mradermacher/Qwen3-14B-Uncensored-GGUF
About to delete 1 repo(s) totalling 12.1G.
  - model/mradermacher/Qwen3-14B-Uncensored-GGUF (entire repo)
Proceed with deletion? [y/N]: y
Cache deletion done. Saved 12.1G.
✓ Deleted 1 repo(s) and 1 revision(s); freed 12.1G.
  repos_deleted: 1
  revisions_deleted: 1
  freed: 12.1G
```
