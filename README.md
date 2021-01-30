# Repos List

I had a need to export a list of all the projects that I've worked on over
the years, and this is it! You can export a GitHub token, and run the
script. The output file will be a `<username>-github-repos.tsv` file in the
present working directory.

```bash
export GITHUB_TOKEN=xxxxxxxxxxxxxxx
python export.py vsoch
```

Then it produces the example file, as shown at [vsoch-repositories.tsv](vsoch-repositories.tsv).
Note that I've manually filtered this file to only include my own repositories, and repositories
that I've contribed to.

