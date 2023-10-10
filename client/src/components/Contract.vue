<template>
  <div>
    <!-- Title section -->
    <b-container fluid>
      <b-row>
        <b-col>
          <h4 class="font-weight-bold">{{ this.contract.name }}</h4>
        </b-col>
      </b-row>
      <b-row>
        <b-col class="text-secondary">
          ({{ this.contract.id }})
          <b-button variant="outline-secondary" class="id-copy-button" @click="copyToClipBoard(contract.id)">
            <b-icon icon="clipboard"></b-icon>
          </b-button>
        </b-col>
      </b-row>
    </b-container>
    <br />
    <!-- General Contract Information -->
    <b-container class="code-section" fluid>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Sha: </b-col>
        <b-col> {{ this.contract.sha }} </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Path: </b-col>
        <b-col> {{ this.contract.path }} </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Language: </b-col>
        <b-col> {{ this.contract.language }} </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> License: </b-col>
        <b-col> {{ this.contract.license }} </b-col>
      </b-row>
    </b-container>
    <br />
    <!-- Repository Information -->
    <h6 class="font-italic">Repository:</h6>
    <b-container class="code-section" fluid>
      <b-row>
        <b-col>
          <a :href="'https://github.com/' + this.contract.repo.full_name" target="_blank">
            <strong>{{ this.contract.repo.full_name }}</strong>
          </a>
          <span class="text-secondary">({{ this.contract.repo.repo_id }})</span>
        </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Description: </b-col>
        <b-col> {{ this.contract.repo.description }} </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> url: </b-col>
        <b-col>
          <a :href="this.contract.repo.url" target="_blank">{{ this.contract.repo.url }}</a>
        </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Owner: </b-col>
        <b-col> {{ owner }} </b-col>
      </b-row>
    </b-container>
    <br />
    <!-- Versions Information -->
    <h6 class="font-italic">Versions:</h6>
    <b-container class="code-section" v-if="this.contract.versions.length > 0" fluid>
      <b-row v-if="show_version_dropdown">
        <b-col cols="auto">
          <b-dropdown id="choose-Version" variant="outline-secondary" class="m-2" size="sm">
            <template #button-content> Version: {{ current_version + 1 }} </template>
            <b-dropdown-item v-for="vers in contract.versions" :key="vers.version_id"
              @click="changeVersion(vers.version_id)">
              Version: {{ vers.version_id }}
            </b-dropdown-item>
          </b-dropdown>
        </b-col>
      </b-row>
      <b-row v-else>
        <b-button variant="outline-secondary" size="sm" class="m-2" disabled>
          Version: 1
        </b-button>
        <span class="font-weight-lighter m-2" style="font-size: 0.9em;">(only one version available)</span>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Sha: </b-col>
        <b-col> {{ this.contract.versions[current_version].sha }} </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Message: </b-col>
        <b-col> {{ this.contract.versions[current_version].message }} </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Size: </b-col>
        <b-col> {{ this.contract.versions[current_version].size }} </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Created: </b-col>
        <b-col> {{ this.contract.versions[current_version].created | formatDate }} (UTC)</b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Compiler: </b-col>
        <b-col> {{ this.contract.versions[current_version].compiler_version }} </b-col>
      </b-row>
      <b-row v-if="show_version_dropdown">
        <b-col class="font-weight-bold" md="2" lg="1"> Parents: </b-col>
        <b-col> {{ this.contract.versions[current_version].parents }} </b-col>
      </b-row>
      <b-row>
        <b-col class="font-weight-bold" md="2" lg="1"> Sourcecode: </b-col>
        <b-col>
          <b-button variant="outline-secondary" class="icon-button ml-2"
            @click="copyToClipBoard(contract.versions[current_version].content)">
            <b-icon icon="clipboard"></b-icon>
          </b-button>
        </b-col>
      </b-row>
      <b-row>
        <b-col>
          <prism-editor class="my-editor height-500" v-model="this.contract.versions[current_version].content"
            :highlight="highlighter" line-numbers placeholder="no source code here ...">
          </prism-editor>
        </b-col>
      </b-row>
    </b-container>
    <p v-else>Sorry, no Versions here!</p>
  </div>
