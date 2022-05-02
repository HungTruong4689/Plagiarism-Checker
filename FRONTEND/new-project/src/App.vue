<template>
  <div class="show-result">
    <div class="container">
      <div class="complete">Complete</div>

      <div class="loading-bar">
        <div class="percentage" :style="{ width: changecontent + '%' }">
          <span>{{ changecontent }}&percnt;</span>
        </div>
      </div>
    </div>
    <div>
      <h1>{{ changeunique }}&percnt;</h1>
      <div>Unique Content</div>
    </div>
    <div>
      <h1>{{ changeplagiarism }}&percnt;</h1>
      <div>Plagiarized Content</div>
    </div>
  </div>
  <div class="listview">
    <div>
      <div class="select-control">
        <div>
          <label>Language:</label>
          <select id="referrer" name="referrer" v-model="versionparent">
            <option value="esv">English</option>
            <option value="vie2010">Vietnamese</option>
          </select>
        </div>
      </div>
    </div>
    <CheckForm
      @point="updatepoint"
      @tip="updatetip"
      :versionparent="versionparent"
      v-for="item in 10"
      :key="item"
    />
  </div>
</template>

<script>
import CheckForm from "./components/CheckForm.vue";

export default {
  name: "App",
  data() {
    return {
      versionparent: "esv",
      parentpoint: 0,
      parenttip: 0,
      uniquerate: 0,
      plagiarismrate: 0,
      complete: 0,
      percentage: 50,
    };
  },

  components: {
    CheckForm,
  },
  methods: {
    updatepoint(variable) {
      this.parentpoint += variable;
    },
    updatetip(variable) {
      this.parenttip += variable;
    },
  },
  computed: {
    changecontent() {
      let complete;
      complete = Math.round((this.parentpoint / 10) * 100);
      // this.plagiarismrate = Math.round(
      //   (this.parenttip / this.parentpoint) * 100
      // );
      // this.uniquerate = 100 - this.plagiarismrate;
      return complete;
    },
    changeunique() {
      let uniquerate;
      // complete = Math.round((this.parentpoint / 10) * 100);
      // this.plagiarismrate = Math.round(
      //   (this.parenttip / this.parentpoint) * 100
      // );
      if (this.parentpoint == 0) {
        uniquerate = 0;
      } else {
        uniquerate =
          100 - Math.round((this.parenttip / this.parentpoint) * 100);
      }

      return uniquerate;
    },
    changeplagiarism() {
      let plagiarismrate;
      // complete = Math.round((this.parentpoint / 10) * 100);
      if (this.parentpoint == 0) {
        plagiarismrate = 0;
      } else {
        plagiarismrate = Math.round((this.parenttip / this.parentpoint) * 100);
      }

      // this.uniquerate = 100 - this.plagiarismrate;
      return plagiarismrate;
    },
  },
};
// const app = {
//   data() {
//     return {
//       friends: [
//         {
//           id: "manuel",
//           name: "Manuel Lorenz",
//           phone: "0123 456 78 90",
//           email: "manuel@localhost.com",
//         },
//         {
//           id: "manuel",
//           name: "Manuel Lorenz",
//           phone: "0123 456 78 90",
//           email: "manuel@localhost.com",
//         },
//       ],
//     };
//   },
// };
</script>

<style>
:root {
  --border-color: #1d3c78;
  --unique-color: #027902;
  --plagiarized-color: #d6292f;
}

html {
  padding: 0;
  box-sizing: border-box;
  display: flex;
  justify-content: center;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 60px;
  border: 1.5px solid var(--border-color);
  margin: 40px auto;
}

.show-result {
  max-width: 40rem;
  background-color: #ffffff;
  display: flex;
  text-align: center;
}

.container {
  padding: 10px 24px;
  width: 540px;
  max-width: 300px;
  border-bottom: 1.5px solid var(--border-color);
  border-right: 1.5px solid var(--border-color);
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.show-result > div:nth-child(2) {
  border-bottom: 1.5px solid var(--border-color);
  padding: 6px 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
}

.show-result > div:nth-child(3) {
  border-left: 1.5px solid var(--border-color);
  border-bottom: 1.5px solid var(--border-color);
  padding: 6px 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
}

.show-result > div:nth-child(2) h1,
.show-result > div:nth-child(3) h1 {
  margin: 0;
  font-size: 50px;
}

.show-result > div:nth-child(2) div,
.show-result > div:nth-child(3) div {
  font-size: 12px;
  font-weight: 600;
}

.show-result > div:nth-child(2) h1,
.show-result > div:nth-child(2) div {
  color: var(--unique-color);
}

.show-result > div:nth-child(3) h1,
.show-result > div:nth-child(3) div {
  color: var(--plagiarized-color);
}

.show-result div h1 {
  font-weight: 400;
}

.complete {
  font-size: 18px;
  font-weight: 400;
  text-transform: uppercase;
  margin-bottom: 20px;
}

.loading-bar {
  position: relative;
  width: 100%;
  height: 30px;
  border-bottom: 1px solid #ddd;
  box-shadow: inset 0 1px 2px rgba($color: #000, $alpha: 0.4), 0 -1px 1px #fff,
    0 1px 0 #fff;
}

.percentage {
  position: absolute;
  top: 1px;
  left: 1px;
  right: 1px;
  display: block;
  height: 100%;
  background-color: #a5df41;
  background-size: 30px 30px;
  background-image: linear-gradient(
    135deg,
    rgba($color: #fff, $alpha: 0.15) 25%,
    transparent 25%,
    transparent 50%,
    rgba($color: #fff, $alpha: 0.15) 50%,
    rgba($color: #fff, $alpha: 0.15) 75%,
    transparent 75%,
    transparent
  );
  animation: animate-stripes 3s linear infinite;
}

.percentage span {
  line-height: 31px;
  font-size: 15px;
  margin-top: 2px;
  margin-left: 6px;
}

.listview {
  padding: 0 20px 10px;
}

.select-control {
  display: flex;
  padding-top: 10px;
}

.select-control div {
  display: flex;
  flex-direction: column;
  margin-right: 20px;
}

.select-control div label {
  margin-bottom: 4px;
}

// Animations
@keyframes animate-stripes {
  0% {
    background-position: 0 0;
  }
  100% {
    background-position: 60px 0;
  }
}
</style>
