<template>
  <div>
    <h3>Create a New Smart Contract</h3>

    <div class="p-2 code-section">
      <form>
        <!-- Title -->
        <div class="container my-3 mx-0 px-0">
          <div class="row g-3 align-items-center">
            <div class="col-2 mx-2">
              <label for="titleTextInput" class="form-label"
                ><b>Title*:</b></label
              >
            </div>
            <div class="col">
              <input
                type="text"
                id="titleTextInput"
                class="form-control"
                v-model="title"
                required
              />
            </div>
          </div>
        </div>
        <!-- Description -->
        <div class="container my-3 mx-0 px-0">
          <div class="row g-3 align-items-center">
            <div class="col-2 mx-2">
              <label for="descriptionTextInput" class="form-label"
                ><b>Description:</b></label
              >
            </div>
            <div class="col">
              <input
                type="text"
                id="descriptionTextInput"
                class="form-control"
                v-model="description"
              />
            </div>
          </div>
        </div>
        <p>
          <b>Sourcecode:</b>
        </p>
        <prism-editor
          class="my-editor height-200"
          v-model="sourcecode"
          :highlight="highlighter"
          line-numbers
        ></prism-editor
        ><br />
        <p>
          <b>Bytecode:</b>
        </p>
        <prism-editor
          class="my-editor height-200"
          v-model="bytecode"
          :highlight="highlighter"
          line-numbers
        ></prism-editor
        ><br />
        <p>
          <b>ABI:</b>
        </p>
        <prism-editor
          class="my-editor height-200"
          v-model="abi"
          :highlight="highlighter"
          line-numbers
        ></prism-editor>
        <div class="my-4">
          <button
            type="button"
            class="btn btn-outline-success w-100"
            @click="createContract()"
          >
            Add New Contract
          </button>
        </div>
      </form>
    </div>
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
      title: "",
      description: null,
      sourcecode: "",
      bytecode: "",
      abi: "",
    };
  },
  methods: {
    /**
     * Set highlighting on prism editors
     */
    highlighter(code) {
      return highlight(code, languages.js); // languages.<insert language> to return html with markup
    },

    /**
     * Check if string is empty or has value
     */
    hasValue(val) {
      if (!(!val || val.length == 0 || val == "null")) return true;
      else false;
    },

    /**
     * POST to create a new contract in the database
     */
    async createContract() {
      if (this.title.length == 0) {
        alert("Title can't be emtpy.");
        return;
      }
      var data = {
        title: this.title,
      };
      if (this.hasValue(this.description)) data.description = this.description;
      if (this.hasValue(this.sourcecode)) data.sourcecode = this.sourcecode;
      if (this.hasValue(this.bytecode)) data.bytecode = this.bytecode;
      if (this.hasValue(this.abi)) data.abi = this.abi;
      const response = await ContractsService.create(data);
      if (response.status == "201") {
        this.$parent.makeToast(
          "201 :: Success",
          `The contract ${response.data.id} was saved.`,
          "success"
        );
        this.$router.push(`/contracts/${response.data.id}`);
      } else {
        this.$parent.makeToast(
          "422 :: Error",
          "Something went wrong.",
          "danger"
        );
      }
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
  border-radius: 4px;
}

.height-200 {
  height: 200px;
}

.code-section {
  border-radius: 4px;
  border: 1.5px solid #ccc;
}
</style>