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
        <b-col cols="6">
          <b>Version Timestamp:</b> {{ this.timestamp }} (UTC)
        </b-col>
        <b-col>
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
      <b-row align-v="center" class="mb-4">
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
            @click="saveContract()"
          >
            Save Changes
          </b-button>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
import ContractsService from "@/services/ContractsService";
import CopyIcon from "@/components/copyIcon";
import EditIcon from "@/components/editIcon";
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
    CopyIcon,
    EditIcon,
  },
  data() {
    return {
      contract: {},
      version: 1,
      timestamp: "loading ...",
      sourcecode: "loading ...",
      bytecode: "loading ...",
      abi: "loading ...",
      title: "loading ...",
      description: "loading ...",
      disabledesc: true,
      disabletitle: true,
    };
  },
  mounted() {
    this.getContract(this.$route.params.id);
  },
  methods: {
    highlighter(code) {
      return highlight(code, languages.js); // languages.<insert language> to return html with markup
    },
    setCode(vid) {
      this.title = this.contract.title;
      this.description = this.contract.description;
      this.sourcecode = this.contract.versions[vid - 1].content.sourcecode
        ? this.contract.versions[vid - 1].content.sourcecode
        : "null";
      this.bytecode = this.contract.versions[vid - 1].content.bytecode
        ? this.contract.versions[vid - 1].content.bytecode
        : "null";
      this.abi = this.contract.versions[vid - 1].content.abi
        ? this.contract.versions[vid - 1].content.abi
        : "null";
      this.findTimestamp(this.version);
    },
    changeVersion(vid) {
      this.version = vid;
      this.setCode(vid);
    },
    findTimestamp(vid) {
      var tmp = new Date(this.contract.versions[vid - 1].created);
      this.timestamp = tmp.toLocaleDateString("de-DE", {
        hour: "numeric",
        minute: "numeric",
      });
    },
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
    async getContract(iden) {
      const response = await ContractsService.get(iden);
      this.contract = response.data;
      this.version = this.contract.latestVersion;
      this.setCode(this.version);
    },
    async saveContract() {
      const data = {
        title: this.title,
        description: this.description,
        sourcecode: this.sourcecode,
        bytecode: this.bytecode,
        abi: this.abi,
      };
      const response = await ContractsService.update(this.contract.id, data);
      this.getContract(this.$route.params.id);
    },
    async deleteContract() {
      await ContractsService.delete(this.contract.id);
      this.$router.push("/");
    },
    async deleteContractVersion() {
      if (this.contract.versions.length == 1) return this.deleteContract();
      await ContractsService.deleteVers(this.contract.id, this.version);
      this.getContract(this.contract.id);
    },
    async copyToClipBoard(textToCopy) {
      await navigator.clipboard.writeText(textToCopy);
    },
  },
};
</script>


<style scoped>
.height-300 {
  height: 300px;
}
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