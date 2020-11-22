<template>
  <div id="app">
    <div style="width:50%" class="container">
      <div>
        <h2>COVID-19 Chatbot</h2>

        <h4>Please Input What you want to know about COVID-19：</h4>
        <input type="text" class="form-control" v-model="inputMessage" /><br/>

        <el-button type="primary" icon="el-icon-message" @click="submit" @keyup.enter.native="submit">Sent</el-button>
        <h5>ChatBot：</h5>
        <el-divider></el-divider>
        <div id="content">
          <h6>
          {{chatBotReply}}<br/>
          </h6>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default
  {
    name: 'app',
    data()
    {
      return {
        address:'http://localhost:8081/',
        inputMessage:'Hello',
        chatBotReply:''
      }
    },
    created () {
      document.onkeydown = (e) => {
        if (window.event === undefined) {
          var key = e.keyCode
        } else {
          // eslint-disable-next-line no-redeclare
          var key = window.event.keyCode
        }
        if (key === 13) {
          this.submit()
        }
      }
    },
    methods:
    {
      submit:function(){
        let _this = this
        this.axios({
          method:'get',
          url:this.address + this.inputMessage,
        }).then(function(response)
          {
            console.log(response.data)
            // console.log(_this.chatBotReply)
            _this.chatBotReply = response.data
            _this.inputMessage = ""
          });
      },
    },
  }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

#app h2 {
  font-size: 50px;
}

#app h5 {
  text-align: left;
  font-size: 24px;
}

#app h6 {
  height: 200px;
  width: auto;
  font-size: 18px;
  text-align: left;
  border-radius:2px;

}
</style>
