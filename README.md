# Continuous Evaluation

## Problem Settings

Developers of an AI system want to see their efforts are improving the effectiveness of their work. For example, if we are developing an image classification system, we would like to see that with the merge of more and more pull requests, the system could have higher precision and higher recall values.  From this example, we see the following concepts:

1. An AI system has several KPIs.  The image classification system has two KPIs -- precision and recall.
1. KPIs are supposed to be improved (increment or decrement) with respect to Git commits.

## The Solution

We proposal to develop a tool, the *Continuous Evaluation* program, which checks out each Git commits (or, for saving computational resource, only Git merge commits on the main branch), builds and runs the *KPI evaluation programs* in the commit.  

An KPI evaluation program is the one that computes and prints one or more KPIs.  For example, all programs whose filenames have the suffix `_kpi`.

Given that each Git commit is immutable and has a timestamp, and each Git commit contains some KPI evaluation programs that prints a number, say, N, KPI values, the running of the continuous evaluation program with the AI system's Git repository should fill a table with the following scheme:

| Git commit SHA | Date & Time | KPI 1 (precision) | KPI 2 (recall) |
|----------------|-------------|-------------------|----------------|
| 195aef12       | 2018-01-01  | 50.01%            | 49.17%         |
| 4u059674       | 2018-01-02  | 51.01%            | 55.41%         |
| 39bcc9e1       | 2018-01-03  | 29.01%            | 78.17%         |
| 867abbce       | 2018-01-04  | 58.01%            | 40.92%         |

Here we noticed that the over trends of the precision grows w.r.t. date/time, but the number 29.01% on 2018-01-03 is a decrease, thus warns us about something wrong with the merge commit 39bcc9e1 and reminds us to check the corresponding pull request.

## Components in the Solution

The AI system to be monitored must include:

1. One or more KPI evaluation programs that prints the KPI value.
1. A bash script, say `./kpi.bash` that builds and runs the KPI evaluation programs.

The Continuous Evaluation system should have the following features:

1. A program or a function `build_and_eval(string git_repo, string git_commit_sha, Storage store)`, which
   - checks out the source code of the specified Git commit
   - builds the commit
   - runs the KPI programs
   - save KPI values into the table in `store`.

1. A program `build_and_eval_all(string git_repo, Storage store)`, which
   - loop over each merge commit in some branches (`develop` and `master`)
   - for each commit, if the row in the above table is empty, call `build_and_eval(repo, commit, store)`.
   
1. The storage service that can maintain the above table, and preferablly analyze and plot the data.  A good choice is Google Doc.

## Detailed Design

Consider writing `build_and_eval` as a Bash function. A simple reference implementation is as follows:

```bash
function build_and_eval(repo_url, commit, local_repo_dir, google_doc_api_key) {
  if [[ -d $local_repo_dir ]]; then
    git clone $repo_url -o $local_repo_dir
  fi
  
  cd $local_repo_dir
  
  git checkout -b current $commit
  
  ./kpi.bash | \                                         # Build and run KPI evluation programs.
    awk '$1 == "KPI" { printf("%s %s", $2, $3); }' | \   # Extract printed KPI names and values.
    google-doc-cli google_doc_api_key repo_url commit    # Write to table repo_url and row commit.
    
  git checkout master
  git branch -d current
}
```

Survey if there is a convenient way, e.g., a command line tool, that can write data into a Google Doc spreadsheet.
   
