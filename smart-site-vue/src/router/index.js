import Router from 'vue-router'
import Vue from 'vue'

Vue.use(Router)

const homeView = () => import('../views/home-view.vue')
const loginView = () => import('../views/login-view.vue')
const registerView = () => import('../views/register-view.vue')
const contractView = () => import('../views/contract-view.vue')
const projectView = () => import('../views/project-view.vue')
const employeeView = () => import('../views/employee-view.vue')
const groupView = () => import('../views/group-view.vue')
const testView = () => import('../views/test-view.vue')
const clientView = () => import('../views/client-view.vue')

const routes = [{
	path: '/home',
	name: 'homeView',
	component: homeView
}, {
	path: '/login',
	name: 'loginView',
	component: loginView,
	alias: '/'
}, {
	path: '/register',
	name: 'registerView',
	component: registerView,
}, {
	path: '/contract',
	name: 'contractView',
	component: contractView,
}, {
	path: '/project',
	name: 'projectView',
	component: projectView,
}, {
	path: '/employee',
	name: 'employeeView',
	component: employeeView,
}, {
	path: '/group',
	name: 'groupView',
	component: groupView,
},{
	path: '/client',
	name: 'clientView',
	component: clientView,
},{
	path: '/test',
	name: 'testView',
	component: testView,
}]

const router = new Router({
	mode: 'hash',
	base: '/',
	routes
})

export default router