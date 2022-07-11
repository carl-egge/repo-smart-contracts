<template>
  <div>
    <b-container class="px-0 mb-2" fluid>
      <b-row align-h="start" align-v="center">
        <b-col cols="auto" style="font-size: 1.85rem">
          <strong>{{ this.title }}</strong>
        </b-col>
        <b-col class="text-secondary">
          ({{ this.contract.id }})
          <b-button
            variant="outline-secondary"
            class="id-copy-button"
            @click="copyToClipBoard(contract.id)"
          >
            <b-icon icon="clipboard"></b-icon>
          </b-button>
        </b-col>
      </b-row>
      <b-row align-h="start" align-v="center">
        <b-col cols="auto">
          <b-dropdown
            id="choose-Version"
            variant="outline-secondary"
            class="m-md-2"
            size="sm"
          >
            <template #button-content> Version: {{ version }} </template>
            <b-dropdown-item
              v-for="vers in contract.versions"
              :key="vers.vid"
              @click="changeVersion(vers.vid)"
            >
              Version: {{ vers.vid }}
            </b-dropdown-item>
          </b-dropdown>
        </b-col>
        <b-col cols="auto">
          <b-button
            type="button"
            variant="outline-secondary"
            size="sm"
            @click="deleteContractVersion()"
          >
            Delete Version {{ version }}
          </b-button>
        </b-col>
      </b-row>
      <b-row align-h="start" align-v="center" class="ml-2">
        <b-col> <b>Version Timestamp:</b> {{ this.timestamp }} (UTC) </b-col>
        <b-col> <b>Parent Versions:</b> [{{ this.parents }}] </b-col>
      </b-row>
      <b-row align-h="start" align-v="center" class="ml-2">
        <b-col> <b>Commit Message:</b> {{ this.commitmsg }} </b-col>
        <b-col> <b>Git Sha:</b> {{ this.git_sha }} </b-col>
      </b-row>
    </b-container>

    <b-container class="code-section p-2" fluid>
      <!-- Title -->
      <b-row align-v="center" class="mb-2">
        <b-col
          ><label for="inline-form-input-title">
            <strong>Title:</strong>
          </label></b-col
        >
        <b-col cols="8">
          <b-form-input
            type="text"
            id="inline-form-input-title"
            class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="..."
            v-model="title"
            :disabled="disabletitle"
          ></b-form-input>
        </b-col>
        <b-col>
          <b-button
            variant="outline-secondary"
            class="icon-button"
            @click="copyToClipBoard(contract.title)"
          >
            <b-icon icon="clipboard"></b-icon>
          </b-button>
          <b-button
            variant="outline-secondary"
            class="icon-button"
            @click="edit('title')"
          >
            <b-icon icon="pen"></b-icon>
          </b-button>
        </b-col>
      </b-row>
      <!-- Description -->
      <b-row align-v="center" class="mb-2">
        <b-col
          ><label for="inline-form-input-desc">
            <strong>Description:</strong>
          </label></b-col
        >
        <b-col cols="8">
          <b-form-input
            type="text"
            id="inline-form-input-desc"
            class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="..."
            v-model="description"
            :disabled="disabledesc"
          ></b-form-input>
        </b-col>
        <b-col>
          <b-button
            variant="outline-secondary"
            class="icon-button"
            @click="copyToClipBoard(contract.description)"
          >
            <b-icon icon="clipboard"></b-icon>
          </b-button>
          <b-button
            variant="outline-secondary"
            class="icon-button"
            @click="edit('desc')"
          >
            <b-icon icon="pen"></b-icon>
          </b-button>
        </b-col>
      </b-row>
      <!-- Source -->
      <b-row align-v="center" class="mb-2">
        <b-col
          ><label for="inline-form-input-src">
            <strong>Source:</strong>
          </label></b-col
        >
        <b-col cols="8">
          <b-form-input
            type="text"
            id="inline-form-input-src"
            class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="..."
            v-model="source"
            :disabled="true"
          ></b-form-input>
        </b-col>
        <b-col>
          <b-button
            variant="outline-secondary"
            class="icon-button"
            @click="copyToClipBoard(contract.source)"
          >
            <b-icon icon="clipboard"></b-icon>
          </b-button>
        </b-col>
      </b-row>
      <!-- Source file path -->
      <b-row align-v="center" class="mb-4">
        <b-col
          ><label for="inline-form-input-path">
            <strong>Source file path:</strong>
          </label></b-col
        >
        <b-col cols="8">
          <b-form-input
            type="text"
            id="inline-form-input-path"
            class="mb-2 mr-sm-2 mb-sm-0"
            placeholder="..."
            v-model="source_file_path"
            :disabled="true"
          ></b-form-input>
        </b-col>
        <b-col>
          <b-button
            variant="outline-secondary"
            class="icon-button"
            @click="copyToClipBoard(contract.source_file_path)"
          >
            <b-icon icon="clipboard"></b-icon>
          </b-button>
        </b-col>
      </b-row>
    </b-container>
    <b-container class="mt-2 code-section p-2" fluid>
      <!-- Source Code -->
      <b-row align-v="center" class="m-2">
        <strong>Sourcecode: </strong>
        <b-button
          variant="outline-secondary"
          class="icon-button ml-2"
          @click="copyToClipBoard(sourcecode)"
        >
          <b-icon icon="clipboard"></b-icon>
        </b-button>
        <prism-editor
          class="my-editor height-300"
          v-model="sourcecode"
          :highlight="highlighter"
          line-numbers
          placeholder="start typing here ..."
        >
        </prism-editor>
      </b-row>
      <!-- Byte Code -->
      <b-row align-v="center" class="m-2">
        <strong>Bytecode: </strong>
        <b-button
          variant="outline-secondary"
          class="icon-button ml-2"
          @click="copyToClipBoard(bytecode)"
        >
          <b-icon icon="clipboard"></b-icon>
        </b-button>
        <prism-editor
          class="my-editor height-300"
          v-model="bytecode"
          :highlight="highlighter"
          line-numbers
          placeholder="start typing here ..."
        >
        </prism-editor>
      </b-row>
      <!-- ABI -->
      <b-row align-v="center" class="m-2">
        <strong>ABI: </strong>
        <b-button
          variant="outline-secondary"
          class="icon-button ml-2"
          @click="copyToClipBoard(abi)"
        >
          <b-icon icon="clipboard"></b-icon>
        </b-button>
        <prism-editor
          class="my-editor height-300"
          v-model="abi"
          :highlight="highlighter"
          line-numbers
          placeholder="start typing here ..."
        >
        </prism-editor>
      </b-row>
      <b-row>
        <b-col>
          <b-button
            type="button"
            variant="outline-danger"
            block
            @click="deleteContract()"
          >
            Delete this Contract
          </b-button>
        </b-col>
        <b-col>
          <b-button
            type="submit"
            variant="outline-success"
            block
            @click="$bvModal.show('bv-modal')"
          >
            Save Changes
          </b-button>
        </b-col>
      </b-row>
    </b-container>

    <!-- Save Modal -->
    <b-modal id="bv-modal" hide-footer size="lg">
      <template #modal-title> Save Smart Contract </template>
      <div class="d-block">
        <b-form-group
          id="modal-input-group-1"
          label="Update Message: (recommended)"
          label-for="modal-input-1"
        >
          <b-form-input
            id="modal-input-1"
            v-model="new_commitmsg"
            placeholder="start typing ..."
          ></b-form-input>
        </b-form-group>
        <b-form-group
          id="modal-input-group-2"
          label="Git Sha: (optional)"
          label-for="modal-input-2"
        >
          <b-form-input
            id="modal-input-2"
            v-model="new_git_sha"
            placeholder="optional ..."
          ></b-form-input>
        </b-form-group>
        <b-form-checkbox
          v-model="show_new_parents"
          name="switch-button-abi"
          switch
        >
          Configure Parents
        </b-form-checkbox>
        <b-form-group
          v-if="show_new_parents"
          id="modal-input-group-3"
          label="Parents: (optional)"
          label-for="modal-input-3"
        >
          <b-form-select
            v-model="new_parent1"
            :options="contract.versions"
            text-field="vid"
            value-field="vid"
            size="sm"
            class="col-1"
          >
            <template #first>
              <b-form-select-option :value="null">null</b-form-select-option>
            </template>
          </b-form-select>
          <b-form-select
            v-model="new_parent2"
            :options="contract.versions"
            text-field="vid"
            value-field="vid"
            size="sm"
            class="col-1"
          >
            <template #first>
              <b-form-select-option :value="null">null</b-form-select-option>
            </template>
          </b-form-select>
        </b-form-group>
      </div>
      <b-button
        class="mt-3"
        variant="outline-success"
        type="submit"
        block
        @click="saveContract()"
      >
        Save
      </b-button>
    </b-modal>
  </div>
