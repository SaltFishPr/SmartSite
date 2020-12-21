import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

const store = new Vuex.Store({
	state: {
		verification: 'jl'
	},
	mutations: {
		verificationGet (state,value) {
		  // 变更状态 
		  state.verification = value;
		}
	  }
})

export default store