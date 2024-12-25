# Slurm Trouble Shooting

## State of nodes are down

Show the reason:

```sh
scontrol show node las0
```

Bring it up:

```sh
scontrol update NodeName=las0 State=resume
```
