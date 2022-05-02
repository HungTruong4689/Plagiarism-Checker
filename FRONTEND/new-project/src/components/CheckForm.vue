<template>
  <form @submit.prevent="submitForm">
    <div class="form-control">
      <input
        id="user-name"
        name="user-name"
        type="text"
        placeholder="Enter the content here"
        v-show="show"
        v-model="testline"
      />
      <p
        id="user-name-output"
        v-bind:class="
          isActive == null
            ? 'default-text'
            : isActive
            ? 'plagiarism-text'
            : 'unique-text'
        "
        name="user-name-output"
        v-show="hide"
      >
        {{ this.testline }}
      </p>
      <p v-bind:class="isActive ? 'plagiarism-text' : 'unique-text'">
        {{ this.plagiarism }}
      </p>
      <br />
    </div>
    <!------
    // <div class="form-control">
    //   <select id="referrer" name="referrer" v-model="version">
    //     <option value="esv">English</option>
    //     <option value="vie2010">Vietnamese</option>
    //   </select>
    // </div> ---->
    <div>
      <button v-show="show_button">Compare</button>
    </div>
  </form>
  <div>
    <p v-show="hide">Similar sentence:</p>
    <p>{{ this.textresult }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "CheckForm",
  props: ["versionparent"],
  data() {
    return {
      testline: "",
      version: this.versionparent,
      clicked: false,
      show: true,
      hide: false,
      score: 0,
      textresult: "",
      plagiarism: "",
      point: 0,
      tip: 0,
      isActive: null,
      show_button: true,
    };
  },
  created: function () {
    this.testline = this.testlinechild;
    console.log(this.testline);
  },
  methods: {
    async submitForm() {
      console.log(this.version);
      this.clicked = true;
      this.show = false;
      this.hide = true;
      // var formData = new FormData();
      // console.log(this.testline);
      // console.log(this.version);
      // formData.append("text", this.testline);
      // formData.append("version", this.version);
      // formData.append("_method", "POST");
      //console.log(formData);
      const config = {
        headers: {
          // "content-type": "multipart/form-data",
          "content-type": "application/json",
        },
      };
      const url = "http://localhost:5000/predict";
      const object = {
        text: this.testline,
        version: this.version,
      };
      if (this.testline != "") {
        console.log("Point", this.testline);
        this.point = 1;
        console.log("Point", this.point);
      } else {
        this.plagiarism = "Please input the content";
      }
      await axios
        .post(url, object, config)
        .then((response) => {
          //const data = response.json();
          this.textresult = response.data[0].text;
          this.score = response.data[0].score;
          if (this.score >= 0.3) {
            this.plagiarism = "- Plagiarized";
            this.tip = 1;
            this.isActive = true;
            console.log("Tip", this.tip);
          } else {
            this.plagiarism = "- Unique";
            this.tip = 0;
            this.isActive = false;
            this.show_button = false;
          }
          console.log(response.data[0].score);
        })
        .catch((error) => {
          console.log(error);
        });
      // if (this.tip == 1) {
      //   this.plagiarism = "Plagiarism";
      // } else {
      //   this.plagiarism = "Unique";
      // }
      this.$emit("point", this.point);
      this.$emit("tip", this.tip);
    },
  },
  // computed: {
  //   changeClass(isActive) {
  //     switch (isActive) {
  //       case null:
  //         return "default-class";
  //       case true:
  //         return "plagiarism-text";
  //       case false:
  //         return "unique-text";
  //     }
  //   },
  // },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
form {
  max-width: 40rem;
  border: 1px solid #000;
  padding: 6px 10px;
  background-color: #ffffff;
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-control {
  margin: 0.5rem 0;
  display: flex;
  align-items: center;
  max-width: 370px;
}

#user-name-output {
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;

  margin-right: 4px;
}

label {
  font-weight: bold;
}

h2 {
  font-size: 1rem;
  margin: 0.5rem 0;
}

input {
  display: block;
  width: 400px;
  font: inherit;
  padding: 6px 12px;
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  outline: none;
}

select {
  width: auto;
}

button {
  font: inherit;
  background-color: #0076bb;
  color: white;
  cursor: pointer;
  padding: 8px 12px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
}

button:hover,
button:active {
  border-color: #002350;
  background-color: #002350;
}

.plagiarism-text {
  font-size: 14px;
  color: red;
  font-weight: bold;
  white-space: nowrap;
}

.unique-text {
  font-size: 14px;
  color: green;
  font-weight: bold;
  white-space: nowrap;
}

#user-name-output.plagiarism-text {
  font-weight: 400;
}

#user-name-output.unique-text {
  font-weight: 400;
}

.default-text {
  font-size: 14px;
  color: black;
}
</style>
