# Talc Demo

A simple application that answers questions about the warranty and maintenance of Toyota vehicles using LangChain.

Talc is used to evaluate the performance of this system.

## Running the demo

Push a change to github and view the results of testing in Github Actions.

## Other notes:

### Generating the test set:

Point at a PDF file and generate a test set with a sweep of the entire document.

You'll need to manually merge the question set CSVs if you generate using multiple files.

```bash
talc generate --file ./knowledge_base/hybrid.pdf --out ./artifacts/test_set.csv --dataset_name test --generation_modes sweep
```

### Running the tests:

From the `/talc-demo` directory:

```bash
python ./src/main.py
```

This generates an `output.csv` file in the `artifacts` directory.

### Grading the tests with talc:

When you check in a new version of output.csv, the tests will be run automatically in Github Actions.

Alternatively, you can run the tests locally:

```bash
talc upload-and-grade --csv ./artifacts/output.csv --name "Demo test run" --fail_on_error
```

