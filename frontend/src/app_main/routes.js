/**************************************************************************************************
APP-MAIN ROUTES
**************************************************************************************************/
import * as PR from '../page-routes/_index.js'

export const RoutesConfig = [
   {
      title: 'Home',
      path: '/',
      component: PR.Home,
      order: 1,
   },
   {
      title: 'Rule Book',
      path: '/',
      component: PR.RuleBook,
      order: 2,
   },
   {
      title: 'Rules Loader',
      path: '/rules-loader',
      component: PR.RulesLoader,
      order: 3,
   },
]