</template>

<script>
import ContractsService from "@/services/ContractsService";
import FlatContractsService from "@/services/FlatContractsService";

// import Prism Editor
import { PrismEditor } from "vue-prism-editor";
import "vue-prism-editor/dist/prismeditor.min.css"; // import the styles somewhere

// import highlighting library (you can use any library you want just return html string)
import { highlight, languages } from "prismjs/components/prism-core";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/themes/prism-tomorrow.css"; // import syntax highlighting styles

export default {
  components: {
    PrismEditor,
  },
  data() {
    return {
      contract: {
        repo: {
          repo_id: "loading ...",
          full_name: "loading ...",
          owner_id: "loading ...",
          description: "loading ...",
          url: "loading ...",
        },
        versions: [],
      },
      current_version: 0,
      show_version_dropdown: true,
    };
  },
  created() {
    this.getContract(this.$route.params.id);
  },
  computed: {
    /**
     * Get the Owner of the repository
     */
    owner() {
      if (this.contract == {}) {
        return "loading ...";
      }
      if (this.contract.repo.full_name.indexOf("/") > -1) {
        return this.contract.repo.full_name.split("/")[0] + " (" + this.contract.repo.owner_id + ")";
      } else {
        return this.contract.repo.owner_id;
      }
    },
  },
  methods: {
    /**
     * GET contract from server
     */
    async getContract(iden) {
      const routeName = this.$route.name;
      let response = {}
      if (routeName == 'ContractDetails') {
        response = await ContractsService.get(iden);
      } else {
        response = await FlatContractsService.get(iden);
      }
      if (response.data.status == 404) {
        this.$parent.makeToast(
          "Error",
          `The contract ID is unknown.`,
          "danger"
        );
        this.$router.push("/");
      } else {
        this.contract = response.data.data;
        if (this.contract.versions.length < 1) {
          this.$parent.makeToast(
            "Error",
            `No versions found for this contract.`,
            "danger"
          );
        } if (this.contract.versions.length == 1) {
          this.show_version_dropdown = false;
          this.current_version = 0;
        } else {
          this.current_version = this.contract.versions.length - 1;
        }
      }
    },

    /**
     * Set highlighting on prism editors
     */
    highlighter(code) {
      return highlight(code, languages.js); // languages.<insert language> to return html with markup
    },

    /**
     * Dropdown change version of contract
     */
    changeVersion(vid) {
      this.current_version = vid - 1;
      this.$forceUpdate();
    },

    /**
     * Helper function to copy values to the users clipboard
     */
    async copyToClipBoard(textToCopy) {
      await navigator.clipboard.writeText(textToCopy);
    },
  },
  filters: {
    /**
     * Filter to format the timestamp
     */
    formatDate: function (value) {
      if (!value) return "";
      var tmp = new Date(value);
      return tmp.toLocaleDateString
        // ("de-DE", {
        //   hour: "numeric",
        //   minute: "numeric",
        // });
        ("en-us", {
          hour: "numeric",
          minute: "numeric",
        });
    },
  },
};
</script>


<style scoped>
.my-editor {
  /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
  background: #eee;
  /*#2d2d2d;*/
  color: #ccc;

  /* you must provide font-family font-size line-height. Example: */
  font-family: Fira code, Fira Mono, Consolas, Menlo, Courier, monospace;
  font-size: 14px;
  line-height: 1.5;
  padding: 5px;
  margin-top: 0.5rem;
  margin-bottom: 0.5rem;
  border-radius: 4px;
}

.height-500 {
  height: 500px;
}

.code-section {
  border-radius: 4px;
  border: 1.5px solid #ccc;
}

.id-copy-button {
  padding: 0.1rem 0.35rem;
  font-size: 0.6rem;
}

.icon-button {
  padding: 0.1rem 0.35rem;
  font-size: 0.7rem;
}
</style>