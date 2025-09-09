# Macrocosmos Protobufs

Protobufs used by Macrocosmos products

## Usage

Here are instructions on how to add and update the protos from your own project repo.

> ⚠️ These commands must be run from the target repo's root directory

How to add the Macrocosmos protobufs to a project repo:

```bash
git subtree add --prefix=protos git@github.com:macrocosm-os/macrocosmos-protos.git main --squash
```

You can pull the latest updates to `main` from this repo to your project repo with:

```bash
git subtree pull --prefix=protos git@github.com:macrocosm-os/macrocosmos-protos.git main --squash
```

To push changes back to this repo for other projects, run this to create a branch:

```bash
git subtree push --prefix=protos git@github.com:macrocosm-os/macrocosmos-protos.git <your-branch-name>
```

You'll then need to create a pull request for that branch to merge to `main`.