</template>

<script>
import ContractsService from "@/services/ContractsService";

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
      contract: {},
      version: 1,
      timestamp: "loading ...",
      parents: "loading ...",
      commitmsg: "",
      git_sha: "",
      sourcecode: "loading ...",
      bytecode: "loading ...",
      abi: "loading ...",
      title: "loading ...",
      description: "loading ...",
      source: "loading ...",
      source_file_path: "loading ...",
      disabledesc: true,
      disabletitle: true,
      new_commitmsg: "",
      new_parent1: null,
      new_parent2: null,
      new_git_sha: "",
      show_new_parents: false,
    };
  },
  mounted() {
    this.getContract(this.$route.params.id);
  },
  methods: {
    /**
     * Set highlighting on prism editors
     */
    highlighter(code) {
      return highlight(code, languages.js); // languages.<insert language> to return html with markup
    },

    /**
     * Update the variables on the page
     */
    setCode(vid) {
      this.title = this.contract.title;
      this.description = this.contract.description;
      this.source = this.contract.source;
      this.source_file_path = this.contract.source_file_path;
      this.sourcecode = this.contract.versions[vid - 1].content.sourcecode
        ? this.contract.versions[vid - 1].content.sourcecode
        : "";
      this.bytecode = this.contract.versions[vid - 1].content.bytecode
        ? this.contract.versions[vid - 1].content.bytecode
        : "";
      this.abi = this.contract.versions[vid - 1].content.abi
        ? this.contract.versions[vid - 1].content.abi
        : "";
      this.parents = this.contract.versions[vid - 1].parents.toString();
      this.commitmsg = this.contract.versions[vid - 1].message;
      this.git_sha = this.contract.versions[vid - 1].git_sha;
      this.findTimestamp(this.version);
    },

    /**
     * Dropdown change version of contract
     */
    changeVersion(vid) {
      this.version = vid;
      this.setCode(vid);
    },

    /**
     * Format the timestamp of the version
     */
    findTimestamp(vid) {
      var tmp = new Date(this.contract.versions[vid - 1].created);
      this.timestamp = tmp.toLocaleDateString("de-DE", {
        hour: "numeric",
        minute: "numeric",
      });
    },

    /**
     * Buttons to activate textfields of text or description
     */
    edit(prop) {
      if (prop == "desc") {
        const temp = this.disabledesc;
        this.disabledesc = !temp;
      }
      if (prop == "title") {
        const temp = this.disabletitle;
        this.disabletitle = !temp;
      } else {
        return;
      }
    },

    /**
     * Check if string is empty or has value
     */
    hasValue(val) {
      if (!(!val || val.length == 0 || val == "null")) return true;
      else false;
    },

    /**
     * GET contract from server
     */
    async getContract(iden) {
      const response = await ContractsService.get(iden);
      this.contract = response.data;
      if (!this.contract) {
        this.$parent.makeToast(
          "Error",
          `The contract ID is unknown.`,
          "danger"
        );
        this.$router.push("/");
      }
      this.version = this.contract.latestVersion;
      this.setCode(this.version);
    },

    /**
     * PUT to update contract in database
     */
    async saveContract() {
      this.$bvModal.hide("bv-modal");
      const data = {
        title: this.title,
      };
      if (this.hasValue(this.new_commitmsg)) data.message = this.new_commitmsg;
      if (this.hasValue(this.new_git_sha)) data.git_sha = this.new_git_sha;
      if (this.hasValue(this.description)) data.description = this.description;
      if (this.hasValue(this.sourcecode)) data.sourcecode = this.sourcecode;
      if (this.hasValue(this.bytecode)) data.bytecode = this.bytecode;
      if (this.hasValue(this.abi)) data.abi = this.abi;
      let parents = [];
      if (this.new_parent1) parents.push(this.new_parent1);
      if (this.new_parent2) parents.push(this.new_parent2);
      if (parents.length != 0) data.parents = parents;
      const response = await ContractsService.update(this.contract.id, data);
      if (response.status == "200") {
        this.$parent.makeToast(
          "200 :: Success",
          `The contract ${response.data.id} was saved.`,
          "success"
        );
      } else {
        this.$parent.makeToast(
          "422 :: Error",
          "Something went wrong.",
          "danger"
        );
      }
      this.getContract(this.$route.params.id);
    },

    /**
     * DELETE a contract from database
     */
    async deleteContract() {
      const response = await ContractsService.delete(this.contract.id);
      if (response.status == "204") {
        this.$parent.makeToast(
          "204 :: Success",
          "The contract was deleted.",
          "success"
        );
        this.$router.push("/");
      } else {
        this.$parent.makeToast(
          "422 :: Error",
          "Something went wrong.",
          "danger"
        );
        this.getContract(this.contract.id);
      }
    },

    /**
     * DELETE a single version of the contract from the database
     */
    async deleteContractVersion() {
      if (this.contract.versions.length == 1) return this.deleteContract();
      const temp_version = this.version;
      const response = await ContractsService.deleteVers(
        this.contract.id,
        this.version
      );
      if (response.status == "204") {
        this.$parent.makeToast(
          "204 :: Success",
          `Version ${temp_version} of contract ${this.contract.id} was deleted.`,
          "success"
        );
        this.getContract(this.contract.id);
      } else {
        this.$parent.makeToast(
          "422 :: Error",
          "Something went wrong.",
          "danger"
        );
        this.getContract(this.contract.id);
      }
    },

    /**
     * Helper function to copy values to the users clipboard
     */
    async copyToClipBoard(textToCopy) {
      await navigator.clipboard.writeText(textToCopy);
    },
  },
};
</script>


<style scoped>
.my-editor {
  /* we dont use `language-` classes anymore so thats why we need to add background and text color manually */
  background: #eee; /*#2d2d2d;*/
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

.height-300 {
  height: 300px;
}

.code-section {
  border-radius: 4px;
  border: 1.5px solid #ccc;
}

.id-copy-button {
  padding: 0.1rem 0.35rem;
  font-size: 0.7rem;
}

.icon-button {
  padding: 0.3rem 0.3rem;
  font-size: 0.9rem;
}
</style>