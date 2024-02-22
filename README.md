# README

** This is a draft **

To replicate the solution, do the following:

- create an Azure AI Search service (basic tier)
- Use the *Import and vectorize data* tool to index your data files. This tool automatically creates an indexer that pulls your files, cracks them, splits them in multiple sub-documents, calculates vectors for each chunk, and index them. The tool is available in the Azure Portal, Azure AI Search resource, Overview menu. Note that the tool automatically creates object definitions (data source, indexer, index, cognitive pipeline), i.e., YAML files that can be modified and used to update the service from a CI/CD pipeline.
- Open VSCode and copy the chat flow solution. Connections must be reconfigured. The PromptFlow app must be installed in VSCode if not already available.

The above flow can be deployed in multiple ways:
- the flow_fun.py provides an example of how to use the flow from within Python code. The flow would run on the same process as the UI.
- the flow can be deployed as a local web app on //localhost:8080.
- the flow can be build as a container and deployed as relevant.