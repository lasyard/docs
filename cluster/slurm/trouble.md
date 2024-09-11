# Slurm Trouble Shooting

## State of nodes are down

Show the reason:

```sh
scontrol show node las1
```

Bring it up:

```sh
scontrol update NodeName=las1 State=resume
scontrol update NodeName=las[2-3] State=resume
```
