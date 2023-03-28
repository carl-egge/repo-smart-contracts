<template>
    <b-container>
        <b-row>
            <b-col>
                <h4 class="font-weight-bold">The Smart Contract Repository</h4>
            </b-col>
        </b-row>
        <hr>
        <b-row>
            <b-col>
                <h5># About</h5>
                <p>
                    Blockchain technologies are a growing field of research and public interest. Second generation blockchains, like Ethereum, allow users to execute smart contracts, which are distributed applications executing user-defined logic. This not only expands the utility of blockchains, but also provides new opportunities for tools for solving the same issues that arise with conventional programs. Such tools include optimization of code, detecting code smells and vulnerabilities and developing automated code generation models among others. Such developments require the presence of a dataset of similar code which can be annotated and analyzed according to the desired end application. Existing sources of smart contract code include block explorers that provide limited search and retrieval capabilities on the single version of the contract deployed on the blockchain. Hence, to aid the progress of research, this tool introduces the Smart Contract Repository — a repository of publicly available Solidity smart contracts, complete with multiple versions of the same contract to help the analysis of the effects of incremental changes in source code.
                </p>
                <p>
                    The Smart Contracts in this repository are retrieved from GitHub using the <a href="https://github.com/carl-egge/github-file-scraper" target="_blank">GitHub File Scraper</a>. This is a tool that was also developed by the author of this repository. The scraper is a Python script that exploits the GitHub API to retrieve a list of repositories that contain a specific file. The scraper then retrieves the files from each repository and stores them. The scraper is currently configured to retrieve all Solidity smart contracts from GitHub that are licensed. The scraper is run periodically to collect new contracts for this repository.
                </p>
            </b-col>
        </b-row>
        <hr>
        <b-row>
            <b-col>
                <h5># API</h5>
                <p>
                    This repository is also available as an API. The API is available at <a href="https://api.smartcontractrepo.com" target="_blank">https://api.smartcontractrepo.com</a>. The API is documented at <a href="https://api.smartcontractrepo.com/docs" target="_blank">https://api.smartcontractrepo.com/docs</a>. Take into account that a rate limit of 1000 requests per minute is applied to the API in order to prevent abuse.
                </p>
            </b-col>
        </b-row>
        <hr>
        <b-row>
            <b-col>
                <h5># Links</h5>
                <ul>
                    <li>
                        Paper: <a href="#" target="_blank">a-repository-for-smart-contracts</a>
                    </li>
                    <li>
                        Source Code: <a href="https://github.com/carl-egge/repo-smart-contracts/" target="_blank">https://github.com/carl-egge/repo-smart-contracts/</a>
                    </li>
                    <li>
                        GitHub Scraper: <a href="https://github.com/carl-egge/github-file-scraper" target="_blank">https://github.com/carl-egge/github-file-scraper</a>
                    </li>
                </ul>
            </b-col>
        </b-row>
        <hr>
        <b-row>
            <b-col>
                <h5># Credits</h5>
                <p>
                    This is a project from the Christian Doppler Labor at the Technical University Hamburg.
                    Thanks to the following people for their contributions:
                </p>
                <ul>
                    <li>Stefan Schulte</li>
                    <li>Avik Banerjee</li>
                    <li>Michael Schröder</li>
                    <li>Jürgen Cito</li>
                    <li>Carl Egge</li>
                </ul>
            </b-col>
        </b-row>
        <hr>
        <b-row>
            <b-col>
                <h5># License</h5>
                <p>
                    This project is licensed under the MIT License.
                </p>
            </b-col>
        </b-row>
    </b-container>
</template>

<script>
export default {

}
</script>